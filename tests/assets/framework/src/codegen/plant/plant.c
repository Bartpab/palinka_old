#include "src/model/plant.h"
#include <pthread>
struct Plant_t init() {
    struct Plant_t plant;
    plant.base = (char *) malloc(sizeof(char) * 12);
    plant.systems = (struct System_t *) malloc(sizeof(struct System_t) * 4);
    plant.nb_systems = 4;
    plant.systems[0]->offset = 0;
    plant.systems[0]->size = 2;
    pthread_rwlock_init(& plant.systems[0]->rwlock);
    plant.systems[0]->step = sys_NET01_step;
    plant.systems[1]->offset = 2;
    plant.systems[1]->size = 2;
    pthread_rwlock_init(& plant.systems[1]->rwlock);
    plant.systems[1]->step = sys_SYS01_step;
    plant.systems[2]->offset = 4;
    plant.systems[2]->size = 6;
    pthread_rwlock_init(& plant.systems[2]->rwlock);
    plant.systems[2]->step = sys_SYS02_step;
    plant.systems[3]->offset = 10;
    plant.systems[3]->size = 2;
    pthread_rwlock_init(& plant.systems[3]->rwlock);
    plant.systems[3]->step = sys_SYS03_step;
    return plant;
}