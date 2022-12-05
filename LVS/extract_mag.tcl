set extdir $::env(ext_out)/tmp_ext
file mkdir $extdir
cd $extdir
crashbackups stop
drc off
load $::env(ext_inp1)
cellname list filepath [file rootname [file tail $::env(ext_inp1)]] [file dirname $::env(ext_inp1)]
flush [file rootname [file tail $::env(ext_inp1)]]
select top cell
expand
extract do local
extract all
ext2spice lvs
ext2spice -o $::env(ext_out)/[file rootname [file tail $::env(ext_inp1)]]-mag-extracted.spice
exit
