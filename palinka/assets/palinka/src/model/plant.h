#include <phtread>

/**
* \struct Plant_t
* \brief A handler to the simulated plant.
*/
struct Plant_t {
    /*! Memory base of the plant */
    char* base;
    unsigned int nb_systems;
    System_t* systems;
};

///////////
/// API ///
///////////
/**
 * \brief Initialise a plant simulation.
 */
struct Plant_t init();

/**
 * \brief Execute a step of the simulation for the plant.
 */
void step(struct Plant_t * plant);