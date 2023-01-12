yosys -import

read_verilog $::env(YOSYS_VERILOG_IN)
json -o $::env(YOSYS_JSON_OUT)