#include "src/model/system/accessor.h"

int sys_open(struct SystemAccessor_t* sys, struct System_t** out)
{
    *out = sys;
    return 1;
}

void sys_close(struct SystemAccessor_t* sys)
{

}