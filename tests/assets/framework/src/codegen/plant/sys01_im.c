#include "src/model/system.h"
#include "src/model/data_block.h"
#include "src/codegen/plant/sys01_im.h"
void sys_sys01_im_init(struct System_t * system) {
    sys.nb_blocks = 1;
}
void sys_sys01_im_step(struct Plant_t * plant) {
    struct System_t * sys;
    sys = open_system(plant, 2);
    sys_sys01_im_cpy_relay(plant, & sys);
    close_system(& sys);
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
    other_idb = open_data_block(& sys, #SYS01:IO:01/SENDING:DLNK0);
    memcpy(idb.base, other_idb.base, sizeof(char) * @SYS01:IO:01/SENDING:DLNK0);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
    other_sys = open_system(plant, 3);
    other_idb = open_data_block(& sys, 1);
    memcpy(other_idb.base, idb.base, sizeof(char) * @SYS01:IO:01/SENDING:DLNK0);
    other_sys = close_data_block(& other_idb);
    other_sys = close_system(& other_sys);
}