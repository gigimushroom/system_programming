/* 
 * tcpserver.c - A simple TCP echo server 
 * usage: tcpserver <port>
 */

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

#define BUFSIZE 1024

/*
 * error - wrapper for perror
 */
void error(char *msg) {
  perror(msg);
  exit(1);
}

void handle_connection(int parentfd, struct sockaddr_in serveraddr) {
  // wait for a connection request, echo input line, then close connection.
  struct hostent *hostp; /* client host info */
  char *hostaddrp; /* dotted decimal host addr string */
  int childfd; /* child socket */
  int n; /* message byte size */
  char buf[BUFSIZE]; /* message buffer */
  struct sockaddr_in clientaddr; /* client addr */

  socklen_t clientlen = sizeof(clientaddr);

  /* 
  * accept: wait for a connection request 
  */
  childfd = accept(parentfd, (struct sockaddr *) &clientaddr, &clientlen);
  if (childfd < 0) 
    error("ERROR on accept");
  
  /* 
  * gethostbyaddr: determine who sent the message 
  */
  hostp = gethostbyaddr((const char *)&clientaddr.sin_addr.s_addr, 
      sizeof(clientaddr.sin_addr.s_addr), AF_INET);
  if (hostp == NULL)
    error("ERROR on gethostbyaddr");
  hostaddrp = inet_ntoa(clientaddr.sin_addr);
  if (hostaddrp == NULL)
    error("ERROR on inet_ntoa\n");
  printf("server established connection with %s (%s)\n", 
  hostp->h_name, hostaddrp);
  
  /* 
  * read: read input string from the client
  */
  bzero(buf, BUFSIZE);
  n = read(childfd, buf, BUFSIZE);
  if (n < 0) 
    error("ERROR reading from socket");
  printf("server received %d bytes: %s", n, buf);
  
  /* 
  * write: echo the input string back to the client 
  */
  n = write(childfd, buf, strlen(buf));
  if (n < 0) 
    error("ERROR writing to socket");

  close(childfd);
}

int main(int argc, char **argv) {
  int parentfd; /* parent socket */
  int portno; /* port to listen on */
  struct sockaddr_in serveraddr; /* server's addr */
  int optval; /* flag value for setsockopt */

  /* 
   * check command line arguments 
   */
  if (argc != 2) {
    fprintf(stderr, "usage: %s <port>\n", argv[0]);
    exit(1);
  }
  portno = atoi(argv[1]);

  /* 
   * socket: create the parent socket 
   */
  parentfd = socket(AF_INET, SOCK_STREAM, 0);
  if (parentfd < 0) 
    error("ERROR opening socket");

  /* setsockopt: Handy debugging trick that lets 
   * us rerun the server immediately after we kill it; 
   * otherwise we have to wait about 20 secs. 
   * Eliminates "ERROR on binding: Address already in use" error. 
   */
  optval = 1;
  setsockopt(parentfd, SOL_SOCKET, SO_REUSEADDR, 
	     (const void *)&optval , sizeof(int));

  /*
   * build the server's Internet address
   */
  bzero((char *) &serveraddr, sizeof(serveraddr));

  /* this is an Internet address */
  serveraddr.sin_family = AF_INET;

  /* let the system figure out our IP address */
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);

  /* this is the port we will listen on */
  serveraddr.sin_port = htons((unsigned short)portno);

  /* 
   * bind: associate the parent socket with a port 
   */
  if (bind(parentfd, (struct sockaddr *) &serveraddr, 
	   sizeof(serveraddr)) < 0) 
    error("ERROR on binding");

  /* 
   * listen: make this socket ready to accept connection requests 
   */
  if (listen(parentfd, 5) < 0) /* allow 5 requests to queue up */ 
    error("ERROR on listen");

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
      handle_connection(parentfd, serveraddr);
    }
  }
}