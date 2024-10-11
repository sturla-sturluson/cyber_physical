import pygame

ps4_buttons = {
    0: "X",
    1: "Circle",
    2: "Square",
    3: "Triangle",
    # D-pad
    11: "Up",
    12: "Down",
    13: "Left",
    14: "Right",
    # L1, R1, L2, R2
    9: "L1",
    10: "R1",
    # joystick buttons
    7: "L3",
    8: "R3",
    # Share, Options, PS
    4: "Share",
    6: "Options",
    5: "PS",
    
}

ps4_axis = {
    0: "Left Stick X",
    1: "Left Stick Y",
    2: "Right Stick X",
    3: "Right Stick Y",
    4: "L2", # -1 Neutral , 1 Fully pressed
    5: "R2", # -1 Neutral , 1 Fully pressed
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
                print(f"Button Pressed : {event.button}")
            if(event.type == pygame.JOYBUTTONUP):
                print(f"Button Released : {event.button}")
            if(event.type == pygame.JOYAXISMOTION and abs(event.value) > 0.1):
                print(f"Axis Motion : {event.axis} : {event.value}")


