#include <stdio.h>
/*
Write versions of the library functions strncpy, strncat, and strncmp, 
which operate on at most the first n characters of their argument strings.
For example, strncpy(s,t,n) copies at most n characters of t to s
*/
size_t my_min(size_t a, size_t b) {
  if (a < b) {
    return a;
  }
  return b;
}

size_t my_strlen(char *s) {
  char *p = s;
  while(*p != '\0') {
    p++;
  }
  return p - s;
}

char * my_strncpy(char *s, char *t, size_t n) {
  char * start = s;
  size_t t_len = my_min(my_strlen(t), n);
  //printf("Use length: %zu\n", my_strlen(t));

  size_t i = 0;
  while (i < t_len) {
    *s++ = *t++;
    //printf("%s\n", start);
    i++;
  }

  return start;
}

void test_strncpy() {
  char s[100];
  char t[100] = "pro";
  //printf("%zu\n", my_strlen("dialdial"));
  printf("Result %s\n", my_strncpy(s, t, 4));
}

int main(void) {
  test_strncpy();
  return 0;
}