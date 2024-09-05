from src import Led



def main():
    led = Led(22)
    try:
        while True:
            response = input("Enter on or off: ")
            led.toggle()
    except KeyboardInterrupt:
        led.cleanup()
        print("Exiting")
    except Exception as e:
        print(e)
        led.cleanup()
        print("Exiting")
    finally:
        led.cleanup()
        print("Exiting")

if __name__ == "__main__":
    main()