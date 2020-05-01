#include <stdio.h>
#include <stdlib.h>


typedef struct client {
  int uuid; //fd
  int room; // room index.
} client_t;

client_t *clients[10];

typedef struct chatroom {
  client_t *clients[5]; // the global client index.
  int size;
} chat_room;

chat_room rooms[2];


int main() {

  for (int i=0; i< 10; i++) {
    if (!clients[i]) {
      clients[i] = (client_t*)malloc(sizeof(client_t));
      clients[i]->uuid = i;
      clients[i]->room = (i+1) % 2;;
    }
  }

  for (int i=0; i<2; i++) {
    rooms[i].size = 0;
    for (int j=0; j< 5; j++) {
      rooms[i].clients[j] = NULL;
    }
  }

  rooms[0].clients[0] = clients[0];
  rooms[1].clients[0] = clients[1];
  rooms[1].clients[1] = clients[2];


  printf("...........PRINTING ROOMS INFO.......\n");
  for (int i=0; i<2; i++) {
    for (int j=0; j< 5; j++) {
      if (rooms[i].clients[j]) {
        printf("Room (%d) has user id(%d)\n", i, rooms[i].clients[j]->uuid);
      }
    }
  }
  printf(".....................................\n");
  

  return 0;
}