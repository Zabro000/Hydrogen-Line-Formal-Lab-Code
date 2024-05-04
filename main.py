import time
import virgo

# How to install and activate a venv
# https://python.land/virtual-environments/virtualenv
# https://virgo.readthedocs.io/en/latest/
# venv\Scripts\Activate.ps1
# https://virgo.readthedocs.io/en/latest/reference.html
# https://docs.python.org/3/library/time.html


def parse_time() -> str:
    time_tuple = time.localtime()
    
    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday

    virgo_time_string = f"{year}-{month}-{day}"

    return virgo_time_string





parse_time()

# '2024-4-20'

print(time.asctime(time.localtime()))

#virgo.map_hi(16, -26)




