#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/SYS03.h"
#include "src/blocks/bin_output.h"
void * sys_SYS03_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 7);
    fb_FP03(sys);
    sys_SYS03_copy_to_sending_memory(sys);
    close_system(sys);
}
void fp_FP03(struct System_t * sys) {
    struct DataBlock_t * idb;
    idb = open_data_block(sys, 0);
    block_bin_output(idb->base[0]);
}
void sys_SYS03_copy_to_sending_memory(struct System_t * sys) {
    
}