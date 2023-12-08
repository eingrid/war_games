import json
import random
import requests
from abc import ABC, abstractmethod
import utils

DELTA_SERVER_URL = "http://localhost:5000/api/"

class DeltaAPI(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DeltaAPI, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def detect(self, units):
        """Simulates the detection of units from aerial data.

        This method mimics the process of object detection from aerial data, introducing noise to the ground truth
        (g.t.) units' positions and incorporating the probability of correct detection.

        Args:
        units (list): A list of units representing objects to be detected. Each unit may contain information such as
                    coordinates, type, and other relevant data.

        Returns:
        list: A list of detected units. The detected units incorporate noise in their positions and the probability
            of successful detection, providing a simulated representation of the detected objects based on the
            given aerial data.

        Note:
        The function doesn't modify the original 'units' data; instead, it returns a new list with simulated
        detection results.
        """
        delta_response = {}
        delta_response["forces"] = []
        for unit in units:
            delta_response["forces"].append(
                {
                    "location": {
                        "longtitude": unit.longtitude,
                        "latitude": unit.latitude,
                    },
                    "object_name": unit.name,
                    "object_confidence": 0.8,
                }
            )
            
        return delta_response

    @abstractmethod
    def fetch_json(self, name):
        pass
    
class DeltaLocal(DeltaAPI):
    def __init__(self):
        pass

    def fetch_json(self, name):        
        data = json.load(open(utils.get_absolute_path(f"/input/{name}.json"), "r"))
        return data 

class DeltaRemote(DeltaAPI):
    def __init__(self):
        pass

    def fetch_json(self, name):
        url = DELTA_SERVER_URL + name
        response = requests.get(url)
        data = response.json().get("data")
        return data
    
def api():
    return DeltaLocal()

def allies():
    return api().fetch_json("allies").get("forces")

def enemy():
    return api().fetch_json("enemy").get("forces")

