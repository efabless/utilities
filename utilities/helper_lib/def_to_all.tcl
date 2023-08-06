drc off
crashbackups stop
lef read $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sky130_fd_sc_hd/techlef/sky130_fd_sc_hd__nom.tlef
lef read $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sky130_fd_sc_hvl/techlef/sky130_fd_sc_hvl__nom.tlef
if {  [info exist ::env(EXTRA_LEFS)] } {
    foreach lef_file $::env(EXTRA_LEFS) {
        lef read $lef_file
    }
}
def read $::env(MACRO)
load [file rootname [file tail $::env(MACRO)]]
select top cell
expand
if { $::env(DEF_TO_MAG) } {
    save $::env(OUTPUT)/[file rootname [file tail $::env(MACRO)]].mag
}

if { $::env(DEF_TO_GDS) } {
    gds readonly true
    gds rescale false
    if {  [info exist ::env(EXTRA_GDS_FILES)] } {
		set gds_files_in $::env(EXTRA_GDS_FILES)
		foreach gds_file $gds_files_in {
			gds read $gds_file
		}
	}
    load [file rootname [file tail $::env(MACRO)]]
    select top cell
    expand
    cif *hier write disable
    cif *array write disable
    if { $::env(MAGIC_GDS_ALLOW_ABSTRACT) } { 
        gds abstract allow
    }

	gds write $::env(OUTPUT)/[file rootname [file tail $::env(MACRO)]].gds
}
quit -noprompt
