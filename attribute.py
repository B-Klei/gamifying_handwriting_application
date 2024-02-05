class Attribute:
    def __init__(self, std_limit, colour):
        self.std_limit = std_limit  # maximum standard deviation for which a badge is assigned
        self.colour = colour  # colour assigned for attribute
        self.points = 0  # points earned for the attribute
        self.point_list = []  # list of earned points
        self.badges = 0  # number of badges earned for the attribute
