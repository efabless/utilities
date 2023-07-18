# SPDX-FileCopyrightText: 2020 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License")
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

drc off
crashbackups stop
addpath [file dirname $::env(MACRO)]
if { [info exists ::env(MAG_DIR)] } {
    foreach mag_dir $::env(MAG_DIR) {
        addpath $mag_dir
    }
}

if { [info exists ::env(MAGLEF_MACRO)] } {
    foreach maglef_macro $::env(MAGLEF_MACRO) {
        load $maglef_macro
    }
}

if { [info exists ::env(GDS_MACRO)] } {
    foreach gds_macro $::env(GDS_MACRO) {
        load [file rootname [file rootname [file tail $gds_macro]]]
        property LEFview true
        property GDS_FILE $gds_macro
        property GDS_START 0
    }
}

load [file rootname [file tail $::env(MACRO)]] -dereference
select top cell
expand
cif *hier write disable
cif *array write disable
gds write $::env(OUTPUT)/[file rootname [file tail $::env(MACRO)]].gds
quit -noprompt
