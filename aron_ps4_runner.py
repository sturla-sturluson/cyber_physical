from src .ps4_controller .ps4_aron import PS4_Aron

from src.motor import CarRunner





def main():
    stop_range = 40 # in cm
    with CarRunner(
        stop_range=stop_range
        ) as car_runner:
        input("Press enter to start")
        listener = PS4_Aron(car_runner)

    


if __name__ == "__main__":
    main()