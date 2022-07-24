import argparse
 
from attr import has

parser = argparse.ArgumentParser(
    description="extracts the list of modules for sdf annotation"
)

parser.add_argument("--input", "-i", required=True, help="rtl verilog file")
parser.add_argument("--output", "-o", required=True, help="includes file")

args = parser.parse_args()
input = args.input
output = args.output

pattern = " ("
sdf_path = "../../../sdf/"

with open(input, "r") as f:
    for line in f:
        if pattern in line: 
            if "module" not in line:
                module = line.split()
                print("$sdf_annotate(\"" + sdf_path + module[0] + ".sdf\", uut.mprj.fpga_core_uut." + module[1] + ") ;")
