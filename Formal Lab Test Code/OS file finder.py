import os


""" def file_finder(name):
    ...


for root, folders, files in os.walk("./Observation Data"):
    print("\n")
    print(f"{root = }")
    print(f"{folders = }")
    print(f"{files = }")
    print("\n")
 """
    


def find_file(name, dir):

    for root, folders, files in os.walk(dir):
        print("\n")
        print(f"{root = }")
        print(f"{folders = }")
        print(f"{files = }")
        print("\n")
        
        if name in files:
            print("Found the file")



find_file("HI Map; 2024 day 207 or 2024-7-25 14;24, duration; 10(s), Gain; 20(dB), ra and dec; 6.93(hr), 2.94(deg).png", "./Observation Data" )
#### upon closing sort the cal files or something? 
