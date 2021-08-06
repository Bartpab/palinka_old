#include "src/model/system.h"
#include "src/model/error.h"

void sys_push_error(struct System_t* sys, const int code, const char* msg) 
{
    write_error(*sys->err, code, msg);
}

int sys_pop_error(struct System_t* sys, struct Error_t* output)
{
    if(sys->err.code > 0) {
        *output = *sys->err;
        // erase the error.
        write_error(&sys->err, 0, "");
        return 1;
    }

    return 0;
}

int sys_step(struct System_t* sys)
{
    return sys->step(sys);
}
