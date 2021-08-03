#include <phtread>

struct Plant_t {
    char* base;
    unsigned int nb_systems;
    System_t* systems;
};

struct System_t
{
    unsigned int offset;
    pthread_rwlock_t  rwlock;
    void (*step)(struct Plant_t*);
}

///////////
/// API ///
///////////
/**
 * Initialise a plant simulation
 */
struct Plant_t init();
void step(struct Plant_t * plant);