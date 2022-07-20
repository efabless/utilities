#!/usr/bin/env python

import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description='Process LVS check.')
parser.add_argument('-i1', '--input1', help="first input file", required=True)
parser.add_argument('-i2', '--input2', help="second input file", required=True)
parser.add_argument('-o', '--output', help="output file", required=True)
args = parser.parse_args()
PDK_ROOT=os.getenv('PDK_ROOT')
PDK=os.getenv('PDK')
input1 = os.path.abspath(args.input1)
input2 = os.path.abspath(args.input2)
output = os.path.abspath(args.output)

def extract_gds():
    os.environ['ext_inp1'] = input1
    os.environ['ext_inp2'] = input2
    os.environ['ext_out'] = output

    try:
        os.makedirs(args.output)
    except FileExistsError:
        # directory already exists
        pass

    subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", f"{PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc", "extract_gds.tcl"])

def run_lvs_gds():
    os.environ['NETGEN_COLUMNS'] = "60"
    os.environ['MAGIC_EXT_USE_GDS'] = "1"
    input1_name = os.path.basename(input1).split('.')[0]

    subprocess.run(['netgen', '-batch', 'lvs', f'{output}/{input1_name}-gds-extracted.spice {input1_name}',
		f'{input2} {input1_name}', f'{PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl', 
        f'{output}/{input1_name}-gds-vs-verilog.out'])

if __name__ == "__main__":
    extract_gds()
    run_lvs_gds()

