#include<stdio.h>
#include<string.h>

char whitespace[] = " \t\r\n\v";
char symbols[] = "<|>&;()";

int
gettoken(char **ps, char *es, char **q, char **eq)
{
  char *s;
  int ret;

  s = *ps;
  while(s < es && strchr(whitespace, *s))
    s++;
  if(q)
    *q = s;
  ret = *s;
  switch(*s){
  case 0:
    break;
  case '|':
  case '(':
  case ')':
  case ';':
  case '&':
  case '<':
    s++;
    break;
  case '>':
    s++;
    if(*s == '>'){
      ret = '+';
      s++;
    }
    break;
  default:
    ret = 'a';
    while(s < es && !strchr(whitespace, *s) && !strchr(symbols, *s))
      s++;
    break;
  }
  if(eq)
    *eq = s;

  while(s < es && strchr(whitespace, *s))
    s++;
  *ps = s;
  return ret;
}

int main(void) {
  char *argv[10];
  char *eargv[10];

  char buf[100] = "ls xiaying | wc";
  char *s = buf;
  char *q, *eq;
  char *es = s + strlen(s);
  int i = 0;
  while (gettoken(&s, es, &q, &eq) != '\0') {
    printf ("(%s)(%s)(%s)\n", s, q, eq);
    argv[i] = q;
    eargv[i] = eq;
    i++;
  }
  for(int k=0; k<i; k++)
    *eargv[k] = 0;

  for (int j=0; j<i; j++) {
    printf ("Done. (%s)(%s)\n", argv[j], eargv[j]);
  }
}
