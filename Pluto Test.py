# Test for the 

import adi 
import time
import matplotlib as plt 
import numpy as np 



sdr = adi.Pluto()

sdr.rx_rf_bandwidth = 2 * 10**6

sdr.sample_rate = 6 * 10**6

sdr.rx_lo = 890 * 10**6 #(890Mhz)

sdr.tx_lo = 895 * 10**6

sdr.gain_control_mode_chan0 = "slow_attack"

sdr.tx_cyclic_buffer = True

sdr.tx_hardwaregain_chan0 = - 50

sdr.rx_enabled_channels = [0]
sdr.tx_enabled_channels = [0]

fs = int(sdr.sample_rate)
N = 1024*2

fc = int(1000000 / (fs / N)) * (fs / N)

ts = 1 / float(fs)

t = np.arange(0, N * ts, ts)

i = np.cos(2 * np.pi * t * fc) * 2 **14
q = np.sin(2 * np.pi * t * fc) * 2 **14
iq = i + 1j * q

sdr.tx(iq)





data = sdr.rx()
print(data)
