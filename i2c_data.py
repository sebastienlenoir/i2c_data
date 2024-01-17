#!/usr/bin/env python

# Copyright [2024] [Sébastien LENOIR of copyright owner]
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import socket
import json
from json import JSONEncoder
from icm20948 import ICM20948
from smbus2 import SMBus
from bme280 import BME280


imu = ICM20948(i2c_addr=0x69)
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus, i2c_addr=0x77)

class Payload:
  temperature: float
  humidity: float
  pressure: float
  gyroscope_x: float
  gyroscope_y: float
  gyroscope_z: float
  accelerometer_x: float
  accelerometer_y: float
  accelerometer_z: float
  magnetometer_x: float
  magnetometer_x: float
  magnetometer_z: float
  
  def __init__(self, temperature: float, humidity: float, pressure: float, gyroscope_x: float, gyroscope_y: float, gyroscope_z: float, accelerometer_x: float, accelerometer_y: float, accelerometer_z: float, magnetometer_x: float, magnetometer_y: float, magnetometer_z: float) -> None:
    self.temperature = temperature
    self.humidity = humidity
    self.pressure = pressure
    self.gyroscope_x = gyroscope_x
    self.gyroscope_y = gyroscope_y
    self.gyroscope_z = gyroscope_z
    self.accelerometer_x = accelerometer_x
    self.accelerometer_y = accelerometer_y
    self.accelerometer_z = accelerometer_z
    self.magnetometer_x = magnetometer_x
    self.magnetometer_y = magnetometer_y
    self.magnetometer_z = magnetometer_z
   
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
  # Read magnetometer data from ICM20948
  try:
    x, y, z = imu.read_magnetometer_data()
  except Exception as error:
    print('An error occured when reading magnetometer data:', error)
    x, y, z = 9999, 9999, 9999
  
  # Read accelerometer & gyro data from ICM20948
  try:
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
  except Exception as error:
    print('An error occured when reading accelerometer & gyro data:', error)
    ax, ay, az, gx, gy, gz = 9999, 9999, 9999, 9999, 9999, 9999
  
  # Read temperature value from BME280
  try:
    t = bme280.get_temperature()
  except Exception as error:
    print('An error occured when reading temperature value on BME280:', error)
    t = 9999

  # Read pressure value from BME280
  try:
    p = bme280.get_pressure()
  except Exception as error:
    print('An error occured when reading pressure value on BME280:', error)
    p = 9999

  # Read humidity value from BME280
  try:
    h = bme280.get_humidity()
  except Exception as error:
    print('An error occured when reading humidity value on BME280:', error)
    h = 9999
  
  # Build payload from collected values
  payload = Payload(temperature = t, pressure = p, humidity = h,
                    gyroscope_x = gx, gyroscope_y = gy, gyroscope_z = gz,
                    accelerometer_x = ax, accelerometer_y = ay, accelerometer_z = az,
                    magnetometer_x = x, magnetometer_y = y, magnetometer_z = z)
  
  # Convert Payload to JSON and send it over UDP
  MESSAGE = payload.toJson()
  sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
  
  time.sleep(0.01)
