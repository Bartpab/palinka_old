#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys01_im.h"
void sys_sys01_im_init(struct System_t * system) {
    sys->app_base = sys->base;
    sys->nb_blocks = 1;
    sys->data_blocks = (struct DataBlock_t *) malloc(sizeof(struct DataBlock_t) * 1);
    sys.data_blocks[0]->base = sys->app_base[0];
    sys.sys_base = sys.base + sys_sys01_im_app_memory_size();
}
void sys_sys01_im_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 2);
    sys_sys01_im_cpy_relay(plant, & sys);
    close_system(& sys);
}
size_t sys_sys01_im_memory_size() {
    return sys_sys01_im_app_size_memory() + sys_sys01_im_os_size_memory();
}
size_t sys_sys01_im_app_memory_size() {
    return 1;
}
size_t sys_sys01_im_os_memory_size() {
    return sizeof(struct SystemData_t);
}
void sys_sys01_im_relay(struct Plant_t * plant, struct System_t * sys) {
    sys_sys01_im_cpy_relay_DLNK0(plant, sys);
}
void sys_sys01_im_cpy_relay_DLNK0(struct Plant_t * sys, struct System_t * sys) {
    struct DataBlock_t idb;
    struct System_t other_sys;
    struct DataBlock_t other_idb;
    idb = open_data_block(sys, 0);
    other_sys = open_system(plant, 1);
    other_idb = open_data_block(& sys, 0);
    memcpy(idb.base, other_idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
    other_sys = open_system(plant, 3);
    other_idb = open_data_block(& sys, 1);
    memcpy(other_idb.base, idb.base, sizeof(char) * 1);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
}