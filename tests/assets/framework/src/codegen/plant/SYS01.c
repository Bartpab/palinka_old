#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys01.h"
#include "libs/blocks/bin_input.h"
void sys_sys01_init(struct System_t * system) {
    sys.nb_blocks = 3;
    sys.data_blocks = (struct DataBlock_t *) malloc(sizeof(struct DataBlock_t) * 3);
    sys.data_blocks[0]->offset = 4;
    sys.data_blocks[2]->offset = 4;
    sys.data_blocks[1]->offset = 4;
}
void sys_sys01_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 3);
    sys_sys01_cpy_recv(& sys);
    fb_FP01(& sys);
    sys_sys01_cpy_send(& sys);
    close_system(& sys);
}
void fp_fp01(struct System_t * sys) {
    struct DataBlock_t idb;
    idb = open_data_block(sys, 0);
    block_bin_input(idb.base[0], idb.base[1]);
    close_data_block(& idb);
}
void sys_sys01_cpy_recv(struct System_t * sys) {
    sys_sys01_cpy_recv_DLNK0(sys);
}
void sys_sys01_cpy_recv_DLNK0(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 1);
    close_data_block(& idb);
}
void sys_sys01_cpy_send(struct System_t * sys) {
    sys_sys01_cpy_send_DLNK1(sys);
}
void sys_sys01_cpy_send_DLNK1(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 2);
    close_data_block(& idb);
}