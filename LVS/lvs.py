#!/usr/bin/env python3

# This script is a wrapper to run full LVS using gds, mag, maglef, verilog GL netlist, spice, cdl

from multiprocessing.dummy import Array
import subprocess
import os
import argparse
import warnings
import glob

from numpy import array

class Design:
    def __init__(self, file_path):
        self.file_path = file_path
        self.view, self.name = self.initialize()
        self.extract = self.is_extractable()
        self.file_v2s = self.is_v2s()

    def is_extractable(self):
        """checks if the file can be extracted

        Returns:
            [bool]: bool to reflect if the file type can be extracted
        History:
            created 07/25/2022
        """
        extension_type = self.view
        if extension_type == "gds" or extension_type == "mag":
            file_ext = True
        elif extension_type == "spice" or extension_type == "v" or extension_type == "cdl":
            file_ext = False
        else:
            file_ext = None

        return file_ext

    def is_v2s(self):
        """checks if the file can do vlog2spice

        Returns:
            [bool]: bool to reflect if the file type can do vlog2spice
        History:
            created 07/25/2022
        """
        extension_type = self.view
        if extension_type == "v":
            file_ext = True
        else:
            file_ext = False

        return file_ext

    def initialize(self):
        """fills the view and name for self

        Returns:
            dictionary (str, str): path view and file name

        History:
            created 07/24/2022
        """
        file_split = os.path.splitext(self.file_path)
        view = os.path.basename(file_split[1]).split(".")[1]
        name = os.path.basename(file_split[0])

        return view, name

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

    if pdk is None and os.path.join(pdk_root, pdk):
        warnings.warn("PDK is not exported, will default to sky130B")
        pdk = "sky130B"

    return pdk_root, pdk

def extract(
    design: object,
    output_dir: str
):
    """extract spice using magic

    Args:
        design (object): design to extract
        output_dir (str): output directory
    Raises:
        TypeError: if LVS doesn't support this file type
    Output:
        creates a tmp_ext directory under the output directory and dumps the .ext files there
        generates the .spice netlist under the output directory
    History:
        created 07/24/2022
    """
    os.environ["ext_inp1"] = design.file_path
    os.environ["ext_out"] = output_dir
    magic_ext_command = [
        "magic",
        "-dnull",
        "-noconsole",
        "-rcfile",
        f"{PDK_ROOT}/{PDK}/libs.tech/magic/{PDK}.magicrc",
        f"extract_{design.view}.tcl",
    ]

    if design.extract is True:
        std_out = subprocess.run(
            magic_ext_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        )
        decoded_output = std_out.stdout.decode("utf-8")
        print(decoded_output, end="")
        write_stdout_file(
            f'{output_dir}/{design.name}-magic_extraction.log',
            decoded_output,
        )

    elif design.extract is None:
        raise TypeError(f"LVS on {design.view} files not supported")

def run_lvs(
    netlist_1: object,
    netlist_2: object,
    output_dir: str
):
    """run generic LVS

    Args:
        netlist_1 (object): netlist 1 object
        netlist_2 (object): netlist 2 object
        output_dir (str): output directory
    Output:
        Runs LVS and generates output log under the output directory
    History:
        created 07/21/2022
    """

    if netlist_1.view == "gds" or netlist_2.view == "gds":
        os.environ["MAGIC_EXT_USE_GDS"] = "1"
    os.environ["NETGEN_COLUMNS"] = "60"
    netgen_setup_file = f"{PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl"

    if netlist_1.extract is True:
        spice_file1 = f"{output_dir}/{netlist_1.name}-{netlist_1.view}-extracted.spice"
    else:
        spice_file1 = netlist_1.file_path

    if netlist_2.extract is True:
        spice_file2 = f"{output_dir}/{netlist_2.name}-{netlist_2.view}-extracted.spice"
    else:
        spice_file2 = netlist_2.file_path

    netgen_LVS_command = [
        "netgen",
        "-batch",
        "lvs",
        f'{spice_file1} {netlist_1.name}',
        f'{spice_file2} {netlist_1.name}',
        f"{netgen_setup_file}",
        f'{output_dir}/{netlist_1.name}-{netlist_1.view}-vs-{netlist_2.view}.out',
    ]

    std_out = subprocess.run(
        netgen_LVS_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )
    decoded_output = std_out.stdout.decode("utf-8")
    print(decoded_output, end="")

    write_stdout_file(
        f'{output_dir}/{netlist_1.name}-{netlist_1.view}-vs-{netlist_2.view}.log',
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

def vlog2spice(
    netlist: object,
    output_dir: str
):
    vlog_to_spice = f'{output_dir}/{netlist.name}-folded.spice'
    vlog2spice_command = [
        f'{os.path.dirname(os.path.abspath(__file__))}/vlog2Spice',
        f'{netlist.file_path}',
        '-o',
        f'{vlog_to_spice}',
        '-i'
    ]
    v2s_command = vlog2spice_command + get_std_spice()
    
    subprocess.run(v2s_command)
    vlog_to_spice = unfold(vlog_to_spice, output_dir)
    return vlog_to_spice

def get_std_spice():
    lib_include = []
    for file in glob.glob(f'{PDK_ROOT}/{PDK}/libs.ref/*/spice/*_fd_*.spice'):
        lib_include.extend(('-l', file))
    return lib_include

def unfold(
    spice_netlist: str,
    output_dir: str
):
    print(os.path.splitext(spice_netlist))
    tmp_spice_netlist = f'{output_dir}/{os.path.dirname(spice_netlist)}'
    vlog2spice_command = [
        f'{os.path.dirname(os.path.abspath(__file__))}/unfold',
        f'{spice_netlist}',
        '>',
        f'{tmp_spice_netlist}'
    ]
    
    subprocess.run(vlog2spice_command)
    return tmp_spice_netlist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process LVS check."
    )
    parser.add_argument(
        "-i",
        "--input",
        help="input files to run LVS on them. Takes two input files",
        required=True,
        nargs=2,
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="output directory",
        required=True
    )
    parser.add_argument(
        "-bb",
        "--blackbox",
        action="store_true"
    )
    args = parser.parse_args()
    PDK_ROOT, PDK = check_pdk()

    input1 = os.path.abspath(args.input[0])
    input2 = os.path.abspath(args.input[1])
    output = os.path.abspath(args.output_dir)

    try:
        os.makedirs(output)
    except FileExistsError:
        # directory already exists
        pass

    design1 = Design(input1)
    design2 = Design(input2)
    
    if design1.extract:
        extract(design1, output)
    if design2.extract:
        extract(design2, output)

    if not args.blackbox:
        if design1.file_v2s:
            design1 = Design(vlog2spice(design1, output))
        if design2.file_v2s:
            design2 = Design(vlog2spice(design2, output))
    run_lvs(design1, design2, output)
