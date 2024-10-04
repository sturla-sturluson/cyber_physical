from src import CarRunner
import pygame
import os
import datetime as dt


def main():
    motor_2_gpio_1 = 6
    motor_2_gpio_2 = 13
    motor_1_gpio_1 = 20
    motor_1_gpio_2 = 21
    w_pressed = False
    s_pressed = False
    a_pressed = False
    d_pressed = False

    q_pressed = False

    pygame.display.set_mode((400, 500))
 
    # Setting name for window
    pygame.display.set_caption('GeeksforGeeks')

    with CarRunner((motor_1_gpio_1,motor_1_gpio_2),(motor_2_gpio_1,motor_2_gpio_2)) as car_runner:
        # Create a pygame game loop
        pygame.init()
        # Keyboard events
        running = True


        
        # Game loop
        # keep game running till running is true
        while running:
            # set frame rate to 1 frame per second
            pygame.time.delay(1000)


            #os.system('clear')
            print(f"Time: {dt.datetime.strftime(dt.datetime.now(),'%H:%M:%S')}")
            print("Press keys (press 'q' to quit)")
            print(f"W: {w_pressed} S: {s_pressed} A: {a_pressed} D: {d_pressed}")
            # Check for event if user has pushed 
            # any event in queue
            for event in pygame.event.get():
                # if event is of type keydown
                if event.type == pygame.KEYDOWN:
                    # if key is w set w_pressed to True
                    if event.key == pygame.K_w:
                        w_pressed = True
                    # if key is s set s_pressed to True
                    if event.key == pygame.K_s:
                        s_pressed = True
                    # if key is a set a_pressed to True
                    if event.key == pygame.K_a:
                        a_pressed = True
                    # if key is d set d_pressed to True
                    if event.key == pygame.K_d:
                        d_pressed = True
                    # if key is q set q_pressed to True
                    if event.key == pygame.K_q:
                        q_pressed = True
            
                # if event is of type quit then set
                # running bool to false
                if event.type == pygame.QUIT:
                    running = False
            # if w is pressed then move forward
            # car_runner.set_wasd(w_pressed,s_pressed,a_pressed,d_pressed)
            # if q is pressed then shut down
            if q_pressed:
                car_runner.shut_down()
            # if space is pressed then stop the motor

if __name__ == "__main__":
    main()