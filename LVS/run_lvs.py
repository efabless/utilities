#!/usr/bin/env python3

# This script is a wrapper to run full LVS using gds, mag, maglef

import subprocess
import os
import argparse

def extract_gds(ext_file, output_dir):
    """Extract gds to spice calling extract_gds.tcl script

    Args:
        ext_file (string): gds file absolute path to get extracted
        output_dir (string): output directory
    Output:
        creates a tmp_ext directory under the output directory and dumps the .ext files there
        generates the .spice netlist under the output directory
    History:
        created 07/21/2022
    """

    os.environ['ext_inp1'] = ext_file
    os.environ['ext_out'] = output_dir

    subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", f"{PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc", "extract_gds.tcl"])

def extract_mag(ext_file, output_dir):
    """Extract mag or maglef to spice calling extract_mag.tcl script

    Args:
        ext_file (string): mag file absolute path to get extracted
        output_dir (string): output directory
    Output:
        creates a tmp_ext directory under the output directory and dumps the .ext files there
        generates the .spice netlist under the output directory
    History:
        created 07/21/2022
    """

    os.environ['ext_inp1'] = ext_file
    os.environ['ext_out'] = output_dir

    subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", f"{PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc", "extract_mag.tcl"])

def run_lvs(netlist_1, netlist_2, output_dir, lvs_type):
    """AI is creating summary for run_lvs

    Args:
        netlist_1 (string): spice netlist
        netlist_2 (string): verilog GL netlist
        output_dir (string): output directory
        lvs_type (string): type of lvs done: gds or mag
    Output:
        Runs LVS and generates output log under the output directory
    History:
        created 07/21/2022
    """

    if lvs_type == "gds":
        os.environ['MAGIC_EXT_USE_GDS'] = "1"
    os.environ['NETGEN_COLUMNS'] = "60"
    netlist1_name = os.path.basename(netlist_1).split('.')[0]

    subprocess.run(['netgen', '-batch', 'lvs', f'{output_dir}/{netlist1_name}-gds-extracted.spice {netlist1_name}',
		f'{netlist_2} {netlist1_name}', f'{PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl', 
        f'{output_dir}/{netlist1_name}-{lvs_type}-vs-verilog.out'])

def run_ext(input1, input2, output):
    """Chooses which extraction to run based on file extension

    Args:
        input1 (string): path to input file 1
        input2 (string): path to input file 2
        output (string): path to output file
    History:
        created 07/21/2022
    """

    input1_type = os.path.basename(input1).split('.')[1]
    input2_type = os.path.basename(input2).split('.')[1]

    if input1_type == "gds" or input2_type == "gds":
        lvs_type = "gds"
        if input1_type == "gds":
            extract_gds(input1, output)
            run_lvs(input1, input2, output, lvs_type)
        elif input2_type == "gds":
            extract_gds(input2, output)
            run_lvs(input2, input1, output, lvs_type)

    if input1_type == "mag" or input2_type == "mag":
        lvs_type = "mag"
        if input1_type == "mag":
            extract_mag(input1, output)
            run_lvs(input1, input2, output, lvs_type)
        elif input2_type == "mag":
            extract_mag(input2, output)
            run_lvs(input2, input1, output, lvs_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process LVS check. Layout will always be on the left')
    parser.add_argument('-i', '--input', help="input files to run LVS on them. Takes two input files", required=True, nargs=2)
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

    run_ext(input1, input2, output)

    
    

