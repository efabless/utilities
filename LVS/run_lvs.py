#!/usr/bin/env python3

# This script is a wrapper to run full LVS using gds, mag, maglef, verilog GL netlist, spice

import subprocess
import os
import argparse

def extract(file_dict, output_dir):
    """extract spice using magic

    Args:
        file_dict (dict): dictionary of input file
        output_dir (string): output directory
    Output:
        creates a tmp_ext directory under the output directory and dumps the .ext files there
        generates the .spice netlist under the output directory
    History:
        created 07/24/2022
    """
    os.environ['ext_inp1'] = file_dict.get("file_path")
    os.environ['ext_out'] = output_dir

    if file_dict.get("file_extraction") is True:
        subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", f"{PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc", f"extract_{file_dict['file_type']}.tcl"])
    elif file_dict.get("file_extraction") is None:
        raise TypeError(f"LVS on {file_dict['file_type']} files not supported")


def run_lvs(netlist_1, netlist_2, output_dir):
    """run generic LVS

    Args:
        netlist_1 (dict): netlist 1 dictionary
        netlist_2 (dict): netlist 2 dictionary
        output_dir (string): output directory
    Output:
        Runs LVS and generates output log under the output directory
    History:
        created 07/21/2022
    """

    if netlist_1.get("file_type") == "gds" or netlist_2.get("file_type") == "gds":
        os.environ['MAGIC_EXT_USE_GDS'] = "1"
    os.environ['NETGEN_COLUMNS'] = "60"
    netlist1_name = os.path.basename(netlist_1.get("file_path")).split('.')[0]
    netlist2_name = os.path.basename(netlist_2.get("file_path")).split('.')[0]

    netgen_setup_file = f"{PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl"
    if netlist_1.get("file_extraction") is True:
        spice_file1 = f"{output_dir}/{netlist1_name}-{netlist_1['file_type']}-extracted.spice"
    else:
        spice_file1 = netlist_1.get("file_path")
    
    if netlist_2.get("file_extraction") is True:
        spice_file2 = f"{output_dir}/{netlist2_name}-{netlist_2['file_type']}-extracted.spice"
    else:
        spice_file2 = netlist_2.get("file_path")

    subprocess.run(['netgen', '-batch', 'lvs', 
        f'{spice_file1} {netlist1_name}',
		f'{spice_file2} {netlist1_name}', 
        f'{netgen_setup_file}', 
        f'{output_dir}/{netlist1_name}-{netlist_1["file_type"]}-vs-{netlist_2["file_type"]}.out'])

def set_ext_files(file_type):
    """checks if the file can be extracted

    Args:
        file_type (string): checks if the file type can be extracted

    Returns:
        [bool]: bool to reflect if the file type can be extracted
    """
    if file_type == "gds" or file_type == "mag":
        file_ext = True
    elif file_type == "spice" or file_type == "v":
        file_ext = False
    else:
        file_ext = None

    return file_ext
    

def set_db(file1_path, file2_path):
    """sets the tuples for the file inputs

    Args:
        file1 (string): path to first input file
        file2 (string): path to second input file

    Returns:
        tuple (string, bool): tuple containing (file1_path, if the file1 can be extracted) and (file2_path, if the file1 can be extracted)
    History:
        created 07/24/2022
    """
    file1_type = os.path.basename(file1_path).split('.')[1]
    file2_type = os.path.basename(file2_path).split('.')[1]
    
    file1_db = {
        "file_path" : file1_path,
        "file_type" : file1_type,
        "file_extraction" : set_ext_files(file1_type)
    }
    file2_db = {
        "file_path" : file2_path,
        "file_type" : file2_type,
        "file_extraction" : set_ext_files(file2_type)
    }

    return file1_db, file2_db

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

    input1_db, input2_db = set_db(input1, input2)
    extract(input1_db, output)
    extract(input2_db, output)
    run_lvs(input1_db, input2_db, output)

    
    

