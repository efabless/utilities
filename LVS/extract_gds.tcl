set extdir $::env(ext_out)/tmp_ext
file mkdir $extdir
cd $extdir
crashbackups stop
drc off
gds readonly true
gds flatten true
gds rescale false
tech unlock *
cif istyle sky130(vendor)
gds read $::env(ext_inp1)
load [file rootname [file tail $::env(ext_inp1)]] -dereference
select top cell
extract do local
extract all
ext2spice lvs
ext2spice -o $::env(ext_out)/[file rootname [file tail $::env(ext_inp1)]]-gds-extracted.spice
exit
