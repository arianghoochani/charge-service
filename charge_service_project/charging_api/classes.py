class ChargingRequestValidator:
    def __init__(self, station_id, driver_token, callback_url):
        self.station_id = station_id
        self.driver_token = driver_token
        self.callback_url = callback_url