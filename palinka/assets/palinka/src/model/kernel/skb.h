#ifndef __SKB_H__
#define __SKB_H__

#include "src/model/kernel/mmu.h"
#include "src/model/kernel/drivers/net_device.h"
#include "src/model/system/core.h"
#include "src/utils/memory/alloc.h"

#define SKB_QUEUE_SIZE 300

/**
* \brief Socket buffer queue
*/
struct SocketBufferQueue_t 
{
    struct SocketBuffer_t* head;
    struct SocketBuffer_t* tail;
};

/**
 * \brief Initialise a Socket Buffer Queue
 * 
 * \param queue The queue to initialise
 * \param allocator A memory allocator
 * \param capacity The capacity of the queue
 * 
 * \return 1 if succeeded, 0 if failed (no more memory)
 */
int skb_queue_init(struct SocketBufferQueue_t* queue);

/**
 * \brief Delete a Socket Buffer Queue
 * 
 * \param queue The queue to delete.
 * \param allocator The allocator used to initialise the queue.
 */
void skb_queue_delete(struct SocketBufferQueue_t* queue, struct Allocator_t* allocator);

/**
 * \brief Enqueue a socket buffer
 * 
 * \return 1 if succeeded, 0 if failed (no more cell left)
 */ 
int skb_enqueue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t* skb); 

/**
 * \brief Dequeue a socket buffer
 * 
 * \param queue The queue
 * \param skb Where to store the address to the socket buffer (if any)
 * \return 1 if an element is stored in the queue, 0 else.
 */
int skb_dequeue(struct SocketBufferQueue_t* queue, struct SocketBuffer_t** skb);

/**
 * \brief Socket Buffer
 * 
 * This is used to prepare a frame to send over the network/bus
 */
struct SocketBuffer_t 
{
    void* head;
    void* data;
    void* tail;
    void* end;

    size_t size;
    size_t len;

    struct NetDevice_t* dev;
    struct SocketBuffer_t* next;
};

/**
 * \brief Allocate a new socket buffer
 * 
 * \param allocator The allocator
 * \param len The capacity of the buffer
 */
int alloc_skb(struct Allocator_t* allocator, size_t capacity, struct SocketBuffer_t** out);

/**
 * \brief Free the socket buffer
 * 
 * \param allocator The allocator used to allocate the socket buffer.
 * \param skb The socket buffer to free.
 */
void free_skb(struct Allocator_t* allocator, struct SocketBuffer_t* skb);

/**
 * \brief Reserve headspace in the buffer
 * 
 * This reserves space to write the header part of the buffer.
 * \return 1 if succeeded, 0 if failed (no more space)
 */
int skb_reserve(struct SocketBuffer_t* skb, size_t len);

/**
 * \brief Consume tailspace to write data at the end of the buffer 
 * 
 * \return The pointer to the pushed memory block, NULL if failed.
 */
void* skb_push(struct SocketBuffer_t* skb, size_t data_len);

/**
 * \brief Consume headspace to write data at the beginning of the buffer
 * 
 * \return The pointer to the pushed memory block, NULL if failed.
 */
void* skb_put(struct SocketBuffer_t* skb, size_t data_len);

#endif