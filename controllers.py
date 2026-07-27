from models import DistanceModel

class MarketController:

    def __init__(self):

        self.distance_unit = "miles"

    def convert_distance(self, distance):

        if self.distance_unit == "km":

            return DistanceModel.miles_to_km(
                distance
            )

        return distance