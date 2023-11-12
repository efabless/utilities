drc off
crashbackups stop
if { $::env(MAG_TO_LEF) } {
    load $::env(MACRO)
}
if { $::env(GDS_TO_LEF) } {
    gds read $::env(MACRO)
    load [file rootname [file tail $::env(MACRO)]]
}
if { $::env(DEF_TO_LEF) } {
    lef read $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sky130_fd_sc_hd/techlef/sky130_fd_sc_hd__nom.tlef
    def read $::env(MACRO)
    load [file rootname [file tail $::env(MACRO)]]
}
select top cell
expand
lef write $::env(OUTPUT)/[file rootname [file tail $::env(MACRO)]].lef -hide
quit -noprompt
