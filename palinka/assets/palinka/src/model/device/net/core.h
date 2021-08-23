#ifndef __PHY_NET_H__
#define __PHY_NET_H__

#include "src/model/device/core.h"
#include "src/model/device/net/cfg.h"
#include "src/model/device/cfg.h"
#include "src/model/device/accessor.h"
#include "src/utils/alloc.h"

struct NetCard_t 
{
    /*! The other physical device on the other side */
    struct PhysicalDeviceAccessor_t foreign;

    /*! The system owning the card */
    struct System_t* sys;

    /*! Interrupt Request Code */
    char irq;
};

struct NetDMAHeader_t
{
    size_t len;
};

/*! Transmission command */
const unsigned char NET_TX_CMD = 0x1;

int hard_net_write(struct PhysicalDevice_t* dev, unsigned char cmd)
{
    if (cmd == NET_TX_CMD) 
    {

    }
}

/**
 * \brief Callback to initialise the network card from the PhysicalDeviceCfg_t
 */
int hard_net_init_(
    struct PhysicalDevice_t*    pdev,
    struct PhysicalDeviceCfg_t* pcfg,
    struct Allocator_t*         firmware_allocator,
    struct Allocator_t*         dev_allocator
);

/**
 * \brief Initialise the network card.
 */
int hard_net_init(
    struct PhysicalDevice_t* pdev, 
    struct NetworkCardCfg_t *cfg, 
    struct Allocator_t* firmware_allocator,
    struct Allocator_t* dev_allocator
);

/**
 * \brief Send data to the network card.
 */
void hard_net_recv(
    struct PhysicalDevice_t* pdev, 
    void* data,
    size_t len
);

/**
* \brief Send data from the network card
*/
void hard_net_send(
    struct PhysicalDevice_t* pdev,
    void* data,
    size_t len
);

#endif