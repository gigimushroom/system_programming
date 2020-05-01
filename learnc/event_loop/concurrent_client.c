#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "sock_helper.h"

void *fire_request( void *ptr );

int main(void)
{
  pthread_t thread1, thread2, thread3;
  char *message1 = "Thread 1";
  char *message2 = "Thread 2";
  char *message3 = "Thread 3";

/* Create independent threads each of which will execute function */

  pthread_create( &thread1, NULL, fire_request, (void*) message1);
  pthread_create( &thread2, NULL, fire_request, (void*) message2);
  pthread_create( &thread3, NULL, fire_request, (void*) message3);

  /* Wait till threads are complete before main continues. Unless we  */
  /* wait we run the risk of executing an exit which will terminate   */
  /* the process and all threads before the threads have completed.   */

  pthread_join( thread1, NULL);
  pthread_join( thread2, NULL); 
  pthread_join( thread3, NULL); 

  return 0;
}

void *fire_request( void *ptr )
{
  char *hostname = "localhost";
  int portno = 5555;
  
  struct sockaddr_in serveraddr = prepare_sock_addr(portno, hostname);
  client_special_request(serveraddr);

  char *message = (char *) ptr;
  printf("%s is done.\n", message);

  return NULL;
}
