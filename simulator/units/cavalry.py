import objects

class Templars(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Templar Knights",
            attack = 200,
            defense = 200,
            range = 1,
            movement = 10,
            vision = 7,
            type = objects.UnitType.cavalry,
            abilities = ["zeal", "plain charge"]
        )

class EliteTemplars(Templars):
    def __init__(self):
        super().__init__()
        self.name = "Elite Templar Knights"
        self.attack = 250
        self.defense = 250

class LightCav(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Light Cavalry",
            attack = 150,
            defense = 150,
            range = 1,
            movement = 10,
            vision = 7,
            type = objects.UnitType.cavalry,
            abilities = ["plain charge"]
        )

class Knights(LightCav):
    def __init__(self):
        super().__init__()
        self.name = "Knights"
        self.attack = 200
        self.defense = 200

class Cavaliers(Knights):
    def __init__(self):
        super().__init__()
        self.name = "Cavaliers"
        self.attack = 250
        self.defense = 250

class Paladins(Cavaliers):
    def __init__(self):
        super().__init__()
        self.name = "Paladins"
        self.attack = 300
        self.defense = 300

class Camels(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 200,
            defense = 200,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.cavalry,
            abilities = ["scared horses", "desert charge"]
        )

class HeavyCamels(Camels):
    def __init__(self):
        super().__init__()
        self.name = "Heavy Camels"
        self.attack = 250
        self.defense = 250


class Mameluks(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 250,
            defense = 200,
            range = 1,
            movement = 10,
            vision = 7,
            type = objects.UnitType.cavalry,
            abilities = ["scared horses", "desert charge"]
        )

class EliteMameluks(Mameluks):
    def __init__(self):
        super().__init__()
        self.name = "Elite Mameluks"
        self.attack = 300
        self.defense = 300

class ScoutCav(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Scout Cavalry",
            attack = 100,
            defense = 100,
            range = 1,
            movement = 10,
            vision = 10,
            type = objects.UnitType.cavalry
        )


class WarElephants(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Persian War Elephant",
            attack = 200,
            defense = 250,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.cavalry,
            abilities = ["cause fear"]
        )