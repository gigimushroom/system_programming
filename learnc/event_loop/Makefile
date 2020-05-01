CC = gcc

all: tcpserver tcpclient manyclients selectserver epollserver chatserver

tcpserver: tcp_server.c
	gcc -o tcpserver tcp_server.c

selectserver: select_server.c
	gcc -o selectserver select_server.c

epollserver: epoll_server.c
	gcc -o epollserver epoll_server.c

tcpclient: sock_helper.h tcp_client.c
	gcc -o tcpclient tcp_client.c

manyclients: sock_helper.h concurrent_client.c
	gcc -o manyclients -lpthread concurrent_client.c

chatserver: chat_server.c
	gcc -g -o chatserver chat_server.c

clean:
	rm -f *.o tcpserver tcpclient manyclients selectserver epollserver chatserver