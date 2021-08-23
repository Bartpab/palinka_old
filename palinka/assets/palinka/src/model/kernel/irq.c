#include "src/model/kernel/irq.h"

int irq_init(struct InterruptRequestTable_t* table, struct Allocator_t* allocator, size_t capacity) 
{
    struct InterruptRequestTableEntry_t* it;

    table->base = (struct InterruptRequestTableEntry_t*) allocator_alloc(allocator, sizeof(struct InterruptRequestTableEntry_t) * capacity);
    
    if(table->base == NULL)
        return 0;

    table-> limit = table->base + capacity - 1;

    it = table->base;

    while(it <= table->limit) 
    {
        it->interrupt = NULL;
        it++;
    }

    return 1;
}

void irq_delete(struct InterruptRequestTable_t* table, struct Allocator_t* allocator) 
{
    if(table->base == NULL)
        return;
    
    allocator_free(allocator, table->base);
    table->base = table->limit = NULL;
}

int irq_register(struct InterruptRequestTable_t* table, unsigned char irq, int (*interrupt)(struct System_t* sys, unsigned char irq)) 
{
    if (table->base + irq > table->limit)
        return 0;
    
    (table->base + irq)->interrupt = interrupt;
    return 1;
}

int irq_interrupt(struct System_t* sys, struct InterruptRequestTable_t* table, unsigned char irq)
{
    int (*interrupt)(struct System_t*);

    if (table->base + irq > table->limit)
        return 0;
    
    // The interrupt was not registered...
    interrupt = (table->base + irq)->interrupt;

    if(interrupt == NULL);
        return 0;

    return interrupt(sys, irq);   
}