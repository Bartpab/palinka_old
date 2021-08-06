#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys02.h"
#include "libs/blocks/neg.h"
void sys_sys02_init(struct System_t * system) {
    sys->app_base = sys->base;
    sys->nb_blocks = 3;
    sys->data_blocks = (struct DataBlock_t *) malloc(sizeof(struct DataBlock_t) * 3);
    sys.data_blocks[0]->base = sys->app_base[0];
    sys.data_blocks[2]->base = sys->app_base[5];
    sys.data_blocks[1]->base = sys->app_base[4];
    sys.sys_base = sys.base + sys_sys02_app_memory_size();
}
void sys_sys02_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 4);
    sys_sys02_cpy_recv(& sys);
    fb_FP02(& sys);
    sys_sys02_cpy_send(& sys);
    close_system(& sys);
}
size_t sys_sys02_memory_size() {
    return sys_sys02_app_size_memory() + sys_sys02_os_size_memory();
}
size_t sys_sys02_app_memory_size() {
    return 4 + 1 + 1;
}
size_t sys_sys02_os_memory_size() {
    return sizeof(struct SystemData_t);
}
void fp_fp02(struct System_t * sys) {
    struct DataBlock_t idb;
    idb = open_data_block(sys, 0);
    block_neg(idb.base[0], idb.base[1]);
    * idb.base[2] = * idb.base[1];
    block_neg(idb.base[2], idb.base[3]);
    close_data_block(& idb);
}
void sys_sys02_cpy_recv(struct System_t * sys) {
    sys_sys02_cpy_recv_DLNK1(sys);
}
void sys_sys02_cpy_recv_DLNK1(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 1);
    close_data_block(& idb);
}
void sys_sys02_cpy_send(struct System_t * sys) {
    sys_sys02_cpy_send_DLNK2(sys);
}
void sys_sys02_cpy_send_DLNK2(struct System_t * sys) {
    struct DataBlock_t idb;
    struct DataBlock_t fp_idb;
    idb = open_data_block(sys, 2);
    close_data_block(& idb);
}