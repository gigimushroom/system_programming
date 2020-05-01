
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/event.h>
#include <pthread.h>


#define BUFSIZE 1024
#define NAMESIZE 20
#define MAX_NUM_CLIENTS 50
#define MAX_NUM_IN_ROOM 10
#define MAX_ROOM 2

#define SIGNUP 0
#define ACTIVE 1
#define INACTIVE 2

typedef struct client {
  int uuid; //fd
  char role[NAMESIZE];
  char name[NAMESIZE];
  int state;
  int room; // room index.
} client_t;

client_t *clients[MAX_NUM_CLIENTS];

typedef struct chatroom {
  int cli_uuids[MAX_NUM_IN_ROOM]; // the global client index.
  int size;
} chat_room;

static chat_room rooms[MAX_ROOM];

pthread_mutex_t _mutex = PTHREAD_MUTEX_INITIALIZER;

void error(char *msg) {
  perror(msg);
  exit(1);
}

void print_room() {
  printf("...........PRINTING ROOMS INFO.......\n");
  for (int i=0; i<MAX_ROOM; i++) {
    for (int j=0; j< MAX_NUM_IN_ROOM; j++) {
      if (rooms[i].cli_uuids[j] != -1) {
        printf("Room (%d) has user id(%d)\n", i, rooms[i].cli_uuids[j]);
      }
    }
  }
  printf(".....................................\n");
}

int count_active_clients() {
  int num = 0;
  //pthread_mutex_lock(&_mutex);
  for (int i=0; i< MAX_NUM_CLIENTS; i++) {
    if (clients[i]) {
      num++;
    }
  }
  //pthread_mutex_unlock(&_mutex);
  return num;
}

int find_client_index_by_fd(int fd) {
  int result = -1;
  pthread_mutex_lock(&_mutex);
  for (int i=0; i< MAX_NUM_CLIENTS; i++) {
    if (clients[i] && clients[i]->uuid == fd) {
      result = i;
      break;
    }
  }
  pthread_mutex_unlock(&_mutex);
  return result;
}

void broadcast_msg(int from_fd, int chatroom, char* msg) {
  int idx = find_client_index_by_fd(from_fd);
  int room_idx = clients[idx]->room;
  printf("Client(%d) %s wants to send a broadcast msg to chat room(%d).\n", 
         idx, clients[idx]->name, room_idx);

  chat_room* room = &rooms[room_idx];
  for (int i=0; i< MAX_NUM_IN_ROOM; i++) {
    int uuid = room->cli_uuids[i];
    
    if (uuid == -1)
      continue;
      
    if (uuid == from_fd)
      continue;

    // send msg to others.
    char buf[100];
    sprintf(buf, "%s: %s", clients[idx]->name, msg);
    int n = write(uuid, buf, strlen(buf));
    if (n < 0) {
      printf("ERROR broadcast to %d", uuid);
      error("broadcast err.");
    }
    //printf("DEBUG: user(%s) sends msg to %d at room(%d)\n", clients[idx]->name, uuid, room_idx);
  }
}

void register_client(int fd) {
  int index = -1;
  int room_idx = -1;
  pthread_mutex_lock(&_mutex);
  for (int i=0; i< MAX_NUM_CLIENTS; i++) {
    if (!clients[i]) {
      clients[i] = (client_t*)malloc(sizeof(client_t));
      clients[i]->state = 1;
      clients[i]->uuid = fd;
      room_idx = (i+1) % MAX_ROOM;
      clients[i]->room = room_idx;
      // save fd as name by default.
      sprintf(clients[i]->name, "%d", fd);
      index = i;
      break;
    }
  }
  pthread_mutex_unlock(&_mutex);

  if (index == -1 || room_idx == -1) {
    error("Error assign user to chat room!");
  }

  chat_room* room = &rooms[room_idx];
  printf("DEBUG: ......User(%d) fd(%d) logs in room (%d)\n", index, fd, room_idx);
  for (int i=0; i < MAX_NUM_IN_ROOM; i++) {
    if (room->cli_uuids[i] == -1) {
      room->cli_uuids[i] = fd;
      return;
    }
  }
}

void client_rename(char* name, int childfd) {
  int index = find_client_index_by_fd(childfd);
  pthread_mutex_lock(&_mutex);
  strncpy(clients[index]->name, name, strlen(name));
  clients[index]->name[strlen(name)]=0;
  pthread_mutex_unlock(&_mutex);
}

int validate_cmd(char *buf) {
  // If cmd is name, we enforce format: '/name <NICK_NAME>/'.
  // Dont care other cmds.
  char *sym = strstr(buf, "name");
  if (sym == NULL) {
    return 1;
  }
  sym = strchr(buf+1, '/');
  if (sym == NULL) {
    printf("The command sytax is: /<CMD> <ARGS>/. You have %s\n", buf);
    return 0;
  }
  return 1;
}

void *handle_connection(void *fd) {
  int n; /* message byte size */
  char buf[BUFSIZE]; /* message buffer */

  int childfd = (int)fd;

  while(1) {
    bzero(buf, BUFSIZE);
    n = read(childfd, buf, BUFSIZE);
    if (n < 0) 
      error("ERROR reading from socket");
    printf("server received %d bytes: %s", n, buf);
    
    if (buf[0] == '/') {
      if (!validate_cmd(buf)) {
        continue;
      }
      // special options
      char *cmd, *param;
      cmd = strtok(buf, " ");
      if (strcmp(cmd, "/name") == 0) {
        // change nick name.
        param = strtok(NULL, "/");
        char *p = strdup(param);
        int len = strlen(p);
        printf("User wants to change name to %s. Length %d\n", p, len);
        client_rename(p, childfd);
      } else if (strstr(cmd, "/quit") != NULL) {
        break;
      } else if (strstr(cmd, "/help") != NULL) {
        char buff_out[500];
        strcat(buff_out, "<< /quit     Quit chatroom\r\n");
        //strcat(buff_out, "<< /ping     Server test\r\n");
        //strcat(buff_out, "<< /topic    <message> Set chat topic\r\n");
        strcat(buff_out, "<< /name     <name>/ Change nickname\r\n");
        strcat(buff_out, "<< /room     <room>/ Change chat room\r\n");
        //strcat(buff_out, "<< /msg      <reference> <message> Send private message\r\n");
        strcat(buff_out, "<< /list     Show active clients\r\n");
        strcat(buff_out, "<< /help     Show help\r\n");
        write(childfd, buff_out, strlen(buff_out));
      } else if (strstr(cmd, "/list") != NULL) {
        char buff_out[100];
        int num = count_active_clients();
        sprintf(buff_out, "Total number of clients in your chatroom: %d.\n", num);
        write(childfd, buff_out, strlen(buff_out));
      } else if (strstr(cmd, "/room") != NULL) {
        // change room.
        printf("User wants to change chat room.\n");
        print_room();
      }
    } else {
      broadcast_msg(childfd, 0, buf);
    }
  }
  close(childfd);
  int rm_index = find_client_index_by_fd(childfd);
  free(clients[rm_index]);
  clients[rm_index] = NULL;
  printf("Close client %d connection.\n", childfd);

  return 0;
}


void _init_clients() {
  for (int i=0; i< MAX_NUM_CLIENTS; i++) {
    clients[i] = NULL;
  }
}

void _init_rooms() {
  for (int i=0; i<MAX_ROOM; i++) {
    rooms[i].size = 0;
    for (int j=0; j< MAX_NUM_IN_ROOM; j++) {
      rooms[i].cli_uuids[j] = -1;
    }
  }
}

size_t wait_client_to_join(int parentfd) {
  // wait for a connection request, echo input line, then close connection.
  struct hostent *hostp; /* client host info */
  char *hostaddrp; /* dotted decimal host addr string */
  size_t childfd; /* child socket */
  
  struct sockaddr_in clientaddr; /* client addr */

  socklen_t clientlen = sizeof(clientaddr);

  childfd = accept(parentfd, (struct sockaddr *) &clientaddr, &clientlen);
  if (childfd < 0) 
    error("ERROR on accept");
  
  hostp = gethostbyaddr((const char *)&clientaddr.sin_addr.s_addr, 
      sizeof(clientaddr.sin_addr.s_addr), AF_INET);
  if (hostp == NULL)
    error("ERROR on gethostbyaddr");
  hostaddrp = inet_ntoa(clientaddr.sin_addr);
  if (hostaddrp == NULL)
    error("ERROR on inet_ntoa\n");
  printf("server established connection with %s (%s)\n", 
  hostp->h_name, hostaddrp);

  return childfd;
}

int main(int argc, char **argv) {
  int parentfd; /* parent socket */
  int portno; /* port to listen on */
  struct sockaddr_in serveraddr; /* server's addr */
  int optval; /* flag value for setsockopt */

  pthread_t tid;

  if (argc != 2) {
    fprintf(stderr, "usage: %s <port>\n", argv[0]);
    exit(1);
  }
  portno = atoi(argv[1]);
  portno = 5555;

  parentfd = socket(AF_INET, SOCK_STREAM, 0);
  if (parentfd < 0) 
    error("ERROR opening socket");

  optval = 1;
  setsockopt(parentfd, SOL_SOCKET, SO_REUSEADDR, 
	     (const void *)&optval , sizeof(int));

  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  serveraddr.sin_port = htons((unsigned short)portno);

  if (bind(parentfd, (struct sockaddr *) &serveraddr, 
	   sizeof(serveraddr)) < 0) 
    error("ERROR on binding");

  if (listen(parentfd, 5) < 0) /* allow 5 requests to queue up */ 
    error("ERROR on listen");

  _init_clients();
  _init_rooms();

  int kq = kqueue();
  struct kevent ev_set;
  EV_SET(&ev_set, parentfd, EVFILT_READ, EV_ADD, 0, 0, NULL);

  struct kevent evList[32];

  while (1) {
    printf("waiting for client to connect me...\n");
    
    int nev = kevent(kq, &ev_set, 1, evList, 32, NULL);
    for (int i=0; i<nev; i++) {
      if (evList[i].ident != parentfd) {
        continue;
      }

      size_t childfd = wait_client_to_join(parentfd);

      register_client(childfd);

      pthread_create(&tid, NULL, &handle_connection, (void*)childfd);
    }
  }
}