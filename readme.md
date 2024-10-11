# Cyber Physical Systems

## Sturla Emil Sturluson


###

Preamble
Highly recommended to create a venv for this

    python3 -m venv venv

To activate the venv 

    source venv/bin/activate

To install all the packages run

    pip install -r requirements.txt

Possible depending on your setup that you need to have pip or venv installed (ubuntu at least)

To run 

    python3 run_screen.py

This turns on a non timed slideshow, where you can switch between what is displayed. 

    -h, --help        show this help message and exit
    -ip               Display the IP address
    -slide <seconds>  Run the slide show with the specified number of seconds per slide, can be paired with -ip
    -compass          Display the compass, add -cal to calibrate the compass
    -rgb              Display the RGB sensor
    -range            Display the range sensor, add -cal to calibrate the range sensor
    -cal              Calibrate the compass or range sensor


.env file can also be used to change some connection values

    .env

    # The led pin
    LED_PIN=26
    # Range sensor pin
    RANGE_SENSOR_PIN=5
    # Engine gpio pins
    AIN1_PIN=20
    AIN2_PIN=21
    BIN1_PIN=6
    BIN2_PIN=13
    # The motor controller sleep pin
    SLEEP_PIN=25


