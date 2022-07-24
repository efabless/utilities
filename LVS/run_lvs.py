#!/usr/bin/env python3

# This script is a wrapper to run full LVS using gds, mag, maglef, verilog GL netlist, spice, cdl

import subprocess
import os
import argparse
import warnings


def extract(
    file_dict: dict,
    output_dir: str
):
    """extract spice using magic

    Args:
        file_dict (dict): dictionary of input file
        output_dir (str): output directory
    Raises:
        TypeError: if LVS doesn't support this file type
    Output:
        creates a tmp_ext directory under the output directory and dumps the .ext files there
        generates the .spice netlist under the output directory
    History:
        created 07/24/2022
    """
    os.environ["ext_inp1"] = file_dict.get("file_path")
    os.environ["ext_out"] = output_dir
    magic_ext_command = [
        "magic",
        "-dnull",
        "-noconsole",
        "-rcfile",
        f"{PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc",
        f"extract_{file_dict['file_type']}.tcl",
    ]

    if file_dict.get("file_extraction") is True:
        std_out = subprocess.run(
            magic_ext_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        )
        decoded_output = std_out.stdout.decode("utf-8")
        print(decoded_output, end="")
        write_stdout_file(
            f'{output_dir}/{file_dict["file_name"]}-magic_extraction.log',
            decoded_output,
        )

    elif file_dict.get("file_extraction") is None:
        raise TypeError(f"LVS on {file_dict['file_type']} files not supported")


def run_lvs(
    netlist_1: dict,
    netlist_2: dict,
    output_dir: str
):
    """run generic LVS

    Args:
        netlist_1 (dict): netlist 1 dictionary
        netlist_2 (dict): netlist 2 dictionary
        output_dir (str): output directory
    Output:
        Runs LVS and generates output log under the output directory
    History:
        created 07/21/2022
    """

    if netlist_1.get("file_type") == "gds" or netlist_2.get("file_type") == "gds":
        os.environ["MAGIC_EXT_USE_GDS"] = "1"
    os.environ["NETGEN_COLUMNS"] = "60"
    netgen_setup_file = f"{PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl"

    if netlist_1.get("file_extraction") is True:
        spice_file1 = f"{output_dir}/{netlist_1['file_name']}-{netlist_1['file_type']}-extracted.spice"
    else:
        spice_file1 = netlist_1.get("file_path")

    if netlist_2.get("file_extraction") is True:
        spice_file2 = f"{output_dir}/{netlist_2['file_name']}-{netlist_2['file_type']}-extracted.spice"
    else:
        spice_file2 = netlist_2.get("file_path")

    netgen_LVS_command = [
        "netgen",
        "-batch",
        "lvs",
        f'{spice_file1} {netlist_1["file_name"]}',
        f'{spice_file2} {netlist_1["file_name"]}',
        f"{netgen_setup_file}",
        f'{output_dir}/{netlist_1["file_name"]}-{netlist_1["file_type"]}-vs-{netlist_2["file_type"]}.out',
    ]

    std_out = subprocess.run(
        netgen_LVS_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )
    decoded_output = std_out.stdout.decode("utf-8")
    print(decoded_output, end="")

    write_stdout_file(
        f'{output_dir}/{netlist_1["file_name"]}-{netlist_1["file_type"]}-vs-{netlist_2["file_type"]}.log',
        decoded_output,
    )


def write_stdout_file(
    output_file: str,
    content: str
):
    """open and write stdout to file

    Args:
        output_file (str): path to output file
        content (str): content of file
    """
    std_out_file = open(output_file, "w")
    std_out_file.write(content)
    std_out_file.close()


def is_extractable(
    file_type: str
):
    """checks if the file can be extracted

    Args:
        file_type (str): checks if the file type can be extracted

    Returns:
        [bool]: bool to reflect if the file type can be extracted
    History:
        created 07/24/2022
    """
    if file_type == "gds" or file_type == "mag":
        file_ext = True
    elif file_type == "spice" or file_type == "v" or file_type == "cdl":
        file_ext = False
    else:
        file_ext = None

    return file_ext


def create_db(
    file1_path: str,
    file2_path: str
):
    """sets the tuples for the file inputs

    Args:
        file1 (str): path to first input file
        file2 (str): path to second input file

    Returns:
        dictionary (str, str, str, bool): dictionary containing (file_path, file_type, file_name, file_extraction)
    History:
        created 07/24/2022
    """
    file1 = os.path.splitext(file1_path)
    file2 = os.path.splitext(file2_path)
    file1_type = os.path.basename(file1[1]).split(".")[1]
    file2_type = os.path.basename(file2[1]).split(".")[1]
    file1_name = os.path.basename(file1[0])
    file2_name = os.path.basename(file2[0])

    file1_db = {
        "file_path": file1_path,
        "file_type": file1_type,
        "file_name": file1_name,
        "file_extraction": is_extractable(file1_type),
    }
    file2_db = {
        "file_path": file2_path,
        "file_type": file2_type,
        "file_name": file2_name,
        "file_extraction": is_extractable(file2_type),
    }

    return file1_db, file2_db

def check_pdk():
    """check PDK_ROOT and PDK env variables

    Raises:
        FileNotFoundError: PDK_ROOT is not exported or doesn't exist

    Returns:
        [str]: PDK_ROOT, PDK
    History:
        created 07/24/2022
    """
    pdk_root = os.getenv("PDK_ROOT")
    pdk = os.getenv("PDK")
    if pdk_root is None and os.path.isdir(pdk_root):
        raise FileNotFoundError(
            "PDK_ROOT doesn't exist, please export PDK_ROOT to the right pdk path"
        )

    if pdk is None or os.path.isdir(pdk):
        warnings.warn("PDK is not exported, will default to sky130B")
        pdk = "sky130B"

    return pdk_root, pdk

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process LVS check. Layout will always be on the left"
    )
    parser.add_argument(
        "-i",
        "--input",
        help="input files to run LVS on them. Takes two input files",
        required=True,
        nargs=2,
    )
    parser.add_argument("-o", "--output", help="output file", required=True)
    args = parser.parse_args()
    PDK_ROOT, PDK = check_pdk()

    input1 = os.path.abspath(args.input[0])
    input2 = os.path.abspath(args.input[1])
    output = os.path.abspath(args.output)

    try:
        os.makedirs(output)
    except FileExistsError:
        # directory already exists
        pass

    input1_db, input2_db = create_db(input1, input2)
    extract(input1_db, output)
    extract(input2_db, output)
    run_lvs(input1_db, input2_db, output)
