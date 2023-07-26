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
    else:
        magic_env['MACRO'] = gds_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
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
    else:
        magic_env['MACRO'] = mag_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
    else:
        magic_env['PDK'] = pdk
    if maglef_macro:
        mag_export = ""
        for maglefs in maglef_macro:
            if not os.path.exists(maglefs):
                console.print(f"[red]ERROR : {maglefs} path doesn't exist")
            else:
                mag_export = mag_export + maglefs + " "
        magic_env['MAGLEF_MACRO'] = f'"{mag_export.strip()}"'
    if gds_macro:
        gds_export = ""
        for gds in gds_macro:
            if not os.path.exists(gds):
                console.print(f"[red]ERROR : {gds} path doesn't exist")
            else:
                gds_export = gds_export + gds + " "
        magic_env['GDS_MACRO'] = f'"{gds_export.strip()}"'
    if mag_dir:
        mag_export = ""
        for mags in mag_dir:
            if not os.path.exists(mags):
                console.print(f"[red]ERROR : {mags} path doesn't exist")
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
    else:
        magic_env['MACRO'] = gds_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
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
    else:
        magic_env['MACRO'] = mag_file
    if not os.path.exists(output):
        console.print(f"[red]ERROR : {output} path doesn't exist")
    else:
        magic_env['OUTPUT'] = output
    if not os.path.exists(pdk_root):
        console.print(f"[red]ERROR : {pdk_root} path doesn't exist")
    else:
        magic_env['PDK_ROOT'] = pdk_root
    if not os.path.exists(os.path.join(pdk_root, pdk)):
        console.print(f"[red]ERROR : {pdk_root}/{pdk} path doesn't exist")
    else:
        magic_env['PDK'] = pdk
    if maglef_macro:
        mag_export = ""
        for maglefs in maglef_macro:
            if not os.path.exists(maglefs):
                console.print(f"[red]ERROR : {maglefs} path doesn't exist")
            else:
                mag_export = mag_export + maglefs + " "
        magic_env['MAGLEF_MACRO'] = f'"{mag_export.strip()}"'
    if gds_macro:
        gds_export = ""
        for gds in gds_macro:
            if not os.path.exists(gds):
                console.print(f"[red]ERROR : {gds} path doesn't exist")
            else:
                gds_export = gds_export + gds + " "
        magic_env['GDS_MACRO'] = f'"{gds_export.strip()}"'
    if mag_dir:
        mag_export = ""
        for mags in mag_dir:
            if not os.path.exists(mags):
                console.print(f"[red]ERROR : {mags} path doesn't exist")
            else:
                mag_export = mag_export + mags + " "
        magic_env['MAG_DIR'] = f'"{mag_export.strip()}"'
    magic_env.update(os.environ)
    magic_cmd = [
        "magic", "-noconsole", "-dnull", "-rcfile", f"{pdk_root}/{pdk}/libs.tech/magic/{pdk}.magicrc", f"{os.path.dirname(os.path.abspath(__file__))}/helper_lib/mag_to_def.tcl"
    ]
    subprocess.run(magic_cmd, env=magic_env)

def drc(console, gds_file, output_path):
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
    subprocess.run(['python3', f'{precheck_root}/checks/drc_checks/klayout/klayout_gds_drc_check.py', '-g', f'{gds_file}', '-o', f'{output_path}', '-f', '-b', '-og'])
