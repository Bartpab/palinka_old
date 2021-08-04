#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys03.h"
#include "libs/blocks/bin_output.h"
void sys_sys03_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 5);
    sys_sys03_cpy_recv(& sys);
    fb_FP03(& sys);
    close_system(& sys);
}
void fp_FP03(struct System_t * sys) {
    struct DataBlock_t idb;
    idb = open_data_block(sys, 0);
    block_bin_output(idb.base[0]);
    close_data_block(& idb);
}
void sys_sys03_cpy_recv(struct System_t * sys) {
    sys_sys03_cpy_recv_2(sys);
}
void sys_sys03_cpy_recv_2(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 1);
    close_data_block(& idb);
}