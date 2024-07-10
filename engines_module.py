import queue
import threading
import time
from utils.message import Message
import RPi.GPIO as GPIO
from time import sleep, time

class MotorModule:
    
    # Motor control pins
    PWM_PIN = 18  # GPIO pin for PWM (connect to PWM1)
    DIR_PIN = 23  # GPIO pin for direction (connect to DIR1)

    # Encoder pins
    ENCODER_A_PIN = 24  # GPIO pin for encoder A output
    ENCODER_B_PIN = 25  # GPIO pin for encoder B output

    # Encoder state
    encoder_count = 0
    last_time = time()

    # Encoder parameters
    PULSES_PER_REV = 6 * 45  # Number of encoder pulses per wheel revolution
    desired_revolutions = 0  # Desired number of wheel revolutions
    
    def __init__(self, communication_queue, stop_event, **kwargs):
        self.communication_queue = communication_queue
        self.stop_event = stop_event

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PWM_PIN, GPIO.OUT)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.ENCODER_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.ENCODER_B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Set up PWM
        global pwm
        pwm = GPIO.PWM(self.PWM_PIN, 1000)  # 1kHz frequency
        pwm.start(0)  # Start with 0% duty cycle

        # Set up encoder interrupts
        GPIO.add_event_detect(self.ENCODER_A_PIN, GPIO.BOTH, callback=self.encoder_callback)
        GPIO.add_event_detect(self.ENCODER_B_PIN, GPIO.BOTH, callback=self.encoder_callback)

    def encoder_callback(self):
        a_state = GPIO.input(self.ENCODER_A_PIN)
        b_state = GPIO.input(self.ENCODER_B_PIN)

        if a_state == b_state:
            self.encoder_count += 1
        else:
            self.encoder_count -= 1

        if abs(self.encoder_count) >= self.desired_revolutions * self.PULSES_PER_REV:
            self.set_motor_speed(0)  # Stop motor

    def set_motor_speed(self, speed):
        if speed >= 0:
            GPIO.output(self.DIR_PIN, GPIO.HIGH)
        else:
            GPIO.output(self.DIR_PIN, GPIO.LOW)
            speed = -speed
        pwm.ChangeDutyCycle(speed)

    def print_encoder_count(self):
        current_time = time()
        elapsed_time = current_time - self.last_time
        print(f"Encoder count: {self.encoder_count} (Elapsed time: {elapsed_time:.2f} seconds)")
        self.last_time = current_time

    def cleanup(self):
        pwm.stop()
        GPIO.cleanup()

    def run_motor_for_revolutions(self, revolutions, speed):
        current_time = time()
        self.encoder_count = 0  # Reset encoder count
        self.desired_revolutions = revolutions
        self.set_motor_speed(speed)
        self.print_encoder_count()
        while not self.stop_event.is_set():
            elapsed_time = current_time - self.last_time
            print(f"Encoder count: {self.encoder_count} (Elapsed time: {elapsed_time:.2f} seconds)")
            self.last_time = current_time
            if abs(self.encoder_count) > self.desired_revolutions * self.PULSES_PER_REV:
                self.stop_event.set()
            sleep(0.5)  # Sleep for a short period to avoid busy waiting
        self.set_motor_speed(0)  # Ensure the motor is stopped
        self.cleanup()
