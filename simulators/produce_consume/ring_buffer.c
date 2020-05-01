/*
A single ring buffer producer/consumer solution.
Producer waits for EMPTY condition if buffer is full. Signal FILL after put.
Consumer waits for FILL condition if buffer is empty. Signal empty after pop.

Key 1
As stated in http://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf
It is industry standard to have 2 condition variables: one for produce, one for consume.

If both of them shares the same condition var, it is likely causing deadlock.
Example:
1. Consumer A, Consumer B sleep waiting for data.
2. Producer A comes in, fill all buckets, and sleep.
3. Consumer A wakes up, consumed all data, and try to signal Producer A.
4. Bad: Consumer B wakes up, instead of Producer A. Nothing to consumer, back to sleep.
5. Now we have 3 threads are sleeping forever.

Key 2
Use 'while' for sleep, instead of 'if'.
Thread could be waken up and still not satisfy the condition, it needs to sleep again.
Example: 
Producer A sleeps when buffer is full.
Consumer B consumes 1, and wake up A.
A is scheduled to be waken up.
Before CPU schedules it, producer B comes up, and fill the buffer to full again.
CPU runs producer A, and A found out ring buffer again is full.
At this point, A needs to go back to sleep.
*/

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>


#define BUCKET_SIZE 16
#define MSG_LENGTH 30

struct bucket {
  int uuid;
  char msg[MSG_LENGTH];
};

static struct bucket* ring_buf[BUCKET_SIZE];

volatile int header, tail;

volatile int uuid; // global uuid
volatile int count;

// locks
pthread_mutex_t lock;
pthread_cond_t empty, fill;
pthread_t tid[3];

void init();
void produce(char *msg);
void consume();

void init() {
  pthread_mutex_init(&lock, NULL);
  pthread_cond_init(&empty, NULL);
  pthread_cond_init(&fill, NULL);

  count = uuid = 0;
  for (int i=0; i<BUCKET_SIZE; i++) {
    ring_buf[i] = NULL;
  }
  header = tail = 0;
}

void produce(char *msg) {
  pthread_mutex_lock(&lock);

  __sync_synchronize();
  while (count == BUCKET_SIZE) {
    // buffer full
    printf("Ring buffer is full!\n");
    pthread_cond_wait(&empty, &lock);
  }

  struct bucket *buffer = (struct bucket*)malloc(sizeof(struct bucket));
  __sync_fetch_and_add(&uuid, 1);
  buffer->uuid = uuid;
  memcpy(buffer->msg, msg, strlen(msg));
  
  // insert to ring buffer.
  __sync_synchronize();

  if (ring_buf[tail] != NULL) {
    printf("Try to insert to existing bucket! Counter(%d) header(%d) tail(%d)\n",
          count, header, tail);
  }


  ring_buf[tail] = buffer;
  tail = (tail+1) % BUCKET_SIZE;

  printf("Produced: Bucket id(%d) content(%s). Header(%d), tail(%d)\n", 
          buffer->uuid, buffer->msg,
          header, tail);

  __sync_fetch_and_add(&count, 1);

  pthread_cond_signal(&fill);
  pthread_mutex_unlock(&lock);
}

void process(struct bucket *buf) {
  printf("Consumed: Bucket id(%d) content(%s). Counter(%d) header(%d) tail(%d)\n", 
        buf->uuid, buf->msg, count, header, tail);
}

void consume() {

  pthread_mutex_lock(&lock);

  __sync_synchronize();

  while (count == 0) {
    printf("Ring buffer is emtpy!\n");
    pthread_cond_wait(&fill, &lock);
  }

  // FIFO
  struct bucket *buffer = ring_buf[header];
  if (buffer != NULL) {
    process(buffer);
    // clean up
    free((void*)buffer);
    ring_buf[header] = NULL;
    // set header.
    __sync_synchronize();
    header = (header+1) % BUCKET_SIZE;

    __sync_fetch_and_sub(&count, 1);
  } else {
    printf("buffer is NULL. Counter(%d) header(%d) tail(%d)\n",
          count, header, tail);
  }
  
  pthread_cond_signal(&empty);
  pthread_mutex_unlock(&lock);
}

int loops;

void* batch_produce() {
  for (int i=0; i<loops/2; i++) {
    char * msg = "Mushroom is growing.";
    produce(msg);
  }
  return NULL;
}

void* batch_consume() {
  for (int i=0; i<loops; i++) {
    consume();
  }
  return NULL;
}

int main() {
  init();

  loops = 1000;
  pthread_create(&(tid[0]), NULL, &batch_produce, NULL);
  pthread_create(&(tid[1]), NULL, &batch_produce, NULL);
  pthread_create(&(tid[2]), NULL, &batch_consume, NULL);


  pthread_join(tid[0], NULL);
  pthread_join(tid[1], NULL);
  pthread_join(tid[2], NULL);
  pthread_mutex_destroy(&lock);

  printf("Ring buffer produced number %d. Consumed %d.\n", uuid, uuid-count);
}