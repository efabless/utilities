drc off
crashbackups stop
gds read $::env(MACRO)
load [file rootname [file tail $::env(MACRO)]]
select top cell
expand
extract do local
extract no all
extract unique
extract all
def write [file rootname [file tail $::env(MACRO)]].def -units 1000
quit -noprompt