#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys01.h"
#include "libs/blocks/bin_input.h"
void sys_sys01_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 3);
    sys_sys01_cpy_recv(& sys);
    fb_FP01(& sys);
    sys_sys01_cpy_send(& sys);
    close_system(& sys);
}
void fp_FP01(struct System_t * sys) {
    struct DataBlock_t idb;
    idb = open_data_block(sys, 0);
    block_bin_input(idb.base[0], idb.base[1]);
    close_data_block(& idb);
}
void sys_sys01_cpy_recv(struct System_t * sys) {
    sys_sys01_cpy_recv_0(sys);
}
void sys_sys01_cpy_recv_0(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 2);
    close_data_block(& idb);
}
void sys_sys01_cpy_send(struct System_t * sys) {
    sys_sys01_cpy_send_1(sys);
}
void sys_sys01_cpy_send_1(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 3);
    close_data_block(& idb);
}