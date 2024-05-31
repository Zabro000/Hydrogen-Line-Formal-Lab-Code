import virgo
import time
import pygame
import astropy
import operator
from Phidget22.Phidget import *
from Phidget22.Devices.Spatial import *
#venv\Scripts\Activate.ps1


### Virgo and radio astronomy varibles#
observation_time_offset = 4
observing_time = 60 # in seconds
observation_start_time = 1 # in seconds
sdr_rf_gain = 20
if_gain = 25
bb_gain = 18
hydrogen_line_freq = 1.420405751768 * 10**9
test_transmit_freq = 845 * 10**6
observing_bandwidth = 2.4 * 10**6
channels = 2048
t_sample = 1
location = None
ra_dec = None
az_alt = None
data_file_name = "Test data.dat"

#initalizing dicts that is required for the obseravtion and ploting data
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

### Varibles and dicts for the astronomical coordinates
observation_ra = 0 
observation_dec = 0 
observation_ra_dec = [observation_ra, observation_dec]
observation_alt = 0 
observation_az = 0
observation_az_alt = [observation_az, observation_alt]

default_observation_coordinates = {
    'azimuth': observation_az,
    'altitude': observation_alt,
    'azimuth and altitude list': observation_az_alt,
    'right ascension': observation_ra,
    'declination': observation_dec,
    'right ascension and declination list': observation_ra_dec
}


### Initalizing location varibles
location_lat = 51
location_lon = -114
location_elevation = 1420 #m
date = None

default_location_parameters = {
    'lat': location_lat,
    'lon': location_lon,
    'height': location_elevation
}



### Phidget spatial sensor attachment time
attachment_time = 5 * 1000


### Pygame varibles
screen_width = 1500
screen_height = 800
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

purple = (187,153,255)

main_screen_color = white
basic_text_color = black

#Using a dict to keep track of the different colors needed for each situation or state
normal_button_colors = {'off': black, 'on': green, 'hover': purple}
night_mode_button_colors = {'off': black, 'on': red, 'hover': other_red}

### Starting pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hydrogen Line")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('calibri')


#Class for the on screen buttons
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

        #Use normal colors if none is inputted
        if colors is None:
            self.colors = normal_button_colors
        #Checks that the color inputted is only a dict
        elif isinstance(colors, dict):
            self.colors = colors
        else:
            raise TypeError
        
        #Set state of the button to off if none is given
        if state is None:
            self.state = False
        else:
            self.state = bool(state)
        
        #Depending on the state, change the text and assign what the color is right now from the dict
        if self.state == False:
            self.text_state = "off"
            self.current_color = self.colors['off']
        else:
            self.text_state = "selected"
            self.current_color = self.colors['on']

        self.image.fill(self.current_color)


    def update(self):
        ...

    #Method to handle the buttons that hold an on or off state
    def on_or_off_button_click(self, mouse_position):
         #This if statement checks to see of the mouse is over the button
         if self.rect.left <= mouse_position[0] <= self.rect.left + self.button_width and self.rect.top <= mouse_position[1] <= self.rect.bottom:
                
                #flips the button state to the opposite bool, if the current state was on, now it should be off
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

                #Return true so the button if statements in the while loop can run 
                return True
         #Return false so the if statments later to exicute the code assosiated with each button depending on its state and if it was pressed will not run
         return False

    #Method to handle buttons that exicute code when pressed regardless of their state
    def doer_button_click(self, mouse_position):
         if self.rect.left <= mouse_position[0] <= self.rect.left + self.button_width and self.rect.top <= mouse_position[1] <= self.rect.bottom:
             
             self.state = operator.not_(self.state)

             return True 
         
         return False
             
    #Method to change the color of the button if the cursor is over the button
    def cursor_hover(self, mouse_position):
        if self.rect.left <= mouse_position[0] <= self.rect.left + self.button_width and self.rect.top <= mouse_position[1] <= self.rect.bottom:
            self.image.fill(self.colors['hover'])
        else:
            self.image.fill(self.current_color)

    #Method that prints the button's text and its state
    def draw_basic_button_text(self):
        draw_txt(screen, self.button_text, 19, white, self.rect.centerx, self.rect.centery -20)
        draw_txt(screen, self.text_state, 19, white, self.rect.centerx, self.rect.centery)


### Normal functions:

def screen_color_change(object) -> None:
    ...

#Function that creates the name of the data, png and csv spectra output files 
def output_file_name_assigner_function(sdr_gain = None, coordinates_dict = None, observation_time = None) -> str:

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

    round_num = 2

    ra = round(coordinates_dict['right ascension'], round_num)
    dec = round(coordinates_dict['declination'], round_num)

    raw_data_file_name = f"HL Data; {year} day {year_day} or {year}-{month}-{normal_day} {hour};{minute}, duration; {observation_time}(s), Gain; {sdr_gain}(dB), ra and dec; {ra}(hr), {dec}(deg).dat"
    plot_image_file_name = f"HL Plot; {year} day {year_day} or {year}-{month}-{normal_day} {hour};{minute}, duration; {observation_time}(s), Gain; {sdr_gain}(dB), ra and dec; {ra}(hr), {dec}(deg).png"
    spectra_csv_file_name = f"HL CSV; {year} day {year_day} or {year}-{month}-{normal_day} {hour};{minute}, duration; {observation_time}(s), Gain; {sdr_gain}(dB), ra and dec; {ra}(hr), {dec}(deg).csv"


    return raw_data_file_name, plot_image_file_name, spectra_csv_file_name


#Function that gets the time right now and returns it in a year, month, day format
def parse_time() -> str:
    time_tuple = time.localtime()
    
    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday

    virgo_time_string = f"{year}-{month}-{day}"

    return virgo_time_string

#Function to display time on screen
def display_time() -> str:
    time_tuple = time.localtime()

    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday
    hour = time_tuple.tm_hour
    minute = time_tuple.tm_min
    second = time_tuple.tm_sec

    if float(hour) < 10:
        hour = str(f"0{hour}")

    if float(minute) < 10:
        minute = str(f"0{minute}")

    if float(second) < 10:
        second = str(f"0{second}")

    return f"{year}-{month}-{day} {hour}:{minute}:{second}"


#Handles the end of the game loop, so everthing is updated
def end_of_game_loop_button_render(general_screen, button_group) -> None:
    button_group.update()

    for button in button_group:
        Button.cursor_hover(button, pygame.mouse.get_pos())

    button_group.draw(general_screen)

    for button in button_group: 
        Button.draw_basic_button_text(button)


#Function that handles user input to change the location of the observation
def user_change_location_input_list_parse(raw_input, split_char = None) -> list:
    #If the inputs are bad, instead of raising an error, just return an error list
    error_list = [0,0,0]

    try:
        stripped_input = raw_input.strip()
        splited_list = stripped_input.split(",")
    except:
        print("Bad input values.")
        return error_list
    
    if len(splited_list) != 3:
        print("Wrong number of inputs.")
        return error_list
    else: 
        return splited_list


#After the parse function, this will run to update the location values in the dict.I use global varibles here, to keep things clean
def user_change_location_parse(location_list) -> None:
    global default_location_parameters
    error_list = [0,0,0]
    error_value = 0

    if len(location_list) != 3:
        default_location_parameters['height'] = error_value
        default_location_parameters['lat'] = error_value
        default_location_parameters['lon'] = error_value
        print("Not enough values: ", default_location_parameters)
        return None 

    try: 
        default_location_parameters['lat'] = float(location_list[0])
        default_location_parameters['lon'] = float(location_list[1])
        default_location_parameters['height'] = float(location_list[2])
    except:
        default_location_parameters['height'] = error_value
        default_location_parameters['lat'] = error_value
        default_location_parameters['lon'] = error_value
        print("Bad values: ", default_location_parameters)
    finally:
        print("Done updating the location parameters! ", default_location_parameters)
        return None 



#Function that parses the user input of what alt and az the antenna is pointed at
def user_change_az_alt_list_parse(raw_input, split_char = None) -> list:
    
    error_list = [0,0]

    try:
        stripped_input = raw_input.strip()
        splited_list = stripped_input.split(",")
    except:
        print("Bad list values.")
        return error_list
    
    if len(splited_list) != 2:
        print("Wrong number of inputs.")
        return error_list
    else: 
        return splited_list


#After the parsing function runs, this will asign the inputted alt and az and then run it through a function that converts to ra and dec. All the new coordinates are updated in the dict.
def user_change_az_alt_parse(az_alt_input_list) -> None:
    global default_observation_coordinates
    global default_location_parameters
    error_value = 0
    error_list = [0,0]
    az_alt_list = []
    ra_dec_list = []

    if len(az_alt_input_list) != 2:
        default_observation_coordinates['azimuth'] = error_value
        default_observation_coordinates['altitude'] = error_value
        default_observation_coordinates['azimuth and altitude list'] = error_list
        default_observation_coordinates['right ascension'] = error_value
        default_observation_coordinates['declination'] = error_value
        default_observation_coordinates['right ascension and declination list'] = error_list
        print("Not enough values: ", default_observation_coordinates)
        return None 
    
    try: 
        default_observation_coordinates['azimuth'] = float(az_alt_input_list[0])
        default_observation_coordinates['altitude'] = float(az_alt_input_list[1])
    except:
        default_observation_coordinates['azimuth'] = error_value
        default_observation_coordinates['altitude'] = error_value
        default_observation_coordinates['azimuth and altitude list'] = error_list
        default_observation_coordinates['right ascension'] = error_value
        default_observation_coordinates['declination'] = error_value
        default_observation_coordinates['right ascension and declination list'] = error_list
        print("Bad values: ", default_observation_coordinates)
        return None
    

   #Function that gets the ra and dec 
    try:
        ra_dec_list = virgo.equatorial(default_observation_coordinates['altitude'], default_observation_coordinates['azimuth'], 
                     default_location_parameters['lat'], default_location_parameters['lon'], default_location_parameters['height'])
        
    except ValueError as error:
        default_observation_coordinates['azimuth'] = error_value
        default_observation_coordinates['altitude'] = error_value
        default_observation_coordinates['azimuth and altitude list'] = error_list
        default_observation_coordinates['right ascension'] = error_value
        default_observation_coordinates['declination'] = error_value
        default_observation_coordinates['right ascension and declination list'] = error_list

        print("Conversion to right ascension and declination failed. ", error)
        return None


    az_alt_list = [default_observation_coordinates['azimuth'], default_observation_coordinates['altitude']]
    default_observation_coordinates['azimuth and altitude list'] = az_alt_list
   
    default_observation_coordinates['right ascension'] = ra_dec_list[0]
    default_observation_coordinates['declination'] = ra_dec_list[1]

    ra_dec_list = [default_observation_coordinates['right ascension'], default_observation_coordinates['declination']]
    default_observation_coordinates['right ascension and declination list'] = ra_dec_list

    print("Done updating observtion coordinates! ", default_observation_coordinates)


#This function parses and chnages the observation time 
def user_change_and_parse_observation_time(user_time_input) -> None:
   
    global final_observing_values
    global observation_time_offset

    error_value = 10

    try:
        user_time_input = float(user_time_input)

    except ValueError as error:
        print("Bad inputted value. ", error)
        final_observing_values['duration'] = error_value
        return None 
    
    final_observing_values['duration'] = user_time_input + observation_time_offset
    print("Done updating the observation time!", final_observing_values['duration'])


def user_update_ra_and_dec_list_parse(inputted_list) -> str:
    error_list = [0,0]

    try:
        stripped_input = inputted_list.strip()
        splited_list = stripped_input.split(",")
    except:
        print("Bad list values.")
        return error_list
    
    if len(splited_list) != 2:
        print("Wrong number of inputs.")
        return error_list
    else: 
        return splited_list
    
#ra then dec in list
def user_update_ra_and_dec(inputted_list) -> None:
    global default_observation_coordinates
    global default_location_parameters


    #Extra function just so I dont need to copy all the error value assign lines for each wrong case
    def error_value_assign() -> None:
        global default_observation_coordinates
        global default_location_parameters

        
        error_value = 0
        error_list = [0,0]

        default_observation_coordinates['right ascension'] = error_value
        default_observation_coordinates['declination'] = error_value
        default_observation_coordinates['right ascension and declination list'] = error_list
        default_observation_coordinates['altitude'] = error_value
        default_observation_coordinates['azimuth'] = error_value
        default_observation_coordinates['azimuth and altitude list'] = error_list

    
    error_value = 0
    error_list = [0,0]
    total_right_ascension = 24
    total_declination = 90

    if len(inputted_list) != 2: 
        error_value_assign()
        print("Wrong number of values inputted.")
        return None 

    try:
        right_ascension = float(inputted_list[0])
        declination =  float(inputted_list[1])
        coord_list = [right_ascension, declination]

    except ValueError as error:
        error_value_assign()
        print("Bad values were inputted. ", error)

        return None
    

   #Domain of right ascension 
    if right_ascension < 0 or right_ascension > 24:
        error_value_assign()
        print("Inputted right ascension value is not between 0h and 24hr.")

        return None 
    
    #Domain of decliation check
    elif declination < -90 or declination > 90:
        error_value_assign()
        print("Inputted declination is not within -90deg and 90 deg.")

        return None
    

    default_observation_coordinates['right ascension'] = right_ascension
    default_observation_coordinates['declination'] = declination
    default_observation_coordinates['right ascension and declination list'] = coord_list

    default_observation_coordinates['altitude'] = error_value
    default_observation_coordinates['azimuth'] = error_value
    default_observation_coordinates['azimuth and altitude list'] = error_list

    print("Done updating the right ascension and declination. Note the altitude and azimuth does not line up now.")
    

    

#Mr.V's on screen text drawing function. It is really helpful!
def draw_txt(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)




### First game loop for the starting screen ###
#color_button = Button("Night Mode", screen_width/2, screen_height/2)
continue_button = Button("Continue", screen_width/2, screen_height/2)
location_settings_button = Button("Change Location", screen_width/2 -300, screen_height/2)



screen_1_buttons = pygame.sprite.Group()
#screen_1_buttons.add(color_button)
screen_1_buttons.add(continue_button)
screen_1_buttons.add(location_settings_button)
 


running = True 
location_settings_text_state = False
location_settings_user_input = " "
location_settings_parsed_1 = " "

display_clock = None
display_location = None 
location_settings_iterate = 0


screen.fill(main_screen_color)
pygame.display.flip()

while running:
    clock.tick(fps)


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            print("Program will hult now!")
            #Raises basic error so the program will just stop 
            raise WindowsError
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            #If the mouse was clicked, this runs through to see if the mouse was over a button 
            #Button.on_or_off_button_click(color_button, pygame.mouse.get_pos())
            click_state_1 = Button.on_or_off_button_click(continue_button, pygame.mouse.get_pos())
            click_state_2 = Button.on_or_off_button_click(location_settings_button, pygame.mouse.get_pos())

            if continue_button.state == True and click_state_1 == True:
                running = False

            
            #These two if statements will make sure that this only runs if the button was turned on because the button needs to be pressed and the state of the button needs to be on
            if location_settings_button.state == True and click_state_2 == True:
                #Changes a state varbile so the code knows if the user wants to input text
                location_settings_text_state = True
                print("on")
            #Stop inputting text if the button is off now
            else:
                location_settings_text_state = False 


        #User input to change their location (lat, lon, elevation), if a key was hit and the state is true 
        if event.type == pygame.KEYDOWN and location_settings_text_state == True:
            
            #if the user hits 'enter' then the values inputted will be updated and parsed
            if event.key == pygame.K_RETURN:
                print("Varibles set!")
                location_settings_parsed_1 = user_change_location_input_list_parse(location_settings_user_input)
                print("location settings parse", location_settings_parsed_1)
                user_change_location_parse(location_settings_parsed_1)
                
            #if the user deletes a key, then remove the last character in the list
            elif event.key == pygame.K_BACKSPACE:
                location_settings_user_input =  location_settings_user_input[:-1]
            
            #if anyother key is hit then add it to the end of the list
            else:
                location_settings_user_input += event.unicode
            
            print(location_settings_user_input)
    
    
    screen.fill(main_screen_color)   

    display_clock = display_time()
    draw_txt(screen, display_clock, 25, basic_text_color, screen_width/2, 50)

    display_location = f"Latitude: {default_location_parameters['lat']}(deg), Longitude: {default_location_parameters['lon']}(deg), Height: {default_location_parameters['height']}(m)"
    draw_txt(screen, f"Location:", 20, basic_text_color, screen_width/2 + 400, screen_height/2 -30) 
    draw_txt(screen, display_location, 20, basic_text_color, screen_width/2 + 400, screen_height/2)  
    
    

    #Draw the user input for the location settings input only if the button for that is still on
    if location_settings_button.state == True:
        draw_txt(screen, f"like: lat,lon,elv {location_settings_user_input}", 19, basic_text_color, location_settings_button.x_position, location_settings_button.y_position + 50)

    end_of_game_loop_button_render(screen, screen_1_buttons)



    pygame.display.flip()




### Second loop for getting the observation ready, the functions for the user input is the same so there are only comments on the new bits
manual_alt_az_button = Button("Manual Alt/Az", screen_width/2 - 600, screen_height/2 - 300)
auto_alt_az_button = Button("Auto Alt Az", screen_width/2 - 600, screen_height/2 + 100)
hi_display_button = Button("Show Hydrogen Map", screen_width/2 - 600, screen_height/2 + 300)
test_spatial_phidget_button = Button("Test Phidget", screen_width/2 - 600, screen_height/2 - 100)
run_observation_button = Button("Begin Observation", screen_width/2 + 600, screen_height/2 -100)
manual_ra_dec_button = Button("Manual Ra/Dec", screen_width/2 - 300, screen_height/2 + 100)
change_observation_time_button = Button("Change Observation Time", screen_width/2 - 300, screen_height/2 + 300)
select_file_to_plot_button = Button("Plot Selected File", screen_width/2 + 600, screen_height/2 + 300)
plot_just_finished_observation_button = Button("Plot Data", screen_width/2 + 600, screen_height/2 + 100)


screen_2_buttons = pygame.sprite.Group()
screen_2_buttons.add(manual_alt_az_button)
screen_2_buttons.add(auto_alt_az_button)
screen_2_buttons.add(hi_display_button)
screen_2_buttons.add(test_spatial_phidget_button)
screen_2_buttons.add(run_observation_button)
screen_2_buttons.add(change_observation_time_button)
#screen_2_buttons.add(select_file_to_plot_button)
screen_2_buttons.add(plot_just_finished_observation_button)
screen_2_buttons.add(manual_ra_dec_button)


running = True 
inital_time = time.time()
final_time = time.time()
wait_time = 10

#These all are created at the same time when the observation is ran but may or may not be used
#I might want to combine all these functions into one just for ease of coding
observation_output_data_file_name = None
observation_image_plot_name = None
observation_csv_file_name = None

manual_alt_az_text_state = False 
manual_alt_az_user_input = " "
manual_alt_az_user_input_parsed = " "

observation_time_text_state = False 
observation_time_input = " "
observation_time_input_parsed = " "

manual_ra_dec_text_state = False 
manual_ra_dec_user_input = " "
manual_ra_dec_user_input_parsed = " "

display_clock = None
display_location = None 
display_coordinates_1 = None
display_coordinates_2 = None
display_round = 2

width_constant = -260
display_value_x_location = screen_width/2 + width_constant



screen.fill(main_screen_color)
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
            click_state_1 =Button.on_or_off_button_click(manual_alt_az_button, pygame.mouse.get_pos())
            temp_state_5 =Button.doer_button_click(auto_alt_az_button, pygame.mouse.get_pos())
            temp_state_1 = Button.doer_button_click(hi_display_button, pygame.mouse.get_pos())
            temp_state_2 = Button.doer_button_click(test_spatial_phidget_button, pygame.mouse.get_pos())
            temp_state_3 = Button.doer_button_click(run_observation_button, pygame.mouse.get_pos())
            temp_state_4 = Button.doer_button_click(plot_just_finished_observation_button, pygame.mouse.get_pos())
            click_state_2 = Button.on_or_off_button_click(change_observation_time_button, pygame.mouse.get_pos())
            click_state_3 = Button.on_or_off_button_click(manual_ra_dec_button, pygame.mouse.get_pos())


            #This handles the manual alt and az input from the user
            if manual_alt_az_button.state == True and click_state_1 == True:
                manual_alt_az_text_state = True
            else:
                manual_alt_az_text_state = False

            if change_observation_time_button.state == True and click_state_2 == True:
                observation_time_text_state = True
            else: 
                observation_time_text_state = False

            if manual_ra_dec_button.state == True and click_state_3 == True:
                manual_ra_dec_text_state = True
            else: 
                manual_ra_dec_text_state = False


            #Displays a map of the hydrogen line strength and a dot to show where the antenna is pointed at
            if temp_state_1 == True: 
                virgo.map_hi(default_observation_coordinates['right ascension'], default_observation_coordinates['declination'])


            #Tries to initalize the angle phidget sensor
            if temp_state_2 == True: 
                angle_sensor = Spatial()
                try:
                    angle_sensor.openWaitForAttachment(attachment_time)
                except PhidgetException as error:
                    print("The phidget is probably not attached, ", error)
                else:
                    print("The angle sensor is connected!")


            #Button that tries to run the obseravtion
            if temp_state_3 == True:
                final_observing_values['loc']
                final_observing_values['duration'] = observing_time
                final_observing_values['rf_gain'] = sdr_rf_gain
                final_observing_values['ra_dec'] = observation_ra_dec
                final_observing_values['az_alt'] = observation_az_alt

                observation_output_data_file_name, observation_image_plot_name, observation_csv_file_name = output_file_name_assigner_function()
                print(observation_output_data_file_name)

                try: 
                    virgo.observe(final_observing_values, 'wola', observation_output_data_file_name,start_in = observation_start_time)
                    print("Observation is complete!")
                except ModuleNotFoundError as error:
                    print("Check if the SDR is connected")
                    print(error)

            
            #Button that plots the most resent data while the script was open
            if temp_state_4 == True: 

                try: 
                    virgo.plot(obs_parameters= default_observing_values, n = 20, m =35, f_rest= hydrogen_line_freq,
                                vlsr=False, meta=False, avg_ylim=(-5,15), cal_ylim=(-20,260), obs_file= observation_output_data_file_name,
                                rfi=[(1419.2e6, 1419.3e6), (1420.8e6, 1420.9e6)], dB=True, spectra_csv=observation_csv_file_name, plot_file=observation_image_plot_name)
                    
                except Exception as error: 
                    print("Propably no observation has been done while this was open", error)

            if temp_state_5 == True: 
                print("There is no code here yet.")
                

                
        #Text input for the alt and az and conversion to ra and dec, I need to add galatic cordinates
        if event.type == pygame.KEYDOWN and manual_alt_az_text_state == True:

            if event.key == pygame.K_RETURN:
                print("Varibles set!")
                manual_alt_az_user_input_parsed = user_change_az_alt_list_parse(manual_alt_az_user_input)
                print("location settings parse", manual_alt_az_user_input_parsed)
                user_change_az_alt_parse(manual_alt_az_user_input_parsed)
                
            elif event.key == pygame.K_BACKSPACE:
                manual_alt_az_user_input =  manual_alt_az_user_input[:-1]

            else:
                manual_alt_az_user_input += event.unicode
            
            print(manual_alt_az_user_input)


        #Text input for observation time
        elif event.type == pygame.KEYDOWN and observation_time_text_state == True:

            if event.key == pygame.K_RETURN:
                print("Varibles set!")
                user_change_and_parse_observation_time(observation_time_input)

            elif event.key == pygame.K_BACKSPACE:
                observation_time_input =  observation_time_input[:-1]

            else:
                observation_time_input += event.unicode
            
            print(observation_time_input)

        #Input to manually change the ra and dec, it does not back calculate the alt and az though
        elif event.type == pygame.KEYDOWN and manual_ra_dec_text_state == True:

            if event.key == pygame.K_RETURN:
                print("Varibles set!")
                manual_ra_dec_user_input_parsed = user_update_ra_and_dec_list_parse(manual_ra_dec_user_input)
                user_update_ra_and_dec(manual_ra_dec_user_input_parsed)

            elif event.key == pygame.K_BACKSPACE:
                manual_ra_dec_user_input =  manual_ra_dec_user_input[:-1]

            else:
                manual_ra_dec_user_input += event.unicode
            
            print(manual_ra_dec_user_input)


    screen.fill(main_screen_color)


    display_clock = display_time()
    draw_txt(screen, display_clock, 25, basic_text_color, screen_width/2, 50)

    display_location_1 = f"Latitude: {default_location_parameters['lat']}(deg), Longitude: {default_location_parameters['lon']}(deg)"
    display_location_2 = f"Height: {default_location_parameters['height']}(m)"
    
    draw_txt(screen, f"Location:", 20, basic_text_color, display_value_x_location, screen_height/2 - 300) 
    draw_txt(screen, display_location_1, 20, basic_text_color, display_value_x_location, screen_height/2 - 270) 
    draw_txt(screen, display_location_2, 20, basic_text_color, display_value_x_location, screen_height/2 - 240) 

    #default_observation_coordinates['']
    display_coordinates_1 = f"Azimuth: {default_observation_coordinates['azimuth']}(deg), Altitude: {default_observation_coordinates['altitude']}(deg)"
    display_coordinates_2 = f"Right Ascension: {round(default_observation_coordinates['right ascension'],display_round)}(hr), Declination: {round(default_observation_coordinates['declination'], display_round)}(deg)"
    
    draw_txt(screen, f"Coordinates:", 20, basic_text_color, display_value_x_location, screen_height/2 - 180)
    draw_txt(screen, display_coordinates_1, 20, basic_text_color, display_value_x_location, screen_height/2 - 150)
    draw_txt(screen, display_coordinates_2, 20, basic_text_color, display_value_x_location, screen_height/2 - 120)

    draw_txt(screen, f"Observation Time: {final_observing_values['duration'] - observation_time_offset}(s)", 20, basic_text_color, display_value_x_location, screen_height/2 - 60)
    draw_txt(screen, f"SDR Gain: {final_observing_values['rf_gain']}(dB)", 20, basic_text_color, display_value_x_location, screen_height/2 - 30)
 

    if manual_alt_az_button.state == True:
        draw_txt(screen, f"like: az,alt {manual_alt_az_user_input}", 19, basic_text_color, manual_alt_az_button.x_position, manual_alt_az_button.y_position + 50)

    if change_observation_time_button.state == True:
        draw_txt(screen, f"like: time {observation_time_input}", 19, basic_text_color, change_observation_time_button.x_position, change_observation_time_button.y_position + 50)
    
    if manual_ra_dec_button.state == True:
        draw_txt(screen, f"like: ra,dec {manual_ra_dec_user_input}", 19, basic_text_color, manual_ra_dec_button.x_position, manual_ra_dec_button.y_position + 50)

    
    end_of_game_loop_button_render(screen, screen_2_buttons)

    pygame.display.flip()







test = Observation("testinggg", default_observing_values, default_location_parameters)

print(test.date)

virgo.predict(default_location_parameters['lat'], default_location_parameters['lon'], default_location_parameters['height'], source= 'Cas A', date= '2024-4-20')
virgo.map_hi(6,45)
