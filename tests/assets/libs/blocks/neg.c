#include "libs/blocks/neg.h"

void block_neg(char* input, char* output)
{
    *output = !*input;
}