set extdir $::env(ext_out)/tmp_ext
file mkdir $extdir
cd $extdir
crashbackups stop
drc off
gds flatten true
gds noduplicates true
gds read $::env(ext_inp1)
load [file rootname [file tail $::env(ext_inp1)]] -dereference
select top cell
expand
extract do local
extract no all
extract unique
extract all
ext2spice lvs
ext2spice -o $::env(ext_out)/[file rootname [file tail $::env(ext_inp1)]]-gds-extracted.spice [file rootname [file tail $::env(ext_inp1)]].ext
exit
