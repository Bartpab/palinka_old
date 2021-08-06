#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys01.h"
#include "libs/blocks/bin_input.h"
void sys_sys01_init(struct System_t * system) {
    sys->app_base = sys->base;
    sys->nb_blocks = 3;
    sys->data_blocks = (struct DataBlock_t *) malloc(sizeof(struct DataBlock_t) * 3);
    sys.data_blocks[0]->base = sys->app_base[0];
    sys.data_blocks[2]->base = sys->app_base[3];
    sys.data_blocks[1]->base = sys->app_base[2];
    sys.sys_base = sys.base + sys_sys01_app_memory_size();
}
void sys_sys01_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 3);
    sys_sys01_cpy_recv(& sys);
    fb_FP01(& sys);
    sys_sys01_cpy_send(& sys);
    close_system(& sys);
}
size_t sys_sys01_memory_size() {
    return sys_sys01_app_size_memory() + sys_sys01_os_size_memory();
}
size_t sys_sys01_app_memory_size() {
    return 2 + 1 + 1;
}
size_t sys_sys01_os_memory_size() {
    return sizeof(struct SystemData_t);
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