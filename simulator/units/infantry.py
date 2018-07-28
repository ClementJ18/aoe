import objects

class Villager(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 50,
            defense = 50,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry
        )

class Milita(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 100,
            defense = 100,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry
        )

class MaA(Milita):
    def __init__(self):
        super().__init__()
        self.name = "Men at Arms"
        self.attack = 150
        self.defense = 150

class Longswordsmen(MaA):
    def __init__(self):
        super().__init__()
        self.name = "Longswordsmen"
        self.attack = 200
        self.defense = 200

class TwoHanded(Longswordsmen):
    def __init__(self):
        super().__init__()
        self.name = "Two Handed Swordsmen"
        self.attack = 250
        self.defense = 250

class Champions(TwoHanded):
    def __init__(self):
        super().__init__()
        self.name = "Champions"
        self.attack = 300
        self.defense = 300

class Berserkers(objects.Unit):
    def __init__(self):
        super().__init__(
            name="Viking Berserkers",
            attack = 200,
            defense = 200,
            range = 1,
            movement = 7,
            vision = 9,
            type = objects.UnitType.infantry,
            abilities = ["berserker"]
        )

class EliteBerserkers(Berserkers):
    def __init__(self):
        super().__init__()
        self.name = "Elite Berserkers"
        self.attack = 250
        self.defense = 250

class Raiders(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Celtic Woad Raiders",
            attack = 200,
            defense = 200,
            range = 1,
            movement = 9,
            vision = 9,
            type = objects.UnitType.infantry,
            abilities = ["cause fear"]
        )

class EliteRaiders(Raiders):
    def __init__(self):
        super().__init__()
        self.name = "Elite Woad Raiders"
        self.attack = 250
        self.defense = 250

class Samurai(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 250,
            defense = 250,
            range = 1,
            movement = 9,
            vision = 9,
            type = objects.UnitType.infantry,
            abilities = ["veteran"]
        )

class EliteSamurai(Samurai):
    def __init__(self):
        super().__init__()
        self.name = "Elite Samurai"
        self.attack = 300
        self.defense = 300

class Spearmen(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 100,
            defense = 100,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry,
            abilities = ["anti-cavalry"]
        )

class Pikemen(Spearmen):
    def __init__(self):
        super().__init__()
        self.name = "Pikemen"
        self.attack = 150
        self.defense = 200

class ElitePikemen(Pikemen):
    def __init__(self):
        super().__init__()
        self.name = "Elite Pikemen"
        self.attack = 200
        self.defense = 250

class Axemen(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Throwing Axemen",
            attack = 225,
            defense = 250,
            range = 1,
            movement = 7,
            vision = 9,
            type = objects.UnitType.infantry,
            abilities = ["woodsmen"]
        )

class EliteAxemen(Axemen):
    def __init__(self):
        super().__init__()
        self.name = "Elite Throwing Axemen"
        self.attack = 275
        self.defense = 300

class Monks(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 50,
            defense = 150,
            range = 1,
            movement = 9,
            vision = 9,
            type = objects.UnitType.infantry
        )

class EliteMonks(Monks):
    def __init__(self):
        super().__init__()
        self.name = "Elite Monks"
        self.attack = 50
        self.defense = 200
