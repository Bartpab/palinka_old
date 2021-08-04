#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys01_io_01.h"
void sys_sys01_io_01_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 1);
    sys_sys01_io_01_cpy_send(& sys);
    close_system(& sys);
}
void sys_sys01_io_01_cpy_send(struct System_t * sys) {
    sys_sys01_io_01_cpy_send_0(sys);
}
void sys_sys01_io_01_cpy_send_0(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 0);
    close_data_block(& idb);
}