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
# import os
# import ipm
import click
from rich.console import Console

from .common import (
    def_to_gds,
    def_to_lef,
    def_to_mag,
    drc,
    gds_to_def,
    gds_to_lef,
    gds_to_mag,
    lvs,
    mag_to_def,
    mag_to_gds,
    mag_to_lef,
    xor,
)

@click.command("mag-to-gds", help="creates a gds from mag")
@click.argument("mag_file")
@click.option("--pdk_root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option(
    "--maglef_macro", required=False, help="path to maglef to get loaded", multiple=True
)
@click.option("--mag_dir", required=False, help="path to mag directory", multiple=True)
@click.option(
    "--gds_macro", required=False, help="path to gds to get loaded", multiple=True
)
@click.option("--output", required=True, help="path to destination of gds")
def mag_to_gds_cmd(mag_file, maglef_macro, mag_dir, gds_macro, output, pdk_root, pdk):
    console = Console()
    mag_to_gds(
        console, mag_file, maglef_macro, mag_dir, gds_macro, output, pdk_root, pdk
    )

@click.command("gds-to-mag", help="creates a mag from gds")
@click.argument("gds_file")
@click.option("--pdk_root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of mag")
def gds_to_mag_cmd(gds_file, output, pdk_root, pdk):
    console = Console()
    gds_to_mag(
        console, gds_file, output, pdk_root, pdk
    )

@click.command("mag-to-def", help="creates a def from mag")
@click.argument("mag_file")
@click.option("--pdk_root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option(
    "--maglef_macro", required=False, help="path to maglef to get loaded", multiple=True
)
@click.option("--mag_dir", required=False, help="path to mag directory", multiple=True)
@click.option(
    "--gds_macro", required=False, help="path to gds to get loaded", multiple=True
)
@click.option("--output", required=True, help="path to destination of gds")
def mag_to_def_cmd(mag_file, maglef_macro, mag_dir, gds_macro, output, pdk_root, pdk):
    console = Console()
    mag_to_def(
        console, mag_file, maglef_macro, mag_dir, gds_macro, output, pdk_root, pdk
    )

@click.command("gds-to-def", help="creates a def from gds")
@click.argument("gds_file")
@click.option("--pdk_root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of mag")
def gds_to_def_cmd(gds_file, output, pdk_root, pdk):
    console = Console()
    gds_to_def(
        console, gds_file, output, pdk_root, pdk
    )

@click.command("drc", help="runs klayout DRC")
@click.argument("gds_file")
@click.option("--output", required=True, help="path to destination output reports")
def drc_cmd(gds_file, output):
    console = Console()
    drc(
        console, gds_file, output
    )

@click.command("lvs", help="runs LVS")
@click.argument("design_name")
@click.option("--output", required=True, help="path to destination output reports")
@click.option("--design_dir", required=True, help="path to design directory (should have gds/<design>.gds & verilog/gl/<design>.v)")
@click.option("--config_file", required=True, help="path to LVS config file")
@click.option("--pdk_root", required=True, help="path to PDK")
@click.option("--pdk", required=True, help="PDK family (sky130A, sky130B, etc..)")
def lvs_cmd(design_name, output, design_dir, config_file, pdk_root, pdk):
    console = Console()
    lvs(console, design_dir, output, design_name, config_file, pdk_root, pdk)

@click.command("xor", help="runs xor on 2 layouts")
@click.argument("design_name")
@click.option("--design1", required=True, help="path to gds1")
@click.option("--design2", required=True, help="path to gds2")
def xor_cmd(design_name, design1, design2):
    console = Console()
    xor(console, design_name, design1, design2)

@click.command("def-to-gds", help="creates a gds from def")
@click.argument("def-file")
@click.option("--pdk-root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--extra-lef", required=False, help="path to extra lef", multiple=True)
@click.option(
    "--extra-gds", required=False, help="path of extra gds", multiple=True
)
@click.option("--output", required=True, help="path to destination of gds")
def def_to_gds_cmd(def_file, pdk, pdk_root, output, extra_gds, extra_lef):
    console = Console()
    def_to_gds(console, def_file, pdk, pdk_root, output, extra_gds, extra_lef)

@click.command("def-to-mag", help="creates a mag from def")
@click.argument("def-file")
@click.option("--pdk-root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of gds")
def def_to_mag_cmd(def_file, pdk, pdk_root, output):
    console = Console()
    def_to_mag(console, def_file, pdk, pdk_root, output)

@click.command("mag-to-lef", help="creates a lef from mag")
@click.argument("mag-file")
@click.option("--pdk-root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of gds")
def mag_to_lef_cmd(mag_file, pdk, pdk_root, output):
    console = Console()
    mag_to_lef(console, mag_file, pdk, pdk_root, output)

@click.command("gds-to-lef", help="creates a lef from gds")
@click.argument("gds-file")
@click.option("--pdk-root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of gds")
def gds_to_lef_cmd(gds_file, pdk, pdk_root, output):
    console = Console()
    gds_to_lef(console, gds_file, pdk, pdk_root, output)

@click.command("def-to-lef", help="creates a lef from def")
@click.argument("def-file")
@click.option("--pdk-root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of gds")
def def_to_lef_cmd(def_file, pdk, pdk_root, output):
    console = Console()
    def_to_lef(console, def_file, pdk, pdk_root, output)
