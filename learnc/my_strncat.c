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

char * my_strncat(char *s, char *t, size_t n) {
  char * start = s;
  size_t t_len = my_min(my_strlen(t), n);
  while (*s) {
    s++;
  }
  int i = 0;
  for (; i < t_len; i++) {
    s[i] = t[i];
  }
  s[i] = '\0';
  return start;
}

void test_strncat() {
  char s[100] = "big xiaying is: ";
  char t[100] = "pro, and the best";
  printf("Result %s\n", my_strncat(s, t, 5));
}

int main(void) {
  test_strncat();
  return 0;
}