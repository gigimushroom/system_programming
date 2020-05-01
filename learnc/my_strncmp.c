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

int my_strncmp(char *s, char *t, size_t n) {
  size_t t_len = my_min(my_strlen(t), n);
  
  int i = 0;
  for(; *s == *t && i < t_len; s++, t++) {
    if (*s == '\0') {
      return 0; // return 0 if s[i] == s[t] == EOF
    }
  }
  //printf("%c - %c\n", *s, *t);
  return *s - *t; 
}

void test() {
  char s[100] = "aaabbaaaaa";
  char t[100] = "aaabcaaaba";
  printf("Result %d\n", my_strncmp(s, t, 5));

  char d[100] = "aaaaaaaaca";
  printf("Result %d\n", my_strncmp(s, d, 30));

  printf("Result %d\n", my_strncmp(s, s, 30));
}

int main(void) {
  test();
  return 0;
}