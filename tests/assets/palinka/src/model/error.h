#define ERROR_MSG_MAX_SIZE 256
#include <cstdio>

struct Error_t {
    char msg[ERROR_MSG_MAX_SIZE];
    int  code;
};

void write_error(struct Error_t* err, const int code, const char* msg) {
    snprintf(err->msg, ERROR_MSG_MAX_SIZE, msg);
    err->code = code;
}

const int ERR_NOT_ENOUGH_MEMORY_SPACE = 0x01;
const int ERR_REACHED_AUTOMATION_TASKS_LIMIT = 0x02;
const int ERR_REACHED_AUTOMATION_DATA_BLOCK_LIMIT = 0x03;
const int ERR_UNALLOCATED_DATA_BLOCK = 0x03;
const int ERR_FREED_DATA_BLOCK = 0x03;