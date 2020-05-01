#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
  char s[100] = "/name wwa";
  char *cmd, *param;
  cmd = strtok(s, " ");
  printf("%s\n", cmd);
  if (strcmp(cmd, "/name") == 0) {
    param = strtok(NULL, " ");

    char *p = strdup(param);
    printf("Changed name to %s. Length %lu\n", p, strlen(p));
  }

}