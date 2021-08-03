#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/SYS03.h"
#include "src/blocks/bin_output.h"
void sys_SYS03_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 2);
    sys_SYS03_copy_recv(sys);
    fb_FP03(sys);
    sys_SYS03_copy_send(sys);
    close_system(sys);
}
void fp_FP03(struct System_t * sys) {
    struct DataBlock_t idb;
    idb = open_data_block(sys, 0);
    block_bin_output(idb.base[0]);
    close_data_block(& idb);
}
void sys_SYS03_cpy_recv(struct System_t sys) {
    sys_SYS03_cpy_recv_SYS02(sys);
}
void sys_SYS03_cpy_recv_SYS02(struct System_t sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 1);
    fp_idb = open_data_block(sys, 0);
    * fp_idb.base[0] = * idb.base[0]
    close_data_block(& fp_idb);
    close_data_block(& idb);
}
void sys_SYS03_cpy_send(struct System_t sys) {
    
}