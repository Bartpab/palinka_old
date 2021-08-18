#include "src/model/common/skb.h"
#include "src/utils/alloc.h"

int skb_queue_init(struct SocketBufferQueue_t* queue, struct Allocator_t* allocator, size_t capacity) 
{
    queue->arena = (struct SocketBufferQueueCell_t*) allocator_alloc(allocator, sizeof(struct SocketBufferQueueCell_t) * capacity);
    queue->capacity = capacity;

    if(queue->arena == NULL)
        return 0;

    return 1;
}

void skb_queue_delete(struct SocketBufferQueue_t* queue, struct Allocator_t* allocator) 
{
    allocator_free(allocator, queue->arena);
    queue->arena = queue->head = queue->tail = NULL;
}

int skb_enqueue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t* skb) 
{
    if(queue->arena == NULL)
        return 0;

    struct SocketBufferQueueCell_t* cell;
    size_t cell_id = queue->capacity;

    // we find a free cell to store our value
    for(size_t i = 0; i < queue->capacity; i++) 
    {
        if(queue->arena[i].is_free) 
            cell_id = i;
    }

    // cannot enqueue anymore...
    if(cell_id == queue->capacity)
        return 0;

    cell = queue->arena + cell_id;
    cell->is_free = 0;
    cell->skb = skb;
    
    if(queue->head == NULL) {
        queue->head = queue->tail = cell;
    } else {
        queue->tail->next = cell;
        queue->tail = cell;
    }

    return 1;
}   

int skb_dequeue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t** skb) 
{
    struct SocketBufferQueueCell_t* cell;

    if (queue->head == NULL)
        return 0;
    
    cell = queue->head;
    cell->is_free = 1;    

    queue->head = cell->next;
    cell->next = NULL;

    *skb = cell->skb;
    
    return 1;   
}

struct SocketBuffer_t* alloc_skb(struct Allocator_t* allocator, size_t len) 
{
    void* block = allocator_alloc(allocator, sizeof(struct SocketBuffer_t) + len);

    // Do not have anymore memory
    if (!block)
        return NULL;

    struct SocketBuffer_t* skb = (struct SocketBuffer_t*) block;
    
    skb->end = block + sizeof(struct SocketBuffer_t) + len;
    skb->head = skb->data = skb->tail = block + sizeof(struct SocketBuffer_t);    
    
    skb->size = len;

    return skb;
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