#include <stdio.h>
#include "src/model/error.h"

void error_init(struct Error_t* err)
{
    err->code = 0;
    snprintf(err->msg, ERROR_MSG_MAX_SIZE, "");
}

void write_error(struct Error_t* err, const int code, const char* msg) 
{
    snprintf(err->msg, ERROR_MSG_MAX_SIZE, msg);
    err->code = code;
}

void copy_error(struct Error_t* dest, const struct Error_t* src) 
{
    write_error(dest, src->code, src->msg);
}