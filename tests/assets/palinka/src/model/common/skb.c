#include "src/model/system/skb.h"

void init_skb_queue(struct SocketBufferQueue_t* queue) {
    queue->size = SKB_QUEUE_SIZE;
    return queue;
}

int skb_enqueue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t* skb) {
    size_t cell_id = queue->size;

    // we find a free cell to store our value
    for(size_t i = 0; i < queue->size; i++) {
        if(queue->arena[i]->is_free) {
            cell_id = i;
        }
    }

    // cannot enqueue anymore...
    if(cell_id == queue->size) {
        return 0;
    }

    struct SocketBufferQueueCell_t* cell = queue->arena[cell_id];
    cell->is_free = 0;
    
    if(queue->head == NULL) {
        queue->head = queue->tail = cell;
    } else {
        queue->tail->next = cell;
        queue->tail = cell;
    }

    return 1;
}   

int skb_dequeue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t** skb) {
    if (queue->head == NULL)
        return 0;
    
    struct SocketBufferQueueCell_t* cell = queue->head;
    cell->is_free = 1;    

    queue->head = cell->next;
    cell->next = 0;

    *skb = cell->skb;
    return 1;   
}

struct SocketBuffer_t* alloc_skb(struct System_t* sys, size_t len) {
    char* block = sys_alloc(sizeof(struct SocketBuffer_t) + len);

    if (!block)
        return NULL;

    struct SocketBuffer_t* skb = (struct SocketBuffer_t) block;
    
    skb->end = block + sizeof(struct SocketBuffer_t) + len;
    skb->head = skb->data = skb->tail = block + sizeof(struct SocketBuffer_t);    
    
    skb->size = len;

    return skb
}

void free_skb(struct System_t* sys, struct SocketBuffer_t* skb) {
    sys_free(sys, (char*) skb);
}

int skb_reserve(struct SocketBuffer_t* skb, size_t len) {
    // Cannot reserve more memory in the buffer...
    if (skb->tail + len > skb->end) {
        return 0;
    }
    skb->tail = skb->data = skb->tail + len;
    return 1;
}

char *skb_push(struct SocketBuffer_t* size_t data_len) {
    if (skb->data - len < skb->head) {
        return NULL;
    }
    skb->data -= data_len;
    return skb->data;
}

// skb_put — add data to a buffer 
char* skb_put(struct SocketBuffer_t* skb, size_t data_len) {
    
    if (skb->tail + len > skb->end) {
        return NULL;
    }
    skb->tail += data_len;
    return skb->data;
} 