class ChargingRequestValidatorInput:
    def __init__(self, station_id, driver_token, callback_url):
        self.station_id = station_id
        self.driver_token = driver_token
        self.callback_url = callback_url

class ChargingRequestValidatorResponse:
    statusDB = {
        "accepted":{
            "status": "accepted",
            "message":"Request is being processed asynchronously. The result will be sent to the provided callback URL."
        },
        "station_id":{
            "status": "rejected",
            "message":"station_id is invalid."
        },
         "driver_token":{
            "status": "rejected",
            "message":"driver_token is invalid."
        },
        "callback_url":{
            "status": "rejected",
            "message":"callback_url is invalid."
        },
        "unknown":{
            "status": "rejected",
            "message":"unknown error has been occured."
        }
    }
    def __init__(self, status = "accepted"):
        self.status = ChargingRequestValidatorResponse.statusDB[status]["status"]
        self.message = ChargingRequestValidatorResponse.statusDB[status]["message"]


class CheckAuthorityRequest:
    def __init__(self, station_id="", driver_token="", callback_url="", request_time=""):
        self.station_id = station_id
        self.driver_token = driver_token
        self.callback_url = callback_url
        self.request_time = request_time

class CheckAuthorityResponse:
    def __init__(self):
        self.message = message


class InsertACLRequest:
    def __init__(self, station_id="", driver_token=""):
        self.station_id = station_id
        self.driver_token = driver_token

class InsertACLResponse:
    def __init__(self,flag=""):
        self.flag = flag