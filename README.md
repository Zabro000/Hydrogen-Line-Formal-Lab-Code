# Hydrogen Line Radio Astronomy Program and Example Data
This is a python program which controls a software defined radio (SDR) to take observations of the hydrogen line. It is built around the Virgo library. To take observations with an SDR, the program must be ran on a Linux operating system (OS) – with all the dependencies the Virgo library needs installed. Other functionality does not need a Linux OS. Generating maps of the sky in the hydrogen line, and converting between astronomical coordinate systems can be done on any OS, so long as the Virgo library is installed. 

The python file, “Radio Astronomy Script-1”, is the aforementioned python program. The example plots, images, and data are found in the folder titled, “Example Observation Data”. 

### Example Plot 1: 
The large spike is the hydrogen line. The antenna took a reading from an area in the sky with the coordinates of 22.32hr of right ascension, and -6.69deg of declination. This area of the sky is near the center of the galaxy.
![HI Plot; 2024 day 214 or 2024-8-1 0;17, duration; 300 0(s), Gain; 20(dB), ra and dec; 22 32(hr), -6 69(deg)](https://github.com/user-attachments/assets/fd30cf74-d442-4163-ad42-4b693dce955e)


### Example Plot 2: 
The red dot shows where the antenna was pointing when it collected data plotted in the previous image. Moreover, this figure shows the strength of the hydrogen line across the sky; the brighter the color, the stronger the hydrogen line signal is at that location. 
![HI Map; 2024 day 214 or 2024-8-1 13;26, duration; 10(s), Gain; 20(dB), ra and dec; 22 32(hr), -6 69(deg)-2](https://github.com/user-attachments/assets/905ba680-8ef4-4202-b4b5-23c49a4d2626)

