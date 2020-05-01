/*
Print error message, takes in multiple args.
*/

#include <stdio.h>
#include <stdarg.h>

void error(char *fmt, ...) {
  va_list args;
  va_start(args, fmt);
  fprintf(stderr, "error:");
  vfprintf(stderr, fmt, args);
  fprintf(stderr, "\n");
  va_end(args);

  //exit(1);
}

int main() {
  error("I am an %s", "error");
}

