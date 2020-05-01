#include <stdio.h>

char * my_strcat(char *s, char *t) {
  char *p = s;
  // iterate s to the end
  while (*s) {
    s++;
  }
  // append t to s
  int i = 0;
  for (; t[i] != '\0'; i++) {
    s[i] = t[i];
  }
  s[i] = '\0';
  // return s head
  return p;
}

int main(void) {
  char s[100] = "xiaying is: ";
  char t[100] = "pro";

  printf("%s\n", my_strcat(s, t));

  return 0;
}