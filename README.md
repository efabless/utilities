# utilities

While in development, engineers usually debug layout issues by writing scripts on the fly, or writing commands manually, which is error prone and not consistent between engineers. Utilities is a python package that collects all the needed layout scripts in one place and provides a python wrapper to interface with these scripts.

- **def-to-gds:**  creates a gds from def
- **def-to-lef:**  creates a lef from def
- **def-to-mag:**  creates a mag from def
- **drc:**         runs klayout DRC
- **gds-to-def:**  creates a def from gds
- **gds-to-lef:**  creates a lef from gds
- **gds-to-mag:**  creates a mag from gds
- **lvs:**         runs Layout Vs Schematic (only accepts gds vs gl netlist)
- **mag-to-def:**  creates a def from mag
- **mag-to-gds:**  creates a gds from mag
- **mag-to-lef:**  creates a lef from mag
- **xor:**         runs xor on 2 layouts

## Installation

```
git clone git@github.com:efabless/utilities.git
cd utilities
pip install .
```
