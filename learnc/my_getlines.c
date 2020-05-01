#include <stdio.h>

int my_getline(char *s, int limit) {
  //char buf[100];
  //printf("Output: %s\n", my_getline(buf, 10));
  char *p = s;
  char c;
  int size = 0;
  while (limit - 1 > 0 && ((c = getchar()) != EOF && c != '\n')) {
    //printf("entering... %c, %d\n", c, limit);
    *s++ = c;
    limit--;
    size++;
  }
  if (c == '\n') {
    *s++ = '\n';
    size++;
  }

  *s = '\0';
  return size;
}

#define MAXLINES 5000     /* max #lines to be sorted */
char *lineptr[MAXLINES];  /* pointers to text lines */

#define ALLOCSIZE 10000  /* size of available space */
char allocation[ALLOCSIZE];
char *next_free = allocation;

char* allocate_mem(int n) {
  if (allocation + ALLOCSIZE - next_free < n) {
    return 0;
  }
  char *p = next_free;
  next_free+=n;
  return p;
}

int readlines(char *lineptr[], int maxlines) {
  char buf[100];
  int nlines = 0;
  int num = 0;
  char *p;
  while (num = my_getline(buf, 100) > 0) {
    if (nlines >= maxlines) {
      return -1;
    }
    p = allocate_mem(100);
    strcpy(p, buf);
    *lineptr++ = p;
    nlines++;
  }
  return nlines;
}

void writelines(char *l[], int nlines) {
  for (int i = 0; i < nlines; i++) {
    printf("%s", l[i]);
  }
}

void swap(char *v[],int i,int j)
{
  char *temp;
  temp=v[i];
  v[i]=v[j];
  v[j]=temp;
}

void qsort(char *v[],int left,int right) {
  if (left >= right) {
    return;
  }
  swap(v, left, (left+right)/2);
  int last = left;
  for (int i=left+1; i <= right; i++) {
    if (strcmp(v[i], v[left]) < 0) {
      // Move the un-sure (last+1)'s val away. So new last has element
      // less than v[left].
      swap(v, i, ++last);
    }
  }
  swap(v, left, last);
  qsort(v, left, last - 1);
  qsort(v, last + 1, right);
}

int main(void) {
  int n = readlines(lineptr, 100);
  qsort(lineptr, 0, n - 1);
  writelines(lineptr, n);

  return 0;
}