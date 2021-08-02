#include "src/model/plant.h"
struct Plant_t * init() {
    struct Plant_t * plant;
    plant = (struct Plant_t *) malloc(sizeof(struct Plant_t));
    plant->base = (char *) malloc(sizeof(char) * 8);
    return plant;
}
void * step(struct Plant_t * plant) {
    sys_SYS01_step(plant);
    sys_SYS02_step(plant);
    sys_SYS03_step(plant);
}