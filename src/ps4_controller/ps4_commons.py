import pygame

BUTTON_MIN_MAX_RELEASED_MAP = {"min":0,"max":1,"released":0}


ps4_buttons = {
    3: {"name":"Square","min":0,"max":1,"released":0},
    0: {"name":"Cross","min":0,"max":1,"released":0},
    1: {"name":"Circle","min":0,"max":1,"released":0},
    2: {"name":"Triangle","min":0,"max":1,"released":0},
    # D-pad
    11: {"name":"Up","min":0,"max":1,"released":0},
    12: {"name":"Down","min":0,"max":1,"released":0},
    13: {"name":"Left","min":0,"max":1,"released":0},
    14: {"name":"Right","min":0,"max":1,"released":0},
    # L1, R1, L2, R2
    4: {"name":"L1","min":0,"max":1,"released":0},
    5: {"name":"R1","min":0,"max":1,"released":0},
    6: {"name":"L2","min":0,"max":1,"released":0},
    7: {"name":"R2","min":0,"max":1,"released":0},
    # joystick buttons
    10: {"name":"L3","min":0,"max":1,"released":0},
    11: {"name":"R3","min":0,"max":1,"released":0},
    # Share, Options, PS
    8: {"name":"Share","min":0,"max":1,"released":0},
    9: {"name":"Options","min":0,"max":1,"released":0},
    12: {"name":"PS","min":0,"max":1,"released":0},
    
}

ps4_axis = {
    0: {"name":"Left Stick X","min":-1,"max":1,"released":0},
    1: {"name":"Left Stick Y","min":-1,"max":1,"released":0},
    3: {"name":"Right Stick X","min":-1,"max":1,"released":0},
    4: {"name":"Right Stick Y","min":-1,"max":1,"released":0},
    2: {"name":"L2","min":-1,"max":1,"released":-1},
    5: {"name":"R2","min":-1,"max":1,"released":-1},
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
                print(f"Axis Moved : {event.axis} : {ps4_axis.get(event.axis,'Not found')} : {event.value:.2f}")


