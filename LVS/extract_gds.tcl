set extdir $::env(ext_out)/tmp_ext
file mkdir $extdir
cd $extdir
crashbackups stop
drc off

# # ! This recipe taken from open_pdks/sky130/custom/scripts/gds_import_io.tcl
# gds flatten true
# gds flatglob *_cdns_*
# gds flatglob *sky130_fd_pr__*_example_*
# # ! flatten within the 120x2 ESD device
# gds flatglob *sky130_fd_io__gnd2gnd_*
# # The following cells have to be flattened for the gpiov2 pad to read in
# # correctly, and produce a layout that can be extracted and generate an
# # LVS clean netlist.
# ### flatten within the analog mux isolated P region
# gds flatglob *sky130_fd_io__amx*
# gds flatglob *sky130_fd_io__xor*
# gds flatglob *sky130_fd_io__gpiov2_amx*
# gds flatglob *sky130_fd_io__gpiov2_amux*
# ### flatten within the isolated VSSIO domain
# gds flatglob *sky130_fd_io__feas_com_pupredrvr*
# gds flatglob *sky130_fd_io__com_pupredrvr_strong_slowv2*
# gds flatglob *sky130_fd_io__com_pdpredrvr_pbiasv2*
# gds flatglob *sky130_fd_io__gpiov2_pdpredrvr_strong*
# ### flatten in opathv2
# gds flatglob *sky130_fd_io__com_pudrvr_strong_slowv2*
# gds flatglob *sky130_fd_io__com_pdpredrvr_strong_slowv2*
# gds flatglob *sky130_fd_io__gpiov2_obpredrvr*
# gds flatglob *sky130_fd_io__hvsbt_*
# ### flatten in ipath
# gds flatglob *sky130_fd_io__gpiov2_ictl_logic*
# ### avoid splitting a netlist that passes in contorted ways through the
# ### layout hierarchy
# gds flatglob *sky130_fd_io__gpio_pddrvr_strong_slowv2*
# gds flatglob *sky130_fd_io__gpiov2_pddrvr_strong*
# gds read $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sky130_fd_io/gds/sky130_fd_io.gds
# gds read $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sky130_fd_io/gds/sky130_ef_io.gds

gds flatten true
gds flatglob *_sram_*
gds read $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sky130_sram_macros/gds/sky130_sram_2kbyte_1rw1r_32x512_8.gds
gds noduplicates true
gds read $::env(ext_inp1)
load sky130_sram_2kbyte_1rw1r_32x512_8
property LEFview true
load [file rootname [file tail $::env(ext_inp1)]]
select top cell
expand
extract do local
extract no all
extract unique
extract all
ext2spice lvs
ext2spice -o $::env(ext_out)/[file rootname [file tail $::env(ext_inp1)]]-gds-extracted.spice [file rootname [file tail $::env(ext_inp1)]].ext
exit
