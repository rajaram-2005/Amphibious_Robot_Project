import gpsd

# Initialize GPSD and return the current location
def get_gps_location():
    gpsd.connect()  # Connect to the local GPS
    packet = gpsd.get_current()  # Get current GPS location
    if packet.mode >= 2:
        return packet.lat, packet.lon
    else:
        return None, None
