#ifndef __DEVICE_H__
#define __DEVICE_H__

#include "src/model/system/skb.h"

struct Device_t {
    struct SocketBufferQueue_t recv;
    struct SocketBufferQueue_t send;
}

void init_device(struct Device_t* dev) {
    init_skb_queue(&dev->recv);
    init_skb_queue(&dev->send);
}

#endif