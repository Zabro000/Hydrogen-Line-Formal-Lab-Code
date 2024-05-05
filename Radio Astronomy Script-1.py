import virgo
import time
import pygame
import astropy
import operator
from Phidget22.Phidget import *
from Phidget22.Devices.Spatial import *


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

final_observing_values = {
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

### Varibles for the Coordinates
observation_ra = None 
observation_dec = None 
observation_ra_dec = [observation_ra, observation_dec]
observation_alt = None 
observation_az = None
observation_az_alt = [observation_az, observation_alt]

default_observation_coordinates = {
    'azimuth': observation_az,
    'altitude': observation_alt,
    'azimuth and altitude list': observation_az_alt,
    'right ascension': observation_ra,
    'declination': observation_dec,
    'right ascension and declination list': observation_ra_dec
}


### location varibles
location_lat = 51
location_lon = -114
location_elevation = 1420 #m
date = None

default_location_parameters = {
    'lat': location_lat,
    'lon': location_lon,
    'height': location_elevation
}



### Phidget spatial sensor code
attachment_time = 5 * 1000



### Pygame varibles
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
green = (23,255,69)
light_green = (135,225,143)

main_screen_color = white
normal_button_colors = {'off': black, 'on': green, 'hover': light_green}
night_mode_button_colors = {'off': black, 'on': red, 'hover': other_red}

### Starting pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hydrogen Line")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('calibri')


class Button(pygame.sprite.Sprite):
    

    def __init__(self, button_text, position_x, position_y, colors = None, state = None) -> None:
        self.button_width = 200
        self.button_height = 100
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.button_width, self.button_height))
        self.rect = self.image.get_rect()
        self.rect.center = [position_x, position_y]
        self.x_position = position_x
        self.y_position = position_y 
        self.button_text = button_text


        if colors is None:
            self.colors = normal_button_colors
        #Checks that the color inputted is only a dict
        elif isinstance(colors, dict):
            self.colors = colors
        else:
            raise TypeError

        if state is None:
            self.state = False
        else:
            self.state = bool(state)
        

        if self.state == False:
            self.text_state = "off"
            self.current_color = self.colors['off']
        else:
            self.text_state = "selected"
            self.current_color = self.colors['on']

        self.image.fill(self.current_color)


    def update(self):
        ...


    def on_or_off_button_click(self, mouse_position):
         if self.rect.left <= mouse_position[0] <= self.rect.left + self.button_width and self.rect.top <= mouse_position[1] <= self.rect.bottom:
                
                # flips the button state to the opposite bool
                self.state = operator.not_(self.state)


                #changes color and text depeding on if the button is on or off 
                if self.state == True:
                    self.current_color = self.colors['on']
                    self.image.fill(self.current_color)
                    self.text_state = "selected"
                else:
                    self.current_color = self.colors['off']
                    self.image.fill(self.current_color)
                    self.text_state = "off"

                # Return true so the button if statements in the while loop can run 
                return True
         
         return False


    def doer_button_click(self, mouse_position):
         if self.rect.left <= mouse_position[0] <= self.rect.left + self.button_width and self.rect.top <= mouse_position[1] <= self.rect.bottom:
             
             self.state = operator.not_(self.state)

             return True 
         
         return False
             
    
    def cursor_hover(self, mouse_position):
        if self.rect.left <= mouse_position[0] <= self.rect.left + self.button_width and self.rect.top <= mouse_position[1] <= self.rect.bottom:
            self.image.fill(self.colors['hover'])
        else:
            self.image.fill(self.current_color)

    def draw_basic_button_text(self):
        draw_txt(screen, self.button_text, 19, white, self.rect.centerx, self.rect.centery -20)
        draw_txt(screen, self.text_state, 19, white, self.rect.centerx, self.rect.centery)

def output_data_file_name(sdr_gain = None, coordinates_dict = None, observation_time = None) -> str:

    if sdr_gain == None: 
        #Refers to thr rf gain for the sdr outside of this function 
        global sdr_rf_gain
        sdr_gain = sdr_rf_gain

    if coordinates_dict == None:
        global default_observation_coordinates
        coordinates_dict = default_observation_coordinates

    if observation_time == None:
        global observing_time
        observation_time = observing_time

    time_tuple = time.localtime() 

    year = time_tuple.tm_year
    year_day = time_tuple.tm_yday
    month = time_tuple.tm_mon
    normal_day = time_tuple.tm_mday
    hour = time_tuple.tm_hour
    minute = time_tuple.tm_min

    ra = coordinates_dict['right ascension']
    dec = coordinates_dict['declination']

    file_name = f"Hydrogen Line Observation Data taken in {year} day {year_day} or {year}-{month}-{normal_day} {hour};{minute}, SDR gain is {sdr_gain}, ra and dec coordinates are {ra}, {dec}.dat"

    return file_name




def parse_time() -> str:
    time_tuple = time.localtime()
    
    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday

    virgo_time_string = f"{year}-{month}-{day}"

    return virgo_time_string

### handels the end of the game loop and drawing all th buttons
def end_of_game_loop_button_render(general_screen, button_group) -> None:
    button_group.update()

    for button in button_group:
        Button.cursor_hover(button, pygame.mouse.get_pos())

    general_screen.fill(white)
    button_group.draw(screen)

    for button in button_group: 
        Button.draw_basic_button_text(button)


def draw_txt(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

color_button = Button("Night Mode", screen_width/2, screen_height/2,  )
skip_button = Button("Skip Settings", screen_width/2 - 300, screen_height/2)
continue_button = Button("Continue", screen_width/2, screen_height/2 + 200)
location_settings_button = Button("Set Location", screen_width/2 -300, screen_height/2 + 200)


screen_1_buttons = pygame.sprite.Group()
screen_1_buttons.add(color_button)
screen_1_buttons.add(skip_button)
screen_1_buttons.add(continue_button)
screen_1_buttons.add(location_settings_button)
 


running = True 
screen.fill(white)
pygame.display.flip()
while running:
    clock.tick(fps)


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            print("Program will hult now!")
            #raises basic error so the program will stop 
            raise WindowsError
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            Button.on_or_off_button_click(color_button, pygame.mouse.get_pos())
            Button.on_or_off_button_click(skip_button, pygame.mouse.get_pos())
            Button.on_or_off_button_click(continue_button, pygame.mouse.get_pos())
            check_state_1 = Button.on_or_off_button_click(location_settings_button, pygame.mouse.get_pos())

            if continue_button.state == True :
                running = False

            if color_button.state == True:
                color_button.colors = normal_button_colors
            else:
                color_button.colors = night_mode_button_colors

            # These two if statements will make sure that this only runs if the button was turned on because the button needs to be pressed and the state of the button needs to be on
            if location_settings_button.state == True and check_state_1 == True:
                print("click")

    end_of_game_loop_button_render(screen, screen_1_buttons)
    
    pygame.display.flip()





### Second loop for getting the observation ready

running = True 

manual_alt_az_button = Button("Manual Alt Az", screen_width/2 - 600, screen_height/2 - 300)
auto_alt_az_button = Button("Auto Alt Az", screen_width/2 - 600, screen_height/2 + 100)
hi_display_button = Button("Show Hydrogen Map", screen_width/2 - 300, screen_height/2 - 100)
test_spatial_phidget_button = Button("Test Phidget", screen_width/2 - 600, screen_height/2 - 100)
run_observation_button = Button("Begin Observation", screen_width/2 + 600, screen_height/2 -100)



screen_2_buttons = pygame.sprite.Group()

screen_2_buttons.add(manual_alt_az_button)
screen_2_buttons.add(auto_alt_az_button)
screen_2_buttons.add(hi_display_button)
screen_2_buttons.add(test_spatial_phidget_button)
screen_2_buttons.add(run_observation_button)


screen.fill(white)
pygame.display.flip()

while running: 

    clock.tick(fps)

    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            Button.on_or_off_button_click(manual_alt_az_button, pygame.mouse.get_pos())
            check_state_2 =Button.on_or_off_button_click(auto_alt_az_button, pygame.mouse.get_pos())
            temp_state = Button.doer_button_click(hi_display_button, pygame.mouse.get_pos())
            temp_state_2 = Button.doer_button_click(test_spatial_phidget_button, pygame.mouse.get_pos())
            temp_state_3 = Button.doer_button_click(run_observation_button, pygame.mouse.get_pos())


            #Updating the button's state mid loop required that stuff in the update method
            if temp_state == True: 

                equatorial_coordinates = virgo.equatorial(30, 210, location_lat, location_lon, location_elevation)

                virgo.map_hi(equatorial_coordinates[0], equatorial_coordinates[1])

            if temp_state_2 == True: 
                angle_sensor = Spatial()
                try:
                    angle_sensor.openWaitForAttachment(attachment_time)
                except PhidgetException as error:
                    print("The phidget is probably not attached, ", error)
                else:
                    print("The angle sensor is connected!")

            if manual_alt_az_button.state == True and check_state_2 == True:
                ...


            if temp_state_3 == True:
                final_observing_values['loc']
                final_observing_values['duration'] = observing_time
                final_observing_values['rf_gain'] = sdr_rf_gain
                final_observing_values['ra_dec'] = observation_ra_dec
                final_observing_values['az_alt'] = observation_az_alt
                output_name = output_data_file_name()

                try: 
                    virgo.observe(final_observing_values, 'wola', output_name)
                except:
                    print("Check if the SDR is connected")
                








        

        if event.type == pygame.QUIT:
            running = False
            print("Program will hult now!")
            #raises basic error so the program will stop 
            raise WindowsError


    end_of_game_loop_button_render(screen, screen_2_buttons)


    pygame.display.flip()


    """     screen_2_buttons.update()
    Button.cursor_hover(manual_alt_az_button, pygame.mouse.get_pos())
    Button.cursor_hover(auto_alt_az_button, pygame.mouse.get_pos())
    Button.cursor_hover(hi_display_button, pygame.mouse.get_pos())
   
    screen.fill(white)
    screen_2_buttons.draw(screen)
   

    Button.draw_basic_button_text(manual_alt_az_button)
    Button.draw_basic_button_text(auto_alt_az_button)
    Button.draw_basic_button_text(hi_display_button) """



""" 
    Button.cursor_hover(color_button, pygame.mouse.get_pos())
    Button.cursor_hover(skip_button, pygame.mouse.get_pos())
    Button.cursor_hover(continue_button, pygame.mouse.get_pos())
    Button.cursor_hover(location_settings_button, pygame.mouse.get_pos())

    screen.fill(white)
    screen_1_buttons.update()
    screen_1_buttons.draw(screen)

    Button.draw_basic_button_text(color_button)
    Button.draw_basic_button_text(continue_button)
    Button.draw_basic_button_text(skip_button)
    Button.draw_basic_button_text(location_settings_button)

 """

    

        

        

test = Observation("testinggg", default_observing_values, default_location_parameters)

print(test.date)

virgo.predict(default_location_parameters['lat'], default_location_parameters['lon'], default_location_parameters['height'], source= 'Cas A', date= '2024-4-20')
virgo.map_hi(6,45)
