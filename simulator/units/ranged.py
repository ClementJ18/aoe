import objects

class Longbowmen(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 225,
            defense = 150,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.ranged,
            abilities = ["volley"]
        )

class EliteLongbowmen(Longbowmen):
    def __init__(self):
        super().__init__()
        self.name = "Elite Longbowmen"
        self.attack = 275
        self.defense = 250

class Skirmishers(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 110,
            defense = 110,
            range = 2,
            movement = 7,
            vision = 7,
            type = objects.UnitType.ranged,
            abilities = ["skirmish"]
        )

class EliteSkirmishers(Skirmishers):
    def __init__(self):
        super().__init__()
        self.name = "Elite Skirmishers"
        self.attack = 150
        self.defense = 150

class ExpertSkirmishers(Skirmishers):
    def __init__(self):
        super().__init__()
        self.name = "Expert Skirmishers"
        self.attack = 190
        self.defense = 190

class Crossbowmen(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 200,
            defense = 175,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.ranged
        )

class Arbalests(Crossbowmen):
    def __init__(self):
        super().__init__()
        self.name = "Arbalests"
        self.attack = 250
        self.defense = 225

class HandCanon(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Hand Cannoneers",
            attack = 300,
            defense = 225,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.ranged
        )

class Archers(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 150,
            defense = 100,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.ranged
        )

class EliteArchers(Archers):
    def __init__(self):
        super().__init__()
        self.name = "Elite Archers"
        self.attack = 200
        self.defense = 200

class ChuKoNu(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 150,
            defense = 150,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.ranged,
            abilities = ["rapid fire"]
        )

class HorseArchers(objects.Unit):
    def __init__(self):
        super().__init__(
            name="Horse Archers",
            attack = 150,
            defense = 150,
            range = 2,
            movement = 10,
            vision = 7,
            type = objects.UnitType.ranged
        )

class HeavyHorseArchers(HorseArchers):
    def __init__(self):
        super().__init__()
        self.name = "Heavy Horse Archers"
        self.attack = 200
        self.defense = 200

class Mangudai(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 150,
            defense = 150,
            range = 2,
            movement = 10,
            vision = 7,
            type = objects.UnitType.ranged,
            abilities = ["first strike"]
        )

class EliteMangudai(Mangudai):
    def __init__(self):
        super().__init__()
        self.name = "Elite Mangudai"
        self.attack = 200
        self.defense = 200

class Janissaries(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 250,
            defense = 175,
            range = 3,
            movement = 7,
            vision = 7,
            type = objects.UnitType.ranged
        )

class EliteJanissaries(Janissaries):
    def __init__(self):
        super().__init__()
        self.name = "Elite Janissaries"
        self.attack = 300
        self.defense = 225
