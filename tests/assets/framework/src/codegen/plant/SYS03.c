#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys03.h"
#include "libs/blocks/bin_output.h"
void sys_sys03_init(struct System_t * system) {
    sys.nb_blocks = 2;
    sys.data_blocks = (struct DataBlock_t *) malloc(sizeof(struct DataBlock_t) * 2);
    sys.data_blocks[0]->offset = 14;
    sys.data_blocks[1]->offset = 14;
}
void sys_sys03_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 5);
    sys_sys03_cpy_recv(& sys);
    fb_FP03(& sys);
    close_system(& sys);
}
void fp_fp03(struct System_t * sys) {
    struct DataBlock_t idb;
    idb = open_data_block(sys, 0);
    block_bin_output(idb.base[0]);
    close_data_block(& idb);
}
void sys_sys03_cpy_recv(struct System_t * sys) {
    sys_sys03_cpy_recv_DLNK2(sys);
}
void sys_sys03_cpy_recv_DLNK2(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 1);
    close_data_block(& idb);
}