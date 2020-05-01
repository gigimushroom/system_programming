#include <stdio.h>
#include <stdlib.h>
#include <execinfo.h>
#include <pthread.h>


#define BT_BUF_SIZE 100

void bt() {
  int j, nptrs;
  void *buffer[BT_BUF_SIZE];
  char **strings;

  nptrs = backtrace(buffer, BT_BUF_SIZE);
  printf("backtrace() returned %d addresses\n", nptrs);

  strings = backtrace_symbols(buffer, nptrs);
  for (j = 0; j < nptrs; j++)
    printf("%s\n", strings[j]);
}

typedef struct _node {
  int val;
  struct _node *next;
} node;

typedef struct _list {
  node *head;
  pthread_mutex_t lock;
} list_t;

list_t *l;

void list_init() {
  l = (list_t*)malloc(sizeof(list_t));
  l->head = NULL;
  pthread_mutex_init(&l->lock, NULL);
}

void list_insert(int val) {
  node *n = (node*)malloc(sizeof(node*));
  n->val = val;
  //printf("Insert val %d\n", val);
  if (l->head == NULL) {
    l->head = n;
    return;
  }

  pthread_mutex_lock(&l->lock);
  n->next = l->head;
  l->head = n;
  pthread_mutex_unlock(&l->lock);
}

int list_search(int val) {
  node *p = l->head;
  while(p) {
    if (p->val == val) {
      return 1;
    }
    p = p->next;
  }
  return 0;
}

int list_delete(int val) {
  node *p = l->head;
  if (!p) {
    return 0;
  }
  if (p->val == val) {
    l->head = p->next;
    return 1;
  }

  while(p && p->next) {
    if (p->next->val == val) {
      p->next = p->next->next;
      return 1;
    }
    p = p->next;
  }
  return 0;
}

void list_dump() {
  node *p = l->head;
  printf("Dumping list:");
  while(p) {
    printf(" %d", p->val);
    p = p->next;
  }
  printf("\n");
}

int list_size() {
  int size = 0;
  node *p = l->head;
  while(p) {
    size++;
    p = p->next;
  }
  return size;
}

void _test_help(int v, int expected) {
  if (v != expected) {
    printf("ERROR: get %d, expected: %d\n", v, expected);
    bt();
  }
}

int main() {
  list_init();

  list_insert(3);
  list_insert(4);
  list_insert(5);

  _test_help(list_size(), 3);
  _test_help(list_search(3), 1);
  _test_help(list_search(6), 0);

  list_delete(5);
  _test_help(list_size(), 2);

  list_delete(3);
  list_delete(4);
  _test_help(list_size(), 0);
  return 0;
}