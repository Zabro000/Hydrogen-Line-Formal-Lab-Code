import virgo
def update_ra_dec(user_input):
    error_list = [0,0]

    user_input = user_input.replace(" ", "")
    user_input = user_input.split(",")

    try:
        user_float_list = list(map(float, user_input))

    except TypeError: 
        return error_list
    

    if (not (0 <= user_float_list[0] <= 24)) or (not (0 <= user_float_list[1] <= 90)) or (not (len(user_float_list) == 2)):
        return error_list
    
    return user_float_list 


def from_az_alt_update_ra_dec(user_input, lat, lon, height) -> list:
    """Arguments:
            list of az and altitude in degrees"""
    error_list = [0,0]

    user_input = user_input.replace(" ", "")
    user_input = user_input.split(",")

    try:
        user_float_list = list(map(float, user_input))
    except TypeError: 
        return error_list
    
    if (not (0 <= user_float_list[0] <= 360)) or (not (0 <= user_float_list[1] <= 90)) or (not (len(user_float_list) == 2)):
        return error_list
    
    try:
        ra_dec_values = list(virgo.equatorial(user_float_list[1], user_float_list[0], lat, lon, height))
    except ValueError:
        return error_list
    
    return ra_dec_values



def error_value_assign(input_dict, error_value = None):

    if error_value is None:
        error_value = 0 
    
    for i in input_dict:
        input_dict[i] = error_value 

    return input_dict

def equatorial_to_galactic(ra_dec):
    error_list = [0,0]

    try:
        gal_lat_lon = list(virgo.galactic(ra=ra_dec[0], dec=ra_dec[1]))

    except ValueError as error:
        print("Conversion to galactic coordinates failed. ", error)
        return error_list
    
    return gal_lat_lon




if __name__ == "__main__":
    print(update_ra_dec("24,90"))
    print(from_az_alt_update_ra_dec("270, 80", 79,170, 1))
    print(error_value_assign({"asasd": 90, "jjj": 99999}))
    print(help(from_az_alt_update_ra_dec))
    print(equatorial_to_galactic([23,45]))