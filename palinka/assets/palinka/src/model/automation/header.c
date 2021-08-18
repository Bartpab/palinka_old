#include "src/model/common/data.h"

struct AutomationHeader_t* get_automation_header(struct System_t* sys) 
{
    return (struct AutomationHeader_t*) (get_common_header(sys) + 1);
}
