void step_system_SYS01(struct System_t * sys) {
    fb_FP01(sys);
}
void fp_FP01(struct System_t * sys) {
    struct DataBlock_t * idb;
    idb = open_data_block(sys, 0);
    block_bin_input(idb->base[0]);
}