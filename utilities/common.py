#!/usr/bin/env python3
# Copyright 2022 Efabless Corporation
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
import os
import subprocess

def gds_to_mag(
    console, gds_file, output, pdk_root, pdk
):
    magic_env = dict()
    if not os.path.exists(gds_file):
        console.print(f"[red]ERROR : {gds_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = gds_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/gds_to_mag.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def mag_to_gds(
    console, mag_file, maglef_macro, mag_dir, gds_macro, output, pdk_root, pdk
):
    magic_env = dict()
    if not os.path.exists(mag_file):
        console.print(f"[red]ERROR : {mag_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = mag_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    if maglef_macro:
        mag_export = ""
        for maglefs in maglef_macro:
            if not os.path.exists(maglefs):
                console.print(f"[red]ERROR : {maglefs} path doesn't exist")
                exit(1)
            else:
                mag_export = mag_export + maglefs + " "
        magic_env['MAGLEF_MACRO'] = f'"{mag_export.strip()}"'
    if gds_macro:
        gds_export = ""
        for gds in gds_macro:
            if not os.path.exists(gds):
                console.print(f"[red]ERROR : {gds} path doesn't exist")
                exit(1)
            else:
                gds_export = gds_export + gds + " "
        magic_env['GDS_MACRO'] = f'"{gds_export.strip()}"'
    if mag_dir:
        mag_export = ""
        for mags in mag_dir:
            if not os.path.exists(mags):
                console.print(f"[red]ERROR : {mags} path doesn't exist")
                exit(1)
            else:
                mag_export = mag_export + mags + " "
        magic_env['MAG_DIR'] = f'"{mag_export.strip()}"'
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/mag_to_gds.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def gds_to_def(
    console, gds_file, output, pdk_root, pdk
):
    magic_env = dict()
    if not os.path.exists(gds_file):
        console.print(f"[red]ERROR : {gds_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = gds_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/gds_to_def.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def mag_to_def(
    console, mag_file, maglef_macro, mag_dir, gds_macro, output, pdk_root, pdk
):
    magic_env = dict()
    if not os.path.exists(mag_file):
        console.print(f"[red]ERROR : {mag_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = mag_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    if maglef_macro:
        mag_export = ""
        for maglefs in maglef_macro:
            if not os.path.exists(maglefs):
                console.print(f"[red]ERROR : {maglefs} path doesn't exist")
                exit(1)
            else:
                mag_export = mag_export + maglefs + " "
        magic_env['MAGLEF_MACRO'] = f'"{mag_export.strip()}"'
    if gds_macro:
        gds_export = ""
        for gds in gds_macro:
            if not os.path.exists(gds):
                console.print(f"[red]ERROR : {gds} path doesn't exist")
                exit(1)
            else:
                gds_export = gds_export + gds + " "
        magic_env['GDS_MACRO'] = f'"{gds_export.strip()}"'
    if mag_dir:
        mag_export = ""
        for mags in mag_dir:
            if not os.path.exists(mags):
                console.print(f"[red]ERROR : {mags} path doesn't exist")
                exit(1)
            else:
                mag_export = mag_export + mags + " "
        magic_env['MAG_DIR'] = f'"{mag_export.strip()}"'
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/mag_to_def.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def drc(console, gds_file, output_path, pdk):
    gds_file = os.path.abspath(gds_file)
    output_path = os.path.abspath(output_path)
    precheck_root = os.path.join(os.path.expanduser("~"), "mpw_precheck")
    if not os.path.exists(precheck_root):
        subprocess.run(['git', 'clone', 'https://github.com/efabless/mpw_precheck.git', precheck_root])
    if not os.path.exists(f'{output_path}/logs'):
        os.mkdir(f'{output_path}/logs')
    if not os.path.exists(f'{output_path}/outputs'):
        os.mkdir(f'{output_path}/outputs')
    if not os.path.exists(f'{output_path}/outputs/reports'):
        os.mkdir(f'{output_path}/outputs/reports')
    subprocess.run(['python3', f'{precheck_root}/checks/drc_checks/klayout/klayout_gds_drc_check.py', '-g', f'{gds_file}', '-o', f'{output_path}', '-f', '-b', '-og', '-p', f'{pdk}'])

def lvs(console, design_dir, output_path, design_name, config_file, pdk_root, pdk, tag):
    design_dir = os.path.abspath(design_dir)
    output_path = os.path.abspath(output_path)
    config_file = os.path.abspath(config_file)
    precheck_root = os.path.join(os.path.expanduser("~"), "mpw_precheck")
    os.environ['PYTHONPATH'] = f'{precheck_root}'
    if not os.path.exists(precheck_root):
        subprocess.run(['git', 'clone', 'https://github.com/efabless/mpw_precheck.git', precheck_root])
    if not os.path.exists(f'{output_path}/{design_name}'):
        os.mkdir(f'{output_path}/{design_name}')
    if tag:
        subprocess.run(['python3', f'{precheck_root}/checks/lvs_check/lvs.py', '-g', f'{design_dir}', '-o', f'{output_path}', '-d', f'{design_name}', '-c', f'{config_file}', '-p', f'{pdk_root}/{pdk}', '-t', f'{tag}'], cwd=precheck_root)
    else:
        subprocess.run(['python3', f'{precheck_root}/checks/lvs_check/lvs.py', '-g', f'{design_dir}', '-o', f'{output_path}', '-d', f'{design_name}', '-c', f'{config_file}', '-p', f'{pdk_root}/{pdk}'], cwd=precheck_root)

def xor(console, design_name, design1, design2):
    design1 = os.path.abspath(design1)
    design2 = os.path.abspath(design2)
    precheck_root = os.path.join(os.path.expanduser("~"), "mpw_precheck")
    if not os.path.exists(precheck_root):
        subprocess.run(['git', 'clone', 'https://github.com/efabless/mpw_precheck.git', precheck_root])
    subprocess.run(['klayout', '-r', 'xor.rb.drc', '-rd', f'thr={os.cpu_count}', '-rd', f'top_cell={design_name}', '-rd', f'a={design1}', '-rd', f'b={design2}', '-rd', f'ol={os.path.dirname(design1)}/{design_name}-xor.gds', '-rd', 'ext=gds', '-rd', f'xor_total_file_path={os.path.dirname(design1)}/xor_output.txt', '-zz'], cwd=f'{precheck_root}/checks/xor_check')

def def_to_gds(console, def_file, pdk, pdk_root, output, extra_gds=None, extra_lef=None):
    magic_env = dict()
    magic_env['DEF_TO_GDS'] = "1"
    magic_env['DEF_TO_MAG'] = "0"
    magic_env['MAGIC_GDS_ALLOW_ABSTRACT'] = "0"
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    if not os.path.exists(def_file):
        console.print(f"[red]ERROR : {def_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = def_file
    if extra_lef:
        magic_env['MAGIC_GDS_ALLOW_ABSTRACT'] = "1"
        lef_export = ""
        for lef in extra_lef:
            if not os.path.exists(lef):
                console.print(f"[red]ERROR : {lef} path doesn't exist")
                exit(1)
            else:
                lef_export = lef_export + lef + " "
        magic_env['EXTRA_LEFS'] = f'"{lef_export.strip()}"'
    if extra_gds:
        gds_export = ""
        for gds in extra_gds:
            if not os.path.exists(gds):
                console.print(f"[red]ERROR : {gds} path doesn't exist")
                exit(1)
            else:
                gds_export = gds_export + gds + " "
        magic_env['EXTRA_GDS_FILES'] = f'"{gds_export.strip()}"'
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/def_to_all.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)


def def_to_mag(console, def_file, pdk, pdk_root, output):
    magic_env = dict()
    magic_env['DEF_TO_MAG'] = "1"
    magic_env['DEF_TO_GDS'] = "0"
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    if not os.path.exists(def_file):
        console.print(f"[red]ERROR : {def_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = def_file
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/def_to_all.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def mag_to_lef(console, mag_file, pdk, pdk_root, output):
    magic_env = dict()
    magic_env['MAG_TO_LEF'] = "1"
    magic_env['GDS_TO_LEF'] = "0"
    magic_env['DEF_TO_LEF'] = "0"
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    if not os.path.exists(mag_file):
        console.print(f"[red]ERROR : {mag_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = mag_file
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/all_to_lef.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def gds_to_lef(console, gds_file, pdk, pdk_root, output):
    magic_env = dict()
    magic_env['MAG_TO_LEF'] = "0"
    magic_env['GDS_TO_LEF'] = "1"
    magic_env['DEF_TO_LEF'] = "0"
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    if not os.path.exists(gds_file):
        console.print(f"[red]ERROR : {gds_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = gds_file
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/all_to_lef.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def def_to_lef(console, def_file, pdk, pdk_root, output):
    magic_env = dict()
    magic_env['MAG_TO_LEF'] = "0"
    magic_env['GDS_TO_LEF'] = "0"
    magic_env['DEF_TO_LEF'] = "1"
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
        exit(1)
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
        exit(1)
    else:
        magic_env['PDK'] = pdk
    if not os.path.exists(def_file):
        console.print(f"[red]ERROR : {def_file} path doesn't exist")
        exit(1)
    else:
        magic_env['MACRO'] = def_file
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/all_to_lef.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)
