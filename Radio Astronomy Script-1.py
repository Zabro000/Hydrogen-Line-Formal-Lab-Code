
import virgo
import time
import pygame
import astropy
import operator


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
green = (23,255,69)
light_green = (135,225,143)

main_screen_color = white
normal_button_colors = {'off': black, 'on': green, 'hover': light_green}
night_mode_button_colors = {'off': black, 'on': red, 'hover': other_red}

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

observation_ra = None 
observation_dec = None 
observation_alt = None 
observation_az = None

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

#starting pygame
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


        #Updates the button states so if I change the state of the button manually its color wont be weird 
        if self.state == True:
            self.current_color = self.colors['on']
            self.image.fill(self.current_color)
            self.text_state = "selected"
        else:
            self.current_color = self.colors['off']
            self.image.fill(self.current_color)
            self.text_state = "off"
        
   

    
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
             

    
    def cursor_hover(self, mouse_position):
        if self.rect.left <= mouse_position[0] <= self.rect.left + self.button_width and self.rect.top <= mouse_position[1] <= self.rect.bottom:
            self.image.fill(self.colors['hover'])
        else:
            self.image.fill(self.current_color)

    def draw_basic_button_text(self):
        draw_txt(screen, self.button_text, 19, white, self.rect.centerx, self.rect.centery)
        draw_txt(screen, self.text_state, 19, white, self.rect.centerx, self.rect.centery - 20)



def parse_time() -> str:
    time_tuple = time.localtime()
    
    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday

    virgo_time_string = f"{year}-{month}-{day}"

    return virgo_time_string


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
            Button.on_or_off_button_click(location_settings_button, pygame.mouse.get_pos())

            if continue_button.state == True :
                running = False

            if color_button.state == True:
                color_button.colors = normal_button_colors
            else:
                color_button.colors = night_mode_button_colors

    end_of_game_loop_button_render(screen, screen_1_buttons)
    
    pygame.display.flip()





### Second loop for getting the observation ready

running = True 

manual_alt_az_button = Button("Manual Alt Az", screen_width/2 - 300, screen_height/2 - 300)
auto_alt_az_button = Button("Auto Alt Az", screen_width/2 - 300, screen_height/2 - 100)
hi_display_button = Button("Show Hydrogen", screen_width/2 - 200, screen_height/2)


screen_2_buttons = pygame.sprite.Group()

screen_2_buttons.add(manual_alt_az_button)
screen_2_buttons.add(auto_alt_az_button)
screen_2_buttons.add(hi_display_button)

screen.fill(white)
pygame.display.flip()

while running: 

    clock.tick(fps)
    inital_button_state = hi_display_button.state

    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            Button.on_or_off_button_click(manual_alt_az_button, pygame.mouse.get_pos())
            Button.on_or_off_button_click(auto_alt_az_button, pygame.mouse.get_pos())
            temp_state = Button.doer_button_click(hi_display_button, pygame.mouse.get_pos())


            #Updating the button's state mid loop required that stuff in the update method
            if hi_display_button.state == True: 

                equatorial_coordinates = virgo.equatorial(30, 210, location_lat, location_lon, location_elevation)

                virgo.map_hi(equatorial_coordinates[0], equatorial_coordinates[1])

                hi_display_button.state = False 
                hi_display_button.on_or_off_button_click(pygame.mouse.get_pos())

        

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
