
import virgo

# Define observation parameters
obs = {
    'dev_args': '',
    'rf_gain': 30,
    'if_gain': 25,
    'bb_gain': 18,
    'frequency': 1420e6,
    'bandwidth': 2.4e6,
    'channels': 2048,
    't_sample': 1,
    'duration': 10,
    'loc': '',
    'ra_dec': '',
    'az_alt': ''
}

# Check source position
#virgo.predict(lat=39.8, lon=-74.9, source='Cas A', date='2020-12-26')
# Begin data acquisition
virgo.observe(obs_parameters=obs, obs_file='observation.dat')

# Analyze data, mitigate RFI and export the data as a CSV file
virgo.plot(obs_parameters=obs, n=20, m=35, f_rest=1420.4057517667e6,
           vlsr=False, meta=False, avg_ylim=(-5,15), cal_ylim=(-20,260),
           obs_file='observation.dat', rfi=[(1419.2e6, 1419.3e6), (1420.8e6, 1420.9e6)],
           dB=True, spectra_csv='spectrum.csv', plot_file='plot.png')

