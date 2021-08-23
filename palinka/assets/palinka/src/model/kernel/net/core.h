#ifndef __NET_DEVICE_H__
#define __NET_DEVICE_H__

#include "src/model/kernel/data.h"
#include "src/model/kernel/skb.h"
#include "src/model/device/net/core.h"
#include "src/utils/alloc.h"
#include <string.h>

struct NetDevice_t
{
    void*               base;
    unsigned char       irq;
    struct NetDevice_t* next;

    struct SocketBufferQueue_t queue;
};

/**
 * \brief Put the skb on the device's queue.
 */
int dev_queue_xmit(struct System_t* sys, struct SocketBuffer_t* skb)
{
    skb_enqueue(&skb->dev->queue, skb);
    return netif_tx_schedule(sys);
}

/**
 * \brief Schedule transmission to the network device.
 */
int netif_tx_schedule(struct System_t* sys)
{
    return netif_tx_action(sys);
}

/**
 * \brief For each network device, dequeue skbs and send it to the network device.
 */
int netif_tx_action(struct System_t* sys)
{
    struct NetDeviceListIterator_t it;
    struct NetDevice_t* dev;
    struct SocketBuffer_t* skb;

    struct Allocator_t allocator = create_sys_allocator(sys);
 
    struct KernelHeader_t* kernel = get_kernel_header(sys);

    net_dev_list_it_init(&it, &kernel->net_devices);
    
    while(it.next(&it)) 
    {
        if(it.get(&it, &dev)) 
        {
            while(skb_dequeue(&dev->queue, &skb)) 
            {   
                // We reenqueue skb if we failed to send the frame to the network device.
                if(!dev_hard_start_xmit(skb)) 
                {
                    skb_enqueue(&dev->queue, skb);
                    break;
                }
                else
                {
                    free_skb(&allocator, skb);
                }
            }
        }
    }
}

int dev_hard_start_xmit(struct SocketBuffer_t* skb)
{
} 

int netif_receive_skb(struct System_t* sys, struct SocketBuffer_t* skb)
{

}

int netif_poll(struct System_t* sys, struct NetDevice_t* dev)
{
    struct Allocator_t allocator = create_sys_allocator(sys);

    struct NetworkCardHeader_t* hard = (struct NetworkCardHeader_t*) dev->base;
    void* buffer = hard->recv_buffer;
    size_t buf_len = hard->recv_len;

    struct SocketBuffer_t* skb;
    
    if(!alloc_skb(&allocator, buf_len, &skb))
        return 0;

    memcpy(skb_push(skb, buf_len), buffer, buf_len);
    skb->dev = dev;
    
    return netif_receive_skb(sys, skb);
}

int netif_rx_action(struct System_t* sys, struct NetDevice_t* dev)
{
    return netif_poll(sys, dev);
}

/**
 * Schedule the recv of frames from the network device.
 */
int netif_rx_schedule(struct System_t* sys, unsigned char irq)
{
    struct NetDeviceListIterator_t it;
    struct NetDevice_t* net = NULL;

    struct KernelHeader_t* kernel = get_kernel_header(sys);

    // We find the net_device handling this IRQ.
    net_dev_list_it_init(&it, &kernel->net_devices);
    
    while(it.next(&it)) 
    {
        if(it.get(&it, &net)) 
        {
            if(net->irq == irq)
                break;
            else    
                net = NULL;
        }
    }

    // Couldn't find a dev handling this
    if(!net)
        return;
    
    return netif_rx_action(sys, net);
}

struct NetDeviceList_t
{
    struct NetDevice_t* tail;
};

struct NetDeviceListIterator_t
{
    struct NetDevice_t* curr;
    struct NetDeviceList_t* list;

    int (*next)(struct NetDeviceListIterator_t* it);
    int (*get)(struct NetDeviceListIterator_t* it, struct NetDevice_t* net);
};

void net_dev_list_it_init(struct NetDeviceListIterator_t* it, struct NetDeviceList_t* list)
{
    it->curr = NULL;
    it->list = list;

    it->next = net_dev_list_it_next;
    it->get = net_dev_list_it_get;
}

int net_dev_list_it_next(struct NetDeviceListIterator_t* it)
{
    if(it->curr == NULL)
        it->curr = it->list->tail;
    else if (it->curr->next == NULL)
        return 0;
    else
        it->curr = it->curr->next;
    
    return 1;
}

int net_dev_list_it_get(struct NetDeviceListIterator_t* it, struct NetDevice_t** out) 
{
    if(it->curr == NULL)
        return 0;
    
    *out = it->curr;
    return 1;
}

#endif