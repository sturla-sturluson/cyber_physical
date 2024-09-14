import board


def get_gpio_pin_number(number: int):

    # Available numbers are
    # Left Side
    #  4,17,27,22, 5, 6,13,19,26
    # Right Side
    # 18,23,24,25,12,16,20,21
    if number == 4:
        return board.D4
    elif number == 17:
        return board.D17
    elif number == 27:
        return board.D27
    elif number == 22:
        return board.D22
    elif number == 5:
        return board.D5
    elif number == 6:
        return board.D6
    elif number == 13:
        return board.D13
    elif number == 19:
        return board.D19
    elif number == 26:
        return board.D26
    elif number == 18:
        return board.D18
    elif number == 23:
        return board.D23
    elif number == 24:
        return board.D24
    elif number == 25:
        return board.D25
    elif number == 12:
        return board.D12
    elif number == 16:
        return board.D16
    elif number == 20:
        return board.D20
    elif number == 21:
        return board.D21
    else:
        raise ValueError("Invalid GPIO pin number")