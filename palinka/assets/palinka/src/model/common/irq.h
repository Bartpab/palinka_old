#ifndef __IRQ__
#define __IRQ__

#include "src/model/system/api.h"
#include "src/utils/alloc.h"

#include <stdlib.h>

/**
 * \struct InterruptRequestTable_t
 * \brief Contains the IRQ table for interruption
 *
 */
struct InterruptRequestTable_t 
{
    struct InterruptRequestTableEntry_t* base;
    struct InterruptRequestTableEntry_t* limit;
};

struct InterruptRequestTableEntry_t 
{
    int (*interrupt)(struct System_t*);
};

int irq_init(struct InterruptRequestTable_t* table, struct Allocator_t* allocator, size_t capacity);
void irq_delete(struct InterruptRequestTable_t* table, struct Allocator_t* allocator);
int irq_register(struct InterruptRequestTable_t* table, unsigned char irq, int (*interrupt)(struct System_t*));
int irq_interrupt(struct System_t* sys, struct InterruptRequestTable_t* table, unsigned char irq);

#endif