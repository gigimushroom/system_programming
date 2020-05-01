#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#define BUFSIZE 1024

/* 
 * error - wrapper for perror
 */
void error(char *msg) {
    perror(msg);
    exit(0);
}

struct sockaddr_in prepare_sock_addr(int portno, char *hostname) {
  struct sockaddr_in serveraddr;
  struct hostent *server;

  /* gethostbyname: get the server's DNS entry */
  server = gethostbyname(hostname);
  if (server == NULL) {
      fprintf(stderr,"ERROR, no such host as %s\n", hostname);
      exit(0);
  }

  /* build the server's Internet address */
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  bcopy((char *)server->h_addr, 
  (char *)&serveraddr.sin_addr.s_addr, server->h_length);
  serveraddr.sin_port = htons(portno);

  return serveraddr;
}

void cli_send_request(struct sockaddr_in serveraddr) {
  /* socket: create the socket */
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) 
      error("ERROR opening socket");

  /* connect: create a connection with the server */
  if (connect(sockfd, &serveraddr, sizeof(serveraddr)) < 0) 
    error("ERROR connecting");

  /* get message line from the user */
  char buf[BUFSIZE];
  printf("Please enter msg: ");
  bzero(buf, BUFSIZE);
  fgets(buf, BUFSIZE, stdin);

  /* send the message line to the server */
  int n = write(sockfd, buf, strlen(buf));
  if (n < 0) 
    error("ERROR writing to socket");

  /* print the server's reply */
  bzero(buf, BUFSIZE);
  n = read(sockfd, buf, BUFSIZE);
  if (n < 0) 
    error("ERROR reading from socket");
  printf("Echo from server: %s", buf);
  close(sockfd);
}

void client_special_request(struct sockaddr_in serveraddr) {
  /* socket: create the socket */
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) 
      error("ERROR opening socket");

  /* connect: create a connection with the server */
  if (connect(sockfd, &serveraddr, sizeof(serveraddr)) < 0) 
    error("ERROR connecting");

  /* get message line from the user */
  char *text = "This is from client!\n";

  /* send the message line to the server */
  int n = write(sockfd, text, strlen(text));
  if (n < 0) 
    error("ERROR writing to socket");

  //printf("Wrote to server: %s", text);

  /* print the server's reply */
  char buf[BUFSIZE];
  bzero(buf, BUFSIZE);
  n = read(sockfd, buf, BUFSIZE);
  if (n < 0) 
    error("ERROR reading from socket");
  printf("Echo from server: %s", buf);
  close(sockfd);
}