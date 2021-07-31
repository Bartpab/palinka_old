void step_system_SYS02(struct System_t * sys) {
    fb_FP02(sys);
}
void fp_FP02(struct System_t * sys) {
    struct DataBlock_t * idb;
    idb = open_data_block(sys, 0);
    block_neg(idb->base[0], idb->base[1]);
}