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


def test_parse_time():
    time_tuple = time.localtime() 
    year = time_tuple.tm_year
    year_day = time_tuple.tm_yday
    month = time_tuple.tm_mon
    normal_day = time_tuple.tm_mday
    hour = time_tuple.tm_hour
    minute = time_tuple.tm_min

    stringg = f"Hydrogen Line Data taken in {year} day {year_day} or {year}-{month}-{normal_day} {hour};{minute}"

    print(stringg)

print(time.asctime(time.localtime()))
parse_time()
test_parse_time()

# '2024-4-20'

print(time.asctime(time.localtime()))

#virgo.map_hi(16, -26)


sillyyy = "asdasd"
fluffy = 90
ra = 36
dec = 74


loc = [ra, dec]

print(loc)

ra = 1 

loc[ra] = ra

print(loc)

cloud = {
    'silly': sillyyy,
    'fluffy': fluffy
}

fluffy = 0.0090

cloud['fluffy'] = fluffy
cloud[0]
print(cloud[0])

