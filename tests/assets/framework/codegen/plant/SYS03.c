void step_system_SYS03(struct System_t * sys) {
    fb_FP03(sys);
}
void fp_FP03(struct System_t * sys) {
    struct DataBlock_t * idb;
    idb = open_data_block(sys, 0);
    block_bin_output(idb->base[0]);
}