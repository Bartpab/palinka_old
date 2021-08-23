#include "src/model/device/net/core.h"
#include "src/model/device/accessor.h"

int hard_net_init_(
    struct PhysicalDevice_t* pdev,
    struct PhysicalDeviceCfg_t* pcfg,
    struct Allocator_t* firmware_allocator,
    struct Allocator_t* dev_allocator
) {
    return hard_net_init(pdev, (struct NetCardCfg_t*) pcfg->data, firmware_allocator, dev_allocator);
}

int hard_net_init(
    struct PhysicalDevice_t* pdev, 
    struct NetCardCfg_t *cfg, 
    struct Allocator_t* firmware_allocator,
    struct Allocator_t* dev_allocator
) {
    pdev->firmware = allocator_alloc(firmware_allocator, sizeof(struct NetworkCard_t));

    if(pdev->firmware == NULL)
        return 0;

    size_t dev_memory_size = cfg->recv_len + cfg->send_len;
    pdev->base = allocator_alloc(dev_allocator, dev_memory_size);
    
    if(pdev->base == NULL) 
    {
        allocator_free(firmware_allocator, pdev->firmware);
        return 0;
    }
    
    pdev->limit = pdev->base + dev_memory_size - 1;
}

void hard_net_recv(struct PhysicalDevice_t* pdev, void* data, size_t len)
{
    struct NetworkCard_t* card = (struct NetworkCard_t* ) pdev->firmware;
    struct NetworkCardHeader_t* header = (struct NetworkCardHeader_t*) pdev->base;
    
    size_t max_size = (size_t) ((char*)header->send_buffer - (char*)header->recv_buffer);
    
    // Ensure we don't oveflow.
    len = MIN(max_size, len);
    memcpy(header->recv_buffer, data, len);
    header->recv_len = len;

    // Trigger the interrupt
    sys_interrupt(card->sys, card->irq);
}

void hard_net_send(
    struct PhysicalDevice_t* pdev,
    void* data,
    size_t len
) {
    struct PhysicalDevice_t* foreign_pdev;
    struct NetworkCard_t* card = (struct NetworkCard_t* ) pdev->firmware;

    // We have access the foreign physical card.
    if(phy_dev_open(&card->foreign, &foreign_pdev)) 
    {
        hard_net_recv(&foreign_pdev, data, len);
        // We do not forget to close the physical device access.
        phy_dev_close(&card->foreign);
    }
}