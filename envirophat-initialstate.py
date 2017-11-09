#!/usr/bin/env python

import time
from envirophat import light, weather
from ISStreamer.Streamer import Streamer

# Create a Streamer instance
streamer = Streamer(bucket_name="Your Bucket Name", bucket_key="bucket_key", access_key="your_access_key")

# Set the time to wait between sending data to Initial State (in seconds). Default is 60.
period = 60

def InitialState():
  while True:
    ### Assume - the '-2' is a temperature calibration to take the Pi's heat into consideration. Adjust if needed.
    temperature, pressure, lux = weather.temperature() -2, weather.pressure()/100, light.light()
    if temperature is not None and pressure is not None and lux is not None:
        print ("Temp={0:.1f}*C   Pressure={1:.0f} hPa   Light={2:.0f} lux".format(temperature, pressure, lux))
        try:
          # Send temperature to Initial State
          streamer.log("Temperature", temperature)
          # Send pressure to Initial State
          streamer.log("Pressure", pressure)
          # Send light to Initial State
          streamer.log("Lux", lux)
          # Flush and close the stream
          streamer.close()

        except KeyboardInterrupt:
          pass

    else:
        print ("Failed to get reading. Try again!")

    # Sleep for the set period
    time.sleep(period)

InitialState()
