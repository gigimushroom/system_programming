#include <stdio.h>

/*
Write the function strend(s,t), 
which returns 1 if the string t occurs at the end of the string s, 
and zero otherwise
*/
int my_strend(char *s, char *t) {
  char * left = s;
  char * right = t;
  int s_size = 0;
  while(*s != '\0') {
    s_size++;
    s++;
  }
  int t_size = 0;
  while (*t != '\0') {
    t_size++;
    t++;
  }
  //printf("s(%d) t(%d)\n", s_size, t_size);
  int i = 0;
  while (left[s_size-i] == right[t_size-i] && t_size-i >= 0)
  {
    //printf("%d, %d %c\n", i, t_size-i, right[t_size-i]);
    if (t_size-i == 0) {
      return 1;
    }
    i++;
  }
  return 0;
}

int main(void) {
  char s[100] = "xiaying is: ";
  char t[100] = "pro";
  printf("Result is: %d\n", my_strend(s, t));

  char d[100] = "xiaying is: ";
  printf("Result is: %d\n", my_strend(s, d));
  return 0;
}