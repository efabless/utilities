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
        f"{os.path.dirname(os.path.abspath(__file__))}/extract_{design.view}.tcl",
    ]

    if design.extract is True:
        with open(f'{output_dir}/{design.name}-magic_extraction.log', "wb") as f:
            std_out = subprocess.Popen(
                magic_ext_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
            )
            with open(f'{output_dir}/{design.name}-magic_extraction.log', "w") as f:
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

    std_out = subprocess.Popen(
        netgen_LVS_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )
    with open(f'{output_dir}/{netlist_1.name}-{netlist_1.view}-vs-{netlist_2.view}.log', "w") as f:
                while True:
                    output = std_out.stdout.readline()
                    if std_out.poll() is not None:
                        break
                    if output:
                        out = output.decode("utf-8")
                        print(out)
                        f.write(out)

def write_stdout_file(
    output_file: str,
    content: str
):
    """open and write stdout to file

    Args:
        output_file (str): path to output file
        content (str): content of file
    """
    std_out_file = open(output_file, "a")
    std_out_file.write(content)
    std_out_file.close()

def vlog2spice(
    netlist: object,
    output_dir: str,
    force: bool,
    verilog_includes
):
    """utilize vlog2spice binary from qflow to extract spice from gl netlist

    Args:
        netlist (object): object discribing the netlist
        output_dir (str): output directory
        force (bool): force flag

    Returns:
        str: path to output from vlog2spice
    """
    vlog_to_spice = f'{output_dir}/{netlist.name}.spice'
    vlog2spice_command = [
        f'{os.path.dirname(os.path.abspath(__file__))}/vlog2Spice',
        f'{netlist.file_path}',
        '-o',
        f'{vlog_to_spice}',
        '-i'
    ]
    v2s_includes = []
    if len(verilog_includes) > 0:
        for v in verilog_includes:
            v2s_includes.extend(('-l', v.file_path))
    v2s_command = vlog2spice_command + get_std_spice() + v2s_includes
    
    std_out = subprocess.run(
        v2s_command, capture_output=True
    )
    out, err = std_out.stdout.decode("utf-8"), std_out.stderr.decode("utf-8")
    
    if out or err:
        print(out + err)

    write_stdout_file(
        f'{output_dir}/{netlist.name}-vlog2spice.log',
        out + err,
    )
    if err.find('subcircuit') != -1 and not force:
        sys.exit('ERROR: Please define the above subcircuits for transistor level LVS')
    
    unfold(vlog_to_spice)
    return vlog_to_spice

def get_std_spice():
    """Fetches the library spice from the PDK_ROOT

    Returns:
        Array: Array of paths to library spice netlists
    """
    lib_include = []
    for file in glob.glob(f'{PDK_ROOT}/{PDK}/libs.ref/*'):
        std_spice_file = f'{file}/spice/{os.path.basename(file)}.spice'
        if os.path.isfile(std_spice_file):
            lib_include.extend(('-l', std_spice_file))
    return lib_include

def unfold(
    spice_netlist: str
):
    """unfolds the spice netlist coming from vlog2spice, to abide by netgen guidlines
        Preserves header comments but removes any comments inside the subckt block

    Args:
        spice_netlist (str): path to the spice netlist
    """
    updated_data = ''

    with open(spice_netlist, 'r+') as file:
        file_content = file.readlines()
        for line in file_content:

            comment_index = 0

            if line.startswith('+'):
                if updated_data.find('*') != -1:
                    comment_index = updated_data.index('*')
                updated_line = line[1:]
                updated_data = f'{updated_data[:comment_index - 1]}' + f'{updated_line}'
            else:
                updated_data += line
                
        file.seek(0)
        file.truncate()
        file.write(updated_data)

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
        help="run LVS in blackbox mode",
        action="store_true"
    )
    parser.add_argument(
        "-f",
        "--force",
        help="force vlog2spice to run and overcome hierarchy errors",
        action="store_true"
    )
    parser.add_argument(
        "-v",
        "--verilog",
        help="includes other verilog modules",
        nargs='+'
    )
    args = parser.parse_args()
    PDK_ROOT, PDK = check_pdk()

    input1 = os.path.abspath(args.input[0])
    input2 = os.path.abspath(args.input[1])
    output = os.path.abspath(args.output_dir)
    force = args.force
    verilog = args.verilog

    try:
        os.makedirs(output)
    except FileExistsError:
        # directory already exists
        pass

    
    verilog_includes = []
    if verilog:
        for includes in verilog:
            v_include = Design(os.path.abspath(includes))
            verilog_includes.append(Design(vlog2spice(v_include, output, force, "")))

    design1 = Design(input1)
    design2 = Design(input2)
    
    if not args.blackbox:
        if design1.file_v2s:
            design1 = Design(vlog2spice(design1, output, force, verilog_includes))
        if design2.file_v2s:
            design2 = Design(vlog2spice(design2, output, force, verilog_includes))

    if design1.extract:
        extract(design1, output)
    if design2.extract:
        extract(design2, output)
    
    run_lvs(design1, design2, output)
