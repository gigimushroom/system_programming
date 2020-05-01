#include <stdio.h>

size_t my_strlen(char *s) {
  char *p = s;
  while(*p != '\0') {
    p++;
  }
  return p - s;
}

int main(void) {
  size_t (*f)(void *) = (size_t (*)(void *))(my_strlen);

  printf("%zu\n", (*f)("xiaying is pro"));
  return 0;
}