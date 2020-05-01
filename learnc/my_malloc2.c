#include <errno.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/time.h>
#include <assert.h>
#include <sys/mman.h>

#include <stdint.h>

//
// Buddy allocator
//

#define LEAF_SIZE     16 // The smallest allocation size (in bytes)
#define NSIZES        5 // Number of entries in bd_sizes array
#define MAXSIZE       (NSIZES-1) // Largest index in bd_sizes array
#define BLK_SIZE(k)   ((1L << (k)) * LEAF_SIZE) // Size in bytes for size k
#define HEAP_SIZE     BLK_SIZE(MAXSIZE) 
#define NBLK(k)       (1 << (MAXSIZE-k))  // Number of block at size k
#define ROUNDUP(n,sz) (((((n)-1)/(sz))+1)*(sz))  // Round up to the next multiple of sz

// A double-linked list for the free list of each level
struct bd_list {
  struct bd_list *next;
  struct bd_list *prev;
};
typedef struct bd_list Bd_list;

// The allocator has sz_info for each size k. Each sz_info has a free
// list, an array alloc to keep track which blocks have been
// allocated, and an split array to to keep track which blocks have
// been split.  The arrays are of type char (which is 1 byte), but the
// allocator uses 1 bit per block (thus, one char records the info of
// 8 blocks).
struct sz_info {
  struct bd_list free;
  char *alloc;
  char *split;
};
typedef struct sz_info Sz_info;

static Sz_info bd_sizes[NSIZES]; 
static void *bd_base;   // start address of memory managed by the buddy allocator

// List functions that the buddy allocator uses. Implementations
// are at the end of the buddy allocator code.
void lst_init(Bd_list*);
void lst_remove(Bd_list*);
void lst_push(Bd_list*, void *);
void *lst_pop(Bd_list*);
void lst_print(Bd_list*);
int lst_empty(Bd_list*);
  
// Return 1 if bit at position index in array is set to 1
int bit_isset(char *array, int index) {
  char b = array[index/8];
  char m = (1 << (index % 8));
  return (b & m) == m;
}

// Set bit at position index in array to 1
void bit_set(char *array, int index) {
  char b = array[index/8];
  char m = (1 << (index % 8));
  array[index/8] = (b | m);
}

// Clear bit at position index in array
void bit_clear(char *array, int index) {
  char b = array[index/8];
  char m = (1 << (index % 8));
  array[index/8] = (b & ~m);
}

void flip_bit(char *array, int index) {
  index >>= 1; // index /= 2
  char m = (1 << (index % 8));
  array[index/8] ^= m;
}

int bit_get(char *array, int index) {
  index >>= 1; // index /= 2
  char b = array[index/8];
  char m = (1 << (index % 8));
  return (b & m) == m;
}

void
bd_print() {
  printf("=== buddy allocator state ===\n");
  for (int k = 0; k < NSIZES; k++) {
    printf("size %d (%ld): free list: ", k, BLK_SIZE(k));
    lst_print(&bd_sizes[k].free);
    printf("  alloc:");
    for (int b = 0; b < NBLK(k)/2; b++) {
      printf(" %d", bit_isset(bd_sizes[k].alloc, b));
    }
    if (NBLK(k) == 1) {
      printf(" %d", bit_isset(bd_sizes[k].alloc, 0));
    }
    printf("\n");
    if(k > 0) {
      printf("  split:");
      for (int b = 0; b < NBLK(k); b++) {
	      printf(" %d", bit_isset(bd_sizes[k].split, b));
      }
      printf("\n");
    }
  }
}

// Mark memory from [start, stop), starting at size 0, as allocated. 
void
bd_mark(void *start, void *stop)
{
  int bi, bj;

  for (int k = 0; k < NSIZES; k++) {
    bi = blk_index(k, start);
    bj = blk_index_next(k, stop);
    for(; bi < bj; bi++) {
      if(k > 0) {
        // if a block is allocated at size k, mark it as split too.
        bit_set(bd_sizes[k].split, bi);
      }
      flip_bit(bd_sizes[k].alloc, bi);
    }
  }
}

// Mark the range [bd_base,p) as allocated
int
bd_mark_data_structures(char *p) {
  int meta = p - (char*)bd_base;
  printf("bd: %d meta bytes for managing %d bytes of memory\n", meta, BLK_SIZE(MAXSIZE));
  bd_mark(bd_base, p);
  return meta;
}

#define in_range(a, b, x) (((x) >= (a)) && ((x) < (b)))

// Convert a block index at size k back into an address
void *addr(int k, int bi) {
  int n = bi * BLK_SIZE(k);
  return (char *) bd_base + n;
}

int
bd_initfree_pair(int k, int bi, void *free_start, void *free_end) {
  int buddy = (bi % 2 == 0) ? bi+1 : bi-1;
  int free = 0;
  if(bit_get(bd_sizes[k].alloc, bi)) {
    // one of the pair is free
    free = BLK_SIZE(k);
    if(in_range(free_start, free_end, addr(k, buddy)))
      lst_push(&bd_sizes[k].free, addr(k, buddy));   // put buddy on free list
    else
      lst_push(&bd_sizes[k].free, addr(k, bi));      // put bi on free list
  } else {
    printf("k(%d) is skipped for index(%d)!\n", k, bi);
  }
  return free;
}
  
// Initialize the free lists for each size k.  For each size k, there
// are only two pairs that may have a buddy that should be on free list:
// bd_left and bd_right.
int
bd_initfree(void *bd_left, void *bd_right) {
  int free = 0;

  for (int k = 0; k < MAXSIZE; k++) {   // skip max size
    int left = blk_index_next(k, bd_left);
    int right = blk_index(k, bd_right);
    int cache = bd_initfree_pair(k, left, bd_left, bd_right);
    free+=cache;
    printf("k(%d), left index(%d), free size(%d)\n", k, left, cache);
    if(right <= left) // right == left means at highest level!
      continue;
    cache = bd_initfree_pair(k, right, bd_left, bd_right);
    free+=cache;
    printf("k(%d), right index(%d), free size(%d)\n\n", k, right, cache);
  }
  return free;
}

// Allocate memory for the heap managed by the allocator, and allocate
// memory for the data structures of the allocator.
void
bd_init() {
  bd_base = mmap(NULL, HEAP_SIZE*2, PROT_READ | PROT_WRITE,
		 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (bd_base == MAP_FAILED) {
    fprintf(stderr, "couldn't map heap; %s\n", strerror(errno));
    assert(bd_base);
  }
  
  char *p = bd_base;

  for (int k = 0; k < NSIZES; k++) {
    lst_init(&bd_sizes[k].free);
    int sz = sizeof(char)*ROUNDUP(NBLK(k), 16)/16;
    printf("bd: heap bd_init k %d, num of block: %d, sze: %d\n", k, NBLK(k), sz);
    bd_sizes[k].alloc = malloc(sz);
    memset(bd_sizes[k].alloc, 0, sz);
    p+=sz;
  }
  for (int k = 1; k < NSIZES; k++) {
    int sz = sizeof(char)*ROUNDUP(NBLK(k), 8)/8;
    bd_sizes[k].split = malloc(sz);
    memset(bd_sizes[k].split, 0, sz);
    p+=sz;
  }
  int using = p - (char*)bd_base;
  int roundup = ROUNDUP(using, LEAF_SIZE);
  printf("using %d, round up %d\n", using, roundup);
  p = bd_base + roundup; // p is current 7 bytes after bd_base, round up

  int meta = bd_mark_data_structures(p);

  //lst_push(&bd_sizes[MAXSIZE].free, bd_base);

  int free = bd_initfree(p, HEAP_SIZE + bd_base);
  int used = p - (char*)bd_base;
  int expected = HEAP_SIZE - used;
  printf("used %d. size of free: %d, expected %d\n", used, free, expected);
}

// What is the first k such that 2^k >= n?
int
firstk(size_t n) {
  int k = 0;
  size_t size = LEAF_SIZE;

  while (size < n) {
    k++;
    size *= 2;
  }
  return k;
}

// Compute the first block at size k that doesn't contain p
// (xp) I think this returns the block next to p's.
int
blk_index_next(int k, char *p) {
  int n = (p - (char *) bd_base) / BLK_SIZE(k);
  if((p - (char*) bd_base) % BLK_SIZE(k) != 0)
  {
    printf("Bump n %d for k(%d)\n", n, k);
    n++;
  }
      
  return n ;
}

// Compute the block index for address p at size k
int
blk_index(int k, char *p) {
  int n = p - (char *) bd_base;
  return n / BLK_SIZE(k);
}

int
blk_index_malloc(int k, char *p) {
  int n = p - (char *) bd_base;
  return n / BLK_SIZE(k) / 2;
}

void *
bd_malloc(size_t nbytes)
{
  int fk, k;
  
  assert(bd_base != NULL);

  // Find a free block >= nbytes, starting with smallest k possible
  fk = firstk(nbytes);
  for (k = fk; k < NSIZES; k++) {
    if(!lst_empty(&bd_sizes[k].free))
      break;
  }
  if(k >= NSIZES)  // No free blocks?
    return NULL;

  // Found one; pop it and potentially split it.
  char *p = lst_pop(&bd_sizes[k].free);
  flip_bit(bd_sizes[k].alloc, blk_index_malloc(k, p));
  for(; k > fk; k--) {
    char *q = p + BLK_SIZE(k-1);
    bit_set(bd_sizes[k].split, blk_index(k, p));
    flip_bit(bd_sizes[k-1].alloc, blk_index_malloc(k-1, p));
    lst_push(&bd_sizes[k-1].free, q);
  }
  // printf("malloc: %p size class %d\n", p, fk);
  return p;
}

// Find the size of the block that p points to.
int
size(char *p) {
  for (int k = 0; k < NSIZES; k++) {
    if(bit_isset(bd_sizes[k+1].split, blk_index(k+1, p))) {
      return k;
    }
  }
  return 0;
}

void
bd_free(void *p) {
  void *q;
  int k;
  
  for (k = size(p); k < MAXSIZE; k++) {
    int bi = blk_index_malloc(k, p);
    //printf("free index %d\n", bi);
    int buddy = (bi % 2 == 0) ? bi+1 : bi-1;
    flip_bit(bd_sizes[k].alloc, bi);
    if (bit_get(bd_sizes[k].alloc, bi)) {
      break;
    }
    // budy is free; merge with buddy
    q = addr(k, buddy);
    lst_remove(q);
    if(buddy % 2 == 0) {
      p = q;
    }
    bit_clear(bd_sizes[k+1].split, blk_index(k+1, p));
  }
  printf("free %p @ %d\n", p, k);
  lst_push(&bd_sizes[k].free, p);
}

// Implementation of lists: double-linked and circular. Double-linked
// makes remove fast. Circular simplifies code, because don't have to
// check for empty list in insert and remove.

void
lst_init(Bd_list *lst)
{
  lst->next = lst;
  lst->prev = lst;
}

int
lst_empty(Bd_list *lst) {
  return lst->next == lst;
}

void
lst_remove(Bd_list *e) {
  e->prev->next = e->next;
  e->next->prev = e->prev;
}

void*
lst_pop(Bd_list *lst) {
  assert(lst->next != lst);
  Bd_list *p = lst->next;
  lst_remove(p);
  return (void *)p;
}

void
lst_push(Bd_list *lst, void *p)
{
  Bd_list *e = (Bd_list *) p;
  e->next = lst->next;
  e->prev = lst;
  lst->next->prev = p;
  lst->next = e;
}

void
lst_print(Bd_list *lst)
{
  for (Bd_list *p = lst->next; p != lst; p = p->next) {
    printf(" %p", p);
  }
  printf("\n");
}


int
main(void)
{
  // set NSIZES to 4
  bd_init();
  bd_print();
}