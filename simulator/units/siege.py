import objects

class Onager(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 275,
            defense = 275,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.siege,
            abilities = ["no counter"]
        )

class Rams(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 400,
            defense = 325,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.siege,
            abilities = ["no counter", "only buildings"]
        )

class SiegeRams(Rams):
    def __init__(self):
        super().__init__()
        self.name = "Siege Rams"
        self.attack = 500
        self.defense = 375

class Scorpions(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 350,
            defense = 250,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.siege,
            abilities = ["no counter", "only units"]
        )

class HeavyScorpions(Scorpions):
    def __init__(self):
        super().__init__()
        self.name = "Heavy Scorpions"
        self.attack = 400
        self.defense = 300

class Trebuchets(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 370,
            defense = 350,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.siege,
            abilities = ["no counter", "min 2"]
        )

class Bombards(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 325,
            defense = 325,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.siege,
            abilities = ["no counter"]
        )




