#ifndef __DEV_PHY_NET_CFG_H__
#define __DEV_PHY_NET_CFG_H__

#include <stddef.h>

#include "src/model/device/cfg.h"
#include "src/model/device/net/core.h"

/**
 * \brief Network Card Configuration
 */
struct NetCardCfg_t
{
    size_t foreign_sys_id;
    size_t foreign_dev_id;

    size_t queue_size;
};

int hard_net_cfg(struct NetCardCfg_t net_cfg, struct PhysicalDeviceCfg_t* cfg)
{
    cfg->data = malloc(sizeof(struct NetCardCfg_t));
    *(struct NetworkCardCfg_t*) cfg->data = net_cfg;
    cfg->init = hard_net_init_;
    cfg->dma_size = net_cfg->queue_size;
}


#endif