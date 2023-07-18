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
    gds_to_def,
    gds_to_mag,
    mag_to_def,
    mag_to_gds,
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

@click.command("gds-to-mag", help="creates a gds from mag")
@click.argument("gds_file")
@click.option("--pdk_root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of mag")
def gds_to_mag_cmd(gds_file, output, pdk_root, pdk):
    console = Console()
    gds_to_mag(
        console, gds_file, output, pdk_root, pdk
    )

@click.command("mag-to-def", help="creates a gds from mag")
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

@click.command("gds-to-def", help="creates a gds from mag")
@click.argument("gds_file")
@click.option("--pdk_root", required=True, help="path to pdk")
@click.option("--pdk", required=True, help="pdk family")
@click.option("--output", required=True, help="path to destination of mag")
def gds_to_def_cmd(gds_file, output, pdk_root, pdk):
    console = Console()
    gds_to_def(
        console, gds_file, output, pdk_root, pdk
    )
