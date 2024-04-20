
import virgo
import time
import pygame
import astropy


### pygame varibles
screen_width = 1600
screen_height = 900
fps = 30 

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
off_red = (240,11,0)
mid_red = (163,8,0)
other_red = (231,12,30)
dark_red = (65,3,0)

### Virgo and radio astronomy varibles
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
default_observing_values = {
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

#Virgo and radio astronomy 
# location varibles
location_lat = 51.9
location_lon = -114
location_elevation = 1420 #m
date = None

default_location_parameters = {
    'lat': location_lat,
    'lon': location_lon,
    'height': location_elevation
}



#starting virgo observation class
""" class Observation():


    def __init__(self, name, observation_parameters, location_parameters, output_name = None, start_time = None, date = None) -> None:
        self.name = name
        self.obs_parameters = observation_parameters
        self.location_parameters = location_parameters

        if date is None:
            self.date = time.asctime(time.localtime())
        else:
            self.date = date

        if output_name is None:
            self.data_name = f"observation data using {self.name} from {time.asctime(time.localtime())}.dat"
        else:
            self.data_name = f"{output_name}.dat"

        if start_time is None:
            self.start_time = 20
        else:
            self.start_time = start_time


    def run_observation(self):
        virgo.observe()

    @classmethod
    def create_observation(cls):
        ...
 """
#starting pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Penny Lab Simulation")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('calibri')


class Button(pygame.sprite.Sprite):
    

    def __init__(self, button_text, position_x, position_y, color = None, state = None) -> None:
        self.button_width = 200
        self.button_height = 100
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.button_width, self.button_height))
        self.rect = self.image.get_rect()
        self.rect.center = [position_x, position_y]
        self.x_position = position_x
        self.y_position = position_y 
        self.button_text = button_text

        if color is None:
            self.color = red
        else:
            self.color = color 
        self.image.fill(self.color)

        if state is None:
            self.state = False
        else:
            self.state = bool(state)
        

    def update(self):
        ... 


        

test = Observation("testinggg", default_observing_values, default_location_parameters)

print(test.date)

virgo.predict(default_location_parameters['lat'], default_location_parameters['lon'], default_location_parameters['height'], source= 'Cas A', date= '2024-4-20')
virgo.map_hi(6,45)
