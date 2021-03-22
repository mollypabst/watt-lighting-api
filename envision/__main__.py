from sys import argv
from warnings import filterwarnings
from pandas import set_option
from datetime import datetime
from envision import update, lighting, occupancy

filterwarnings("ignore")
set_option("display.max_rows", None)
set_option("display.width", 0)

output = {
    "lighting": lighting,
    "update": update,
    "occupancy": occupancy(datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(hours = 1)),
}[argv[1]]()

if hasattr(output, "fillna"):
    output.fillna("", inplace=True)

print(output)
