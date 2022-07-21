#!/usr/bin/env python

# This script is a wrapper to run full LVS using gds, mag, maglef

import subprocess
import os
import argparse

# This function is to extract gds to spice calling extract_gds.tcl script
# arguments to the function:
#               ext_file --> gds file absolute path to get extracted
#               output_dir --> output directory
# output of the function:
#               creates a tmp_ext directory under the output directory and dumps the .ext files there
#               generates the .spice netlist under the output directory
#
# Date created: 07/21/2022

def extract_gds(ext_file, output_dir):
    os.environ['ext_inp1'] = ext_file
    os.environ['ext_out'] = output_dir

    subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", f"{PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc", "extract_gds.tcl"])

# This function is to run LVS on spice generated with gds, and verilog GL netlist
# arguments to the function:
#               netlist_1 --> spice netlist
#               netlist_2 --> verilog GL netlist
#               output_dir --> output directory
# output of the function:
#               Runs LVS and generates output log under the output directory
#
# Date created: 07/21/2022

def run_lvs_gds(netlist_1, netlist_2, output_dir):
    os.environ['NETGEN_COLUMNS'] = "60"
    os.environ['MAGIC_EXT_USE_GDS'] = "1"
    netlist1_name = os.path.basename(netlist_1).split('.')[0]

    subprocess.run(['netgen', '-batch', 'lvs', f'{output_dir}/{netlist1_name}-gds-extracted.spice {netlist1_name}',
		f'{netlist_2} {netlist1_name}', f'{PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl', 
        f'{output_dir}/{netlist1_name}-gds-vs-verilog.out'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process LVS check. Layout will always be on the left')
    parser.add_argument('-i', '--input', help="takes two input files", required=True, nargs=2)
    parser.add_argument('-o', '--output', help="output file", required=True)
    args = parser.parse_args()
    PDK_ROOT=os.getenv('PDK_ROOT')
    PDK=os.getenv('PDK')

    input1 = os.path.abspath(args.input[0])
    input2 = os.path.abspath(args.input[1])
    output = os.path.abspath(args.output)

    try:
        os.makedirs(output)
    except FileExistsError:
        # directory already exists
        pass

    input1_type = os.path.basename(input1).split('.')[1]
    input2_type = os.path.basename(input2).split('.')[1]

    if input1_type == "gds" or input2_type == "gds":
        lvs_type = "gds"
        if input1_type == "gds":
            extract_gds(input1, output)
            run_lvs_gds(input1, input2, output)
        elif input2_type == "gds":
            extract_gds(input2, output)
            run_lvs_gds(input2, input1, output)

