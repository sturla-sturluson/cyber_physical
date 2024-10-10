import pygame

ps4_buttons = {
    0: "Square",
    1: "X",
    2: "Circle",
    3: "Triangle",
    # D-pad
    11: "Up",
    12: "Down",
    13: "Left",
    14: "Right",
    # L1, R1, L2, R2
    4: "L1",
    5: "R1",
    6: "L2",
    7: "R2",
    # joystick buttons
    10: "L3",
    11: "R3",
    # Share, Options, PS
    8: "Share",
    9: "Options",
    12: "PS",
    
}

ps4_axis = {
    0: "Left Stick X",
    1: "Left Stick Y",
    2: "Right Stick X",
    5: "Right Stick Y",
    3: "L2", # -1 Neutral , 1 Fully pressed
    4: "R2", # -1 Neutral , 1 Fully pressed
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


