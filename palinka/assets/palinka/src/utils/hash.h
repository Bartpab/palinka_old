#ifndef __HASH_H__
#define __HASH_H__

/**
 * \brief djb2 hash function
 */
long djb2(char *str)
{
    long hash = 5381;
    int c;

    while (c = *str++)
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash;
}

#endif