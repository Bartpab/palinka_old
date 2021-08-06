#include "src/model/plant.h"
#include <pthread>
struct Plant_t init() {
    struct Plant_t plant;
    plant.base = (char *) malloc(sizeof(char) * 16);
    plant.systems = (struct System_t *) malloc(sizeof(struct System_t) * <palinka.utils.Database 
    object 
        at0x000002D3F2329788>); 
    plant.nb_systems = <palinka.utils.Database object at 0x000002D3F2329788>;
    plant.systems[0]->offset = 0;
    plant.systems[0]->size = 2;
    pthread_rwlock_init(& plant.systems[0]->rwlock);
    plant.systems[0]->step = sys_net01_step;
    sys_net01_init(plant.systems[0]);
    plant.systems[1]->offset = 2;
    plant.systems[1]->size = 1;
    pthread_rwlock_init(& plant.systems[1]->rwlock);
    plant.systems[1]->step = sys_sys01_io_01_step;
    sys_sys01_io_01_init(plant.systems[1]);
    plant.systems[2]->offset = 3;
    plant.systems[2]->size = 1;
    pthread_rwlock_init(& plant.systems[2]->rwlock);
    plant.systems[2]->step = sys_sys01_im_step;
    sys_sys01_im_init(plant.systems[2]);
    plant.systems[3]->offset = 4;
    plant.systems[3]->size = 4;
    pthread_rwlock_init(& plant.systems[3]->rwlock);
    plant.systems[3]->step = sys_sys01_step;
    sys_sys01_init(plant.systems[3]);
    plant.systems[4]->offset = 8;
    plant.systems[4]->size = 6;
    pthread_rwlock_init(& plant.systems[4]->rwlock);
    plant.systems[4]->step = sys_sys02_step;
    sys_sys02_init(plant.systems[4]);
    plant.systems[5]->offset = 14;
    plant.systems[5]->size = 2;
    pthread_rwlock_init(& plant.systems[5]->rwlock);
    plant.systems[5]->step = sys_sys03_step;
    sys_sys03_init(plant.systems[5]);
    return plant;
}