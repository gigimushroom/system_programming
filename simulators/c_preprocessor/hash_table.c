// A hashtable stores symbol and its replacement text.
// A linked list is used for chaining values of same hash.
// Supported operations: Install, look up.
// Not thread-safe.

#include <string.h>
#include <stdlib.h>
#include <stdio.h>


struct nlist {
  struct nlist *next;
  char *name;
  char *defn;
};

typedef struct nlist* LISTPTR;

#define HASHSIZE 101

// pointer table
static struct nlist *hashtab[HASHSIZE];

unsigned hash(char *s) {
  unsigned hashval;
  for (hashval = 0; *s != 0; s++) {
    hashval = *s + 31 * hashval;
  }
  return hashval % HASHSIZE;
}

LISTPTR lookup(char *s) {
  //printf("DEBUG lookup: hashed val(%u), string(%s)\n", hash(s), s);

  LISTPTR np = hashtab[hash(s)];
  for (;np != NULL; np = np->next) {
    //printf("DEBUG: comparing %s to expected(%s)\n", np->name, s);
    if (strcmp(np->name, s) == 0) {
      return np;
    }
  }
  return NULL;
}

LISTPTR install(char *name, char *defn) {
  int hashval = hash(name);
  //printf("DEBUG install: hashed val(%u)\n", hashval);
  LISTPTR np = lookup(name);
  if (np == NULL) {
    // create a new non-existing node
    np = (LISTPTR)malloc(sizeof(*np));
    np->next = hashtab[hashval];
    hashtab[hashval] = np;
    np->name = strdup(name);
  } else {
    // replace old replacement string.
    free((void*) np->defn);
  }
  np->defn = strdup(defn);
  if (np->defn == NULL)
    return NULL;

  printf("Install C macro(%s:%s).\n", np->name, np->defn);
  return np;
}

void init() {
  for (int i=0; i<HASHSIZE; i++) {
    hashtab[i] = NULL;
  }
}

void simple_test() {
  printf("nlist size(%lu), LISTPTR size(%lu)\n", sizeof(struct nlist),
        sizeof(LISTPTR));
  install("xiaying", "best");
  install("mark", "worst");
  LISTPTR n = lookup("xiaying");
  printf("%s:%s\n", n->name, n->defn);
}

void parsing(char const* fileName) {
  FILE* f = fopen(fileName, "r");
  char line[256];
  int i = 0;
  while (fgets(line, sizeof(line), f)) {
    //printf("%s", line);
    char *pch;
    pch = strtok(line, " \n");
    if (pch != NULL && strcmp(pch, "#define") == 0) {
      char *k, *v;
      k = strtok(NULL, " \n");
      if (k != NULL)
        v = strtok(NULL, " \n");
      
      if (k == NULL || v == NULL) {
        printf("Error parsing define line(%s) at line no(%d)\n", line, i);
      }
      install(k, v);
    }
    i++;
  }

  fclose(f);
}

void code_gen(const char* input, const char* output) {
  FILE* f = fopen(input, "r");
  char line[256];

  FILE *out = fopen(output, "ab"); // OUTPUT FILE append only.
  while (fgets(line, sizeof(line), f)) {
    char cp[256] = "";
    char *pch;
    pch = strtok(line, " \n;");
    int filled = 0;
    while (pch != NULL) {
      // Skip #define ones.
      if (strcmp(pch, "#define") == 0) {
        break;
      }
      LISTPTR n = lookup(pch);
      if (n != NULL) {
        //printf("Found pair(%s:%s)\n", n->name, n->defn);
        strcat(cp, n->defn);
      } else {
        strcat(cp, pch);
      }
      pch = strtok (NULL, " \n;");
      
      if (pch != NULL)
        strcat(cp, " ");
      filled = 1;
    }

    if (filled == 1) {
      // Proper end the line.
      if (strrchr(cp, '}') || strrchr(cp, '{') || strrchr(cp, '>')) {
        strcat(cp, "\n");
      } else {
        strcat(cp, ";\n");
      }
      
      //printf("Output: %s", cp);
      fputs(cp, out);
    }
  }
  fclose(f);

}

int main(int argc, char* argv[]) {
  printf("\nInput file(%s), output file(%s)\n", argv[1], argv[2]);
  printf("...Parsing....\n");
  parsing(argv[1]);
  printf("...Code generation begins....\n");
  code_gen(argv[1], argv[2]);
  
  return 0;
}


