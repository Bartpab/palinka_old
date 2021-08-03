#include "src/model/plant.h"

void step(struct Plant_t * plant)
{
    // Call every system step linearly
    for(int i = 0; i < plant->nb_systems; i++)
    {
        plant->systems[i]->step(plant);
    }
}