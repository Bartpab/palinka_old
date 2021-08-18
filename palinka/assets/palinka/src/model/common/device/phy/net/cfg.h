#ifndef __DEV_PHY_NET_CFG_H__
#define __DEV_PHY_NET_CFG_H__

#include <stddef.h>

#include "src/model/common/device/phy/cfg.h"
#include "src/model/common/device/phy/net/api.h"

/**
 * \brief Network Card Configuration
 */
struct NetworkCardCfg_t
{
    size_t foreign_sys_id;
    size_t foreign_dev_id;

    size_t recv_len;
    size_t send_len;
};

int hard_net_cfg(struct NetworkCardCfg_t net_cfg, struct PhysicalDeviceCfg_t* cfg)
{
    cfg->data = malloc(sizeof(struct NetworkCardCfg_t));
    *(struct NetworkCardCfg_t*) cfg->data = net_cfg;
    cfg->init = hard_net_init_;
}


#endif