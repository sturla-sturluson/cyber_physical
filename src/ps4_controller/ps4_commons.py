import pygame

BUTTON_MIN_MAX_RELEASED_MAP = {"min":0,"max":1,"released":0}


ps4_buttons = {
    0: {"name":"Square"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    1: {"name":"Cross"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    2: {"name":"Circle"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    3: {"name":"Triangle"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    # D-pad
    11: {"name":"Up"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    12: {"name":"Down"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    13: {"name":"Left"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    14: {"name":"Right"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    # L1, R1, L2, R2
    4: {"name":"L1"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    5: {"name":"R1"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    6: {"name":"L2"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    7: {"name":"R2"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    # joystick buttons
    10: {"name":"L3"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    11: {"name":"R3"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    # Share, Options, PS
    8: {"name":"Share"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    9: {"name":"Options"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    12: {"name":"PS"}.update(*BUTTON_MIN_MAX_RELEASED_MAP),
    
}

ps4_axis = {
    0: {"name":"Left Stick X","min":-1,"max":1,"released":0},
    1: {"name":"Left Stick Y","min":-1,"max":1,"released":0},
    2: {"name":"Right Stick X","min":-1,"max":1,"released":0},
    5: {"name":"Right Stick Y","min":-1,"max":1,"released":0},
    3: {"name":"L2","min":-1,"max":1,"released":-1},
    4: {"name":"R2","min":-1,"max":1,"released":-1},
}


def button_id_tester():
    pygame.init()
    # window = pygame.display.set_mode((800, 600))

    running = True
    fps = 5
    clock = pygame.time.Clock()

    # Init joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    while running:

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if( event.type == pygame.JOYBUTTONDOWN):
                print(f"Button Pressed : {event.button} : {ps4_buttons.get(event.button),'Not found'}")
            if(event.type == pygame.JOYBUTTONUP):
                print(f"Button Released : {event.button} : {ps4_buttons.get(event.button,'Not found')}")
            if(event.type == pygame.JOYAXISMOTION and abs(event.value) > 0.1):
                print(f"Axis Motion : {event.axis} : {event.value}")


