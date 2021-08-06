#ifndef __SKB_H__
#define __SKB_H__

#include "src/model/system/mmu.h"
#include "src/model/system.h"

#define SKB_QUEUE_SIZE 300

/*
* Socket Buffer
*/
struct SocketBufferQueue_t {
    struct SocketBufferQueueCell_t* head;
    struct SocketBufferQueueCell_t* tail;
    
    struct SocketBufferQueueCell_t  arena[SKB_QUEUE_SIZE];
    const size_t size;
};

struct SocketBufferQueueCell_t {
    struct SocketBuffer_t* skb;
    char is_free;
    struct SocketBufferQueueCell_t* next;
};

void init_skb_queue(struct SocketBufferQueue_t* queue);
int skb_enqueue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t* skb); 
int skb_dequeue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t** skb);

struct SocketBuffer_t {
    char* head;
    char* data;
    char* tail;
    char* end;

    size_t size;
    size_t len;
};

struct SocketBuffer_t* alloc_skb(struct System_t* sys, size_t len);
void free_skb(struct System_t* sys, struct SocketBuffer_t* skb);

int skb_reserve(struct SocketBuffer_t* skb, size_t len);
char *skb_push(struct SocketBuffer_t* size_t data_len);
char* skb_put(struct SocketBuffer_t* skb, size_t data_len);

#endif