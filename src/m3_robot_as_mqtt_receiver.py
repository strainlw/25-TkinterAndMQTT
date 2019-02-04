"""
Using a Brickman (robot) as the receiver of messages.
"""

# Same as m2_fake_robot_as_mqtt_sender,
# but have the robot really do the action.
# Implement just FORWARD at speeds X and Y is enough.

import time
import mqtt_remote_method_calls as com
import math
import ev3dev.ev3 as ev3

class SimpleRoseBot(object):
    def __init__(self):
        self.leftmotor = Motor('B')
        self.rightmotor = Motor('C')
        self.sensor = ColorSensor(3)

    def go(self, leftspeed, rightspeed):
        self.leftmotor.turn_on(leftspeed)
        self.rightmotor.turn_on(rightspeed)

    def stop(self):
        self.leftmotor.turn_off()
        self.rightmotor.turn_off()

    def go_straight_for_seconds(self, seconds, speed):
        self.go(speed, speed)
        start = time.time()
        while True:
            current = time.time()
            if current - start >= seconds:
                break
        self.stop()

    def go_straight_for_inches(self,inches,speed):

        self.go(speed, speed)
        while True:
            current = (self.leftmotor.get_position()/360)*4.08207
            print(current)
            if current >= inches:
                break
        self.stop()

    def go_straight_until_black(self,speed):
        self.go(speed)
        while True:
            if self.sensor.get_reflected_light_intensity() <= 10:
                break
        self.stop()

class Motor(object):
    WheelCircumference = 1.3 * math.pi

    def __init__(self, port):  # port must be 'B' or 'C' for left/right wheels
        self._motor = ev3.LargeMotor('out' + port)

    def turn_on(self, speed):  # speed must be -100 to 100
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0

class ColorSensor(object):
    def __init__(self, port):  # port must be 3
        self._color_sensor = ev3.ColorSensor('in' + str(port))

    def get_reflected_light_intensity(self):
        # Returned value is from 0 to 100,
        # but in practice more like 3 to 90+ in our classroom lighting.
        return self._color_sensor.reflected_light_intensity

rob = SimpleRoseBot()

class DelegateThatReceives(object,rob):

    def forward(self, left, right):
        rob.go(left, right)
        






def main():
    name1 = input("Enter one name (subscriber): ")
    name2 = input("Enter another name (publisher): ")

    my_delegate = DelegateThatReceives()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.



    while True:
        time.sleep(0.01)  # Time to allow message processing


main()
