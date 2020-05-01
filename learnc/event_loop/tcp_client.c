/* 
 * tcpclient.c - A simple TCP client
 * usage: tcpclient <host> <port>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sock_helper.h"


int main(int argc, char **argv) {
    int portno;
    struct sockaddr_in serveraddr;
    
    char *hostname;

    /* check command line arguments */
    if (argc != 3) {
       fprintf(stderr,"usage: %s <hostname> <port>\n", argv[0]);
       exit(0);
    }
    hostname = argv[1];
    portno = atoi(argv[2]);

    serveraddr = prepare_sock_addr(portno, hostname);
    cli_send_request(serveraddr);

    return 0;
}
