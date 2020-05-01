#include <stdio.h>
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>


void handler(int sig) {
  void *array[10];
  size_t size;

  // get void*'s for all entries on the stack
  size = backtrace(array, 10);

  // print out all the frames to stderr
  fprintf(stderr, "Error: signal %d:\n", sig);
  backtrace_symbols_fd(array, size, STDERR_FILENO);
  exit(1);
}


typedef struct client {
  int uuid; //fd
  int room; // room index.
} client_t;

client_t *clients[10];

typedef struct chatroom {
  client_t *clients[5]; // the global client index.
  int size;
} chat_room;

chat_room *rooms[2];


int main() {

  signal(SIGSEGV, handler);

  for (int i=0; i< 10; i++) {
    if (!clients[i]) {
      clients[i] = (client_t*)malloc(sizeof(client_t));
      clients[i]->uuid = i;
      clients[i]->room = (i+1) % 2;;
    }
  }

  for (int i=0; i<2; i++) {
    rooms[i] = (chat_room*)malloc(sizeof(chat_room));
    rooms[i]->size = 0;
    for (int j=0; j< 5; j++) {
      rooms[i]->clients[j] = NULL;
    }
  }

  if (!rooms[0]->clients[0])
    rooms[0]->clients[0] = clients[0];

  if (!rooms[1]->clients[0])
    rooms[1]->clients[0] = clients[1];

  if (!rooms[1]->clients[1])
    rooms[1]->clients[1] = clients[2];


  printf("...........PRINTING ROOMS INFO.......\n");
  for (int i=0; i<2; i++) {
    for (int j=0; j< 5; j++) {
      if (rooms[i]->clients[j]) {
        printf("Room (%d) has user id(%d)\n", i, rooms[i]->clients[j]->uuid);
      }
    }
  }
  printf(".....................................\n");
  

  return 0;
}