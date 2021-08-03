#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/SYS01.h"
#include "src/blocks/bin_input.h"
void sys_SYS01_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 1);
    fb_FP01(& sys);
    sys_SYS01_copy_send(& sys);
    close_system(& sys);
}
void fp_FP01(struct System_t * sys) {
    struct DataBlock_t idb;
    idb = open_data_block(sys, 0);
    block_bin_input(idb.base[0]);
    close_data_block(& idb);
}
void sys_SYS01_cpy_send(struct System_t * sys) {
    sys_SYS01_cpy_send_0(sys);
}
void sys_SYS01_cpy_send_0(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 1);
    fp_idb = open_data_block(sys, 0);
    * idb.base[0] = * fp_idb.base[0]
    close_data_block(& fp_idb);
    close_data_block(& idb);
}