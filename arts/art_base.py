from src.shape import *


class ArtBase:
    def __init__(self) -> None:
        pass

    def create_shapes(self):
        pass

    def create_combined_shape(self):
        return CombinedShape(None, self.create_shapes())
    