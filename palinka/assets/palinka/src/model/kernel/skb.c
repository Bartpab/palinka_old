#include "src/model/kernel/skb.h"

int skb_queue_init(struct SocketBufferQueue_t* queue) 
{
    queue->head = queue->tail = NULL;
}

void skb_queue_delete(struct SocketBufferQueue_t* queue, struct Allocator_t* allocator) 
{
    queue->head = queue->tail = NULL;
}

int skb_enqueue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t* skb) 
{   
    if(queue->head == NULL) 
    {
        queue->head = queue->tail = skb;
    } else {
        queue->tail->next = skb;
        queue->tail = skb;
    }

    return 1;
}   

int skb_dequeue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t** skb) 
{
    struct SocketBuffer_t* el;

    if (queue->head == NULL)
        return 0;
    
    el = queue->head;

    queue->head = el->next;
    el->next = NULL;

    *skb = el;
    
    return 1;   
}

int alloc_skb(struct Allocator_t* allocator, size_t len, struct SocketBuffer_t** out) 
{
    void* block = allocator_alloc(allocator, sizeof(struct SocketBuffer_t) + len);

    // Do not have anymore memory
    if (!block)
        return 0;

    struct SocketBuffer_t* skb = (struct SocketBuffer_t*) block;
    
    skb->end = block + sizeof(struct SocketBuffer_t) + len;
    skb->head = skb->data = skb->tail = block + sizeof(struct SocketBuffer_t);    
    
    skb->size = len;

    *out = skb;

    return 1;
}

void free_skb(struct Allocator_t* allocator, struct SocketBuffer_t* skb) 
{
    allocator_free(allocator, skb);
}

int skb_reserve(struct SocketBuffer_t* skb, size_t len) 
{
    // Cannot reserve more memory in the buffer...
    if (skb->tail + len > skb->end) {
        return 0;
    }
    skb->tail = skb->data = skb->tail + len;
    return 1;
}

void *skb_push(struct SocketBuffer_t* skb, size_t data_len) {
    // No more room left in the headspace.
    if (skb->data - data_len < skb->head) 
    {
        return NULL;
    }
    skb->data -= data_len;
    
    return skb->data;
}

void* skb_put(struct SocketBuffer_t* skb, size_t data_len) {
    
    // No more room left in the tailspace.
    if (skb->tail + data_len > skb->end) 
    {
        return NULL;
    }

    void* data = skb->tail;
    skb->tail += data_len;
    
    return data;
} 