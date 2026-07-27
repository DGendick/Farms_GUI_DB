class DistanceModel:

    MILES_TO_KM = 1.60934


    @staticmethod
    def miles_to_km(miles):

        return round(
            miles * DistanceModel.MILES_TO_KM,
            2
        )