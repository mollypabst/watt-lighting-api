from sys import argv
from warnings import filterwarnings

from pandas import set_option

from envision import update, lighting, occupancy

filterwarnings("ignore")
set_option("display.max_rows", None)
set_option("display.width", 0)

output = {
    "lighting": lighting,
    "update": update,
    "occupancy": occupancy,
}[argv[1]]()

if hasattr(output, "fillna"):
    output.fillna("", inplace=True)

print(output)
