print("hi")
import virgo
import time
import virgo.run_ftf 



# Defining all the observing varibles
observing_time = 60 # in seconds
sdr_rf_gain = 20
if_gain = 25
bb_gain = 18
hydrogen_line_freq = 1.420405751768 * 10**9
observing_bandwidth = 2.4 * 10**6
channels = 2048
t_sample = 1
location = None
ra_dec = None
az_alt = None
data_file_name = "Test data.dat"
spectrometer_type = "FTF"
observing_start_time = 30



#location vars
location_lat = 51.9
location_lon = -114
location_elevation = 1420 #m
date = None


observing_values = {
    'dev_args': '',
    'rf_gain': sdr_rf_gain,
    'if_gain': if_gain,
    'bb_gain': bb_gain,
    'frequency': hydrogen_line_freq,
    'bandwidth': observing_bandwidth,
    'channels': channels,
    't_sample': t_sample,
    'duration': observing_time,
    'loc': '',
    'ra_dec': '',
    'az_alt': ''
}


observing_values['ra_dec'] = 10

print(observing_values['ra_dec'])

def Get_Time():

    pass


timeee = time.localtime()
print(time.asctime(timeee))
print(time.localtime())


print(virgo.wavelength(hydrogen_line_freq))

print(virgo.galactic(12, 12))

try:
    virgo.observe(obs_parameters= observing_values, obs_file= data_file_name)


    print(virgo.predict(location_lat, location_lon, location_elevation, plot_file= True))
except ModuleNotFoundError as error:
    print("try on the other computer")
    print(error)

finally:
    print("done")


