drc off
crashbackups stop
gds read $::env(MACRO)
load [file rootname [file tail $::env(MACRO)]]
save $::env(OUTPUT)/[file rootname [file tail $::env(MACRO)]].mag
quit -noprompt
