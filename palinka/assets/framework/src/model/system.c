#include "src/model/system.h"

struct DataBlock_t open_data_block(struct System_t* sys, unsigned int offset)
{
    struct DataBlock_t db = { sys->base[offset] };
    return db;
}