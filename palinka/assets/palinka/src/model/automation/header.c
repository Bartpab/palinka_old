#include "src/model/kernel/data.h"

struct AutomationHeader_t* get_automation_header(struct System_t* sys) 
{
    return (struct AutomationHeader_t*) (get_kernel_header(sys) + 1);
}
