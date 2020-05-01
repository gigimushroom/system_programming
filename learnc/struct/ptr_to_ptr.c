#include <stdio.h>
#include <string.h>
/*
Knowledge 1:
The generic pointer type void * is used for the pointer arguments. 
Any pointer can be cast to void * and back again 
without loss of information, 
so we can call foo by casting arguments to void *.

Knowledge 2:
Example 1:
char ** a;
a: pointer to pointer to char

Example 2:
int *b[10]
array[10] of pointers to int
*/

// Array of char pointers
// similar to char **lineptr
char *lineptr[10];

char *normal_ptr;

// foo() requires an array of void pointers.
void foo(void *lineptr[]) {
  printf("%s\n", lineptr[0]);
}

// bar() requires a normal void casted ptr.
void bar(void *normal_ptr) {
  printf("%s\n", normal_ptr);
}

int main(void) {
  lineptr[0] = "first word";
  // Cast lineptr to array of void pointers
  foo((void **) lineptr);

  // cast a char ptr to void ptr.
  normal_ptr = "mushroom";
  bar((void*)normal_ptr);

  return 0;
}

/*
Summary


*/