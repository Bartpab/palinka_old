#ifndef __ERROR_H__
#define __ERROR_H__

#define ERROR_MSG_MAX_SIZE 256

struct Error_t 
{
    char msg[ERROR_MSG_MAX_SIZE];
    int  code;
};

void error_init(struct Error_t* err);

void write_error(struct Error_t* err, const int code, const char* msg);
void copy_error(struct Error_t* dest, const struct Error_t* src);

const int ERR_NOT_ENOUGH_MEMORY_SPACE               = 0x01;
const int ERR_REACHED_AUTOMATION_TASKS_LIMIT        = 0x02;
const int ERR_REACHED_AUTOMATION_DATA_BLOCK_LIMIT   = 0x03;
const int ERR_UNALLOCATED_DATA_BLOCK                = 0x04;
const int ERR_FREED_DATA_BLOCK                      = 0x05;
const int ERR_REACHED_SYSTEMS_LIMIT                 = 0x06;
const int ERR_SYSTEM_UNAVAILABLE                    = 0x07;

#endif