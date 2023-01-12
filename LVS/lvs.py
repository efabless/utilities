#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: Apache-2.0

# This script is a wrapper to run full LVS using gds, mag, maglef, verilog GL netlist, spice, cdl

import subprocess
import os
import argparse
import warnings
import glob
import sys
from verilog_parser import VerilogParser
from typing import List

from colorama import Fore, Back, Style


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
        elif (
            extension_type == "spice"
            or extension_type == "v"
            or extension_type == "cdl"
        ):
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
    if "PDK_ROOT" in os.environ:
        pdk_root = os.getenv("PDK_ROOT")
        if not os.path.isdir(pdk_root):
            raise FileNotFoundError(
                Fore.RED
                + f"path {pdk_root} doesn't exist, export PDK_ROOT to the right pdk path"
            )
    else:
        sys.exit(
            Fore.RED + "PDK_ROOT is not exported, export PDK_ROOT to the right pdk path"
        )
    if "PDK" in os.environ:
        pdk = os.getenv("PDK")
        if not os.path.isdir(os.path.join(pdk_root, pdk)):
            sys.exit(
                Fore.RED
                + f"technology {pdk} can't be found, export PDK to the correct technology"
            )
    else:
        sys.exit(Fore.RED + "PDK is not defined, export PDK to the correct technology")

    return pdk_root, pdk


def extract(design: object, output_dir: str):
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
        f"{os.path.dirname(os.path.abspath(__file__))}/extract_{design.view}.tcl",
    ]

    if design.extract is True:
        with open(f"{output_dir}/{design.name}-magic_extraction.log", "wb") as f:
            std_out = subprocess.Popen(
                magic_ext_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
            )
            with open(f"{output_dir}/{design.name}-magic_extraction.log", "w") as f:
                while True:
                    output = std_out.stdout.readline()
                    if std_out.poll() is not None:
                        break
                    if output:
                        out = output.decode("utf-8")
                        print(out)
                        f.write(out)

    elif design.extract is None:
        raise TypeError(f"LVS on {design.view} files not supported")


def run_lvs(netlist_1: object, netlist_2: object, output_dir: str, setup_file):
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
    netgen_LVS_command = ["netgen", "-batch", "source", f"{setup_file}"]

    std_out = subprocess.Popen(
        netgen_LVS_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )
    with open(
        f"{output_dir}/{netlist_1.name}-{netlist_1.view}-vs-{netlist_2.view}.log", "w"
    ) as f:
        while True:
            output = std_out.stdout.readline()
            if std_out.poll() is not None:
                break
            if output:
                out = output.decode("utf-8")
                print(out)
                f.write(out)


def write_stdout_file(output_file: str, content: str):
    """open and write stdout to file

    Args:
        output_file (str): path to output file
        content (str): content of file
    """
    std_out_file = open(output_file, "a")
    std_out_file.write(content)
    std_out_file.close()


def get_macros(lef_file: str) -> List[str]:
    macros = []
    with open(lef_file) as f:
        for line in f.readlines():
            if "MACRO" in line:
                macro_name = line.split()[1]
                macros.append(macro_name)
    return macros


def get_pdk_lefs_paths(pdk_path: str) -> List[str]:
    lef_paths = []
    for root, dirs, files in os.walk(pdk_path):
        for file in files:
            filename, file_extension = os.path.splitext(f"{file}")
            if file_extension == ".lef":
                lef_paths.append(f"{root}/{file}")
    return lef_paths


def get_std_spice():
    """Fetches the library spice from the PDK_ROOT

    Returns:
        Array: Array of paths to library spice netlists
    """
    lib_include = []
    for file in glob.glob(f"{PDK_ROOT}/{PDK}/libs.ref/*/spice/*.spice"):
        if os.path.isfile(file):
            lib_include.append(file)
    return lib_include


def check_hierarchy(pdk_path, netlist_2):
    lef_paths = get_pdk_lefs_paths(pdk_path)
    pdk_macros = []
    non_pdk_macros = []
    for lef in lef_paths:
        pdk_macros = pdk_macros + get_macros(lef)

    parsed = VerilogParser(netlist_2.file_path)
    for instance in parsed.instances:
        macro = parsed.instances[instance]
        if macro not in pdk_macros:
            non_pdk_macros.append(macro)
    non_pdk_macros = list(set(non_pdk_macros))
    return non_pdk_macros


def create_netgen_setup_file(
    netlist_1: object,
    netlist_2: object,
    output_dir: str,
    spice,
    verilog_includes,
    abstract,
    verilog_directory,
    non_pdk_macros,
    blackbox,
    setup_file,
    pdk,
):

    netgen_setup_file = open(setup_file, "w")

    if netlist_1.view == "gds" or netlist_2.view == "gds":
        os.environ["MAGIC_EXT_USE_GDS"] = "1"
    os.environ["NETGEN_COLUMNS"] = "90"

    if netlist_1.extract is True:
        spice_file1 = f"{output_dir}/{netlist_1.name}-{netlist_1.view}-extracted.spice"
        netgen_setup_file.write(f"set circuit1 [readnet spice {spice_file1}]\n")
    else:
        print("circuit 2 has to be spice")
        sys.exit()

    pdk_spice = get_std_spice()
    count = 0
    for sp in pdk_spice:
        if "sky130_fd_pr" not in sp:
            if count == 0:
                netgen_setup_file.write(f"set circuit2 [readnet spice {sp}]\n")
                count = 1
            else:
                netgen_setup_file.write(f"readnet spice {sp} $circuit2\n")
    if spice:
        for s in spice:
            netgen_setup_file.write(f"readnet spice {s} $circuit2\n")
            non_pdk_macros.remove(os.path.splitext(os.path.basename(s))[0])
    if verilog_includes:
        for v in verilog_includes:
            netgen_setup_file.write(f"readnet verilog {v} $circuit2\n")
            non_pdk_macros.remove(os.path.splitext(os.path.basename(v))[0])

    non_pdk_macros_cp = non_pdk_macros.copy()

    if verilog_directory:
        for macro in non_pdk_macros:
            verilog_file = os.path.join(verilog_directory, f"{macro}.v")
            if os.path.isfile(verilog_file):
                netgen_setup_file.write(f"readnet verilog {verilog_file} $circuit2\n")
                non_pdk_macros_cp.remove(os.path.splitext(os.path.basename(macro))[0])
            else:
                sys.exit(
                    Fore.RED
                    + f"{verilog_file} couldn't be found, please check if file exisits"
                )

    if len(non_pdk_macros_cp) != 0 and not blackbox:
        sys.exit(
            Fore.RED
            + f"some macros in the hierarchy could not be found: {non_pdk_macros}"
        )

    if netlist_2.extract is True:
        print("circuit 2 has to be verilog")
        sys.exit()
    else:
        spice_file2 = netlist_2.file_path
        netgen_setup_file.write(f"readnet verilog {spice_file2} $circuit2\n")

    netgen_setup_file.write("set cells1 [cells list -all $circuit1]\n")
    netgen_setup_file.write("set cells2 [cells list -all $circuit2]\n")
    netgen_setup_file.write("foreach cell \$cells1 {\n")
    netgen_setup_file.write('    if {[regexp ".._(.+)" $cell match cellname]} {\n')
    netgen_setup_file.write(
        "        if {([lsearch $cells2 $cell] < 0) && ([lsearch $cells2 $cellname] >= 0) && ([lsearch $cells1 $cellname] < 0)} {\n"
    )
    netgen_setup_file.write(
        '            equate classes "$circuit1 $cell" "$circuit2 $cellname"\n'
    )
    netgen_setup_file.write(
        '            equate pins "$circuit1 $cell" "$circuit2 $cellname"\n        }\n    }\n'
    )
    netgen_setup_file.write(
        "    if {[regexp {.._sky130_fd_sc_[^_]+__fill_[[:digit:]]+} \$cell match]} {\n"
    )
    netgen_setup_file.write('	ignore class "$circuit1 $cell"\n    }\n}\n')
    if "sky130" in pdk:
        netgen_setup_file.write("foreach cell \$cells1 {\n")
        netgen_setup_file.write('    if {[regexp {([A-Z][A-Z0-9]_)*sky130_sram_([^_]+)_([^_]+)_([^_]+)_([^_]+)_(.+)} $cell match prefix memory_size memory_type matrix io cellname]} {\n')
        netgen_setup_file.write('	    if {([lsearch $cells2 $cell] < 0) && \\\n')
        netgen_setup_file.write('   		([lsearch $cells2 $cellname] >= 0) && \\\n')
        netgen_setup_file.write('   		([lsearch $cells1 $cellname] < 0)} { \n')
        netgen_setup_file.write('	    equate classes \"-circuit2 $cellname\" \"-circuit1 $cell\"\n	}\n    }\n}\n')

        netgen_setup_file.write("foreach cell \$cells1 {\n")
        netgen_setup_file.write('    if {[regexp {([A-Z][A-Z0-9]_)*(.*)} $cell match prefix cellname]} {\n')
        netgen_setup_file.write('	    if {([lsearch $cells2 $cell] < 0) && \\\n')
        netgen_setup_file.write('   		([lsearch $cells2 $cellname] >= 0)} {\n')
        netgen_setup_file.write('   		equate classes "-circuit2 $cellname" "-circuit1 $cell"\n')
        netgen_setup_file.write('   		if  { [lsearch $cells1 $cellname] > 0 } {"\n')
        netgen_setup_file.write('   		    equate classes \"-circuit2 $cellname\" \"-circuit1 $cellname\"\n   		}\n	    }\n    }\n}\n')

    if abstract:
        for a in abstract:
            netgen_setup_file.write(f'flatten class "$circuit2 {a}"\n')

    netgen_setup_file.write(
        f'lvs "$circuit1 {netlist_1.name}" "$circuit2 {netlist_1.name}" {PDK_ROOT}/{PDK}/libs.tech/netgen/{PDK}_setup.tcl {output_dir}/{netlist_1.name}-{netlist_1.view}-vs-{netlist_2.view}.out -json\n'
    )

    netgen_setup_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process LVS check.")
    parser.add_argument(
        "-i",
        "--input",
        help="input files to run LVS on them. Takes two input files",
        required=True,
        nargs=2,
    )
    parser.add_argument("-o", "--output_dir", help="output directory", required=True)
    parser.add_argument(
        "-bb", "--blackbox", help="run LVS in blackbox mode", action="store_true"
    )
    parser.add_argument(
        "-f",
        "--force",
        help="force vlog2spice to run and overcome hierarchy errors",
        action="store_true",
    )
    parser.add_argument(
        "-v", "--verilog", help="includes other verilog modules", nargs="+"
    )
    parser.add_argument(
        "-vd",
        "--verilog_directory",
        help="verilog directory which has all the gl verilogs",
    )
    parser.add_argument("-s", "--spice", help="abstract cells", nargs="+")
    parser.add_argument("-abs", "--abstract", help="abstract cells", nargs="+")
    args = parser.parse_args()
    PDK_ROOT, PDK = check_pdk()

    input1 = os.path.abspath(args.input[0])
    input2 = os.path.abspath(args.input[1])
    output = os.path.abspath(args.output_dir)
    force = args.force
    verilog = args.verilog
    verilog_directory = args.verilog_directory
    spice = args.spice
    abstract = args.abstract
    setup_file = f"{os.path.dirname(os.path.abspath(__file__))}/netgen_setup_file.tcl"

    try:
        os.makedirs(output)
    except FileExistsError:
        # directory already exists
        pass

    design1 = Design(input1)
    design2 = Design(input2)
    non_pdk_macros = check_hierarchy(os.path.join(PDK_ROOT, PDK), design2)

    if non_pdk_macros:
        if not args.blackbox and not verilog_directory and not verilog and not spice:
            sys.exit(
                Fore.RED
                + "To run full transistor level LVS you need to use --verilog_directory or --verilog or --spice to include the hierarchy macros"
            )

    create_netgen_setup_file(
        design1,
        design2,
        output,
        spice,
        verilog,
        abstract,
        verilog_directory,
        non_pdk_macros,
        args.blackbox,
        setup_file,
        PDK,
    )

    if design1.extract:
        extract(design1, output)
    elif design2.extract:
        print("spice or gds should be circuit 1")
        sys.exit()

    run_lvs(design1, design2, output, setup_file)
    # os.remove(setup_file)
