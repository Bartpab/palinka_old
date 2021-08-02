#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/SYS02.h"
#include "src/blocks/neg.h"
void * sys_SYS02_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 2);
    fb_FP02(sys);
    sys_SYS02_copy_to_sending_memory(sys);
    close_system(sys);
}
void fp_FP02(struct System_t * sys) {
    struct DataBlock_t * idb;
    idb = open_data_block(sys, 0);
    block_neg(idb->base[0], idb->base[1]);
    * idb->base[2] = * idb->base[1];
    block_neg(idb->base[2], idb->base[3]);
}
void sys_SYS02_copy_to_sending_memory(struct System_t * sys) {
    sys_SYS02_copy_to_sending_memory_for_SYS03(sys);
}
void sys_SYS02_copy_to_sending_memory_for_SYS03(struct System_t * sys) {
    struct DataBlock_t * idb;
    struct DataBlock_t * fp_idb;
    idb = open_data_block(sys, 4);
    fp_idb = open_data_block(sys, 0);
    * idb->base[0] = * fp_idb->base[3]
}