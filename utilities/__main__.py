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
import click
from click_default_group import DefaultGroup

from . import __version__
from .manage import (
    mag_to_gds_cmd,
    gds_to_mag_cmd,
    gds_to_def_cmd,
    mag_to_def_cmd,
    drc_cmd,
    lvs_cmd,
    xor_cmd,
)


@click.group(
    cls=DefaultGroup,
    default="output",
    default_if_no_args=True,
)
@click.version_option(__version__)
def cli():
    pass


cli.add_command(mag_to_gds_cmd)
cli.add_command(gds_to_mag_cmd)
cli.add_command(gds_to_def_cmd)
cli.add_command(mag_to_def_cmd)
cli.add_command(drc_cmd)
cli.add_command(lvs_cmd)
cli.add_command(xor_cmd)

if __name__ == "__main__":
    cli()
