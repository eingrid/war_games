import json
import random


class DeltaAPI:
    def __init__(self) -> None:
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


#        {
#     "forces":[
#         {
#             "location": {
#                 "longtitude": 12,
#                 "latitude": 18
#             },
#             "object_name": "tank",
#             "object_confidence": 0.8
#         },
#         {
#             "location": {
#                 "longtitude": 5,
#                 "latitude": 12
#             },
#             "located_by": "drone1697i2bg335",
#             "object_name": "mlrs",
#             "object_confidence": 0.9
#         },
#         {
#             "timestamp": 0,
#             "location": {
#                 "longtitude": 2,
#                 "latitude": 8
#             },
#             "located_by": "drone1697i2bg335",
#             "object_name": "stormtrooper",
#             "object_confidence": 0.8
#         }
#     ]
# }
