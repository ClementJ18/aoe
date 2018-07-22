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

class MaA(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Men at Arms",
            attack = 150,
            defense = 150,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry
        )

class Longswordsmen(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 200,
            defense = 200,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry
        )

class TwoHanded(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Two Handed Swordsmen",
            attack = 250,
            defense = 250,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry
        )

class Champions(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 300,
            defense = 300,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry
        )

class Berserkers(objects.Unit):
    def __init__(self):
        super().__init__(
            name="Viking Berserkers",
            attack = 200,
            defense = 200,
            range = 1,
            movement = 7,
            vision = 9,
            type = objects.UnitType.infantry
        )

    #berserker ability
    def percent(self):
        return 1

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
            type = objects.UnitType.infantry
        )

    #veteran ability
    def ribbons(self):
        return ((self.battles // 2) * 0.15) if self.battles < 6 else 0.45

class EliteSamurai(Samurai):
    def __init__(self):
        super().__init__()
        self.name = "Elite Samurai"
        self.attack = 300
        self.defense = 300

class Pikemen(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 150,
            defense = 200,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.infantry,
            abilities = ["anti-cavalry"]
        )

    def offensive_abilities(self, ctx, other):
        return 0.83 if other.type == objects.UnitType.cavalry else 0

    def defensive_abilities(self, ctx, other):
        return 0.83 if other.type == objects.UnitType.cavalry else 0

class ElitePikemen(Pikemen):
    def __init__(self):
        super().__init__()
        self.name = "Elite Pikemen"
        self.attack = 200
        self.defense = 250

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

    def offensive_abilities(self, ctx, other):
        return 0.83 if other.type == objects.UnitType.cavalry else 0

    def defensive_abilities(self, ctx, other):
        return 0.83 if other.type == objects.UnitType.cavalry else 0

class Axemen(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Throwing Axemen",
            attack = 225,
            defense = 250,
            range = 1,
            movement = 7,
            vision = 9,
            type = objects.UnitType.infantry
        )

    def offensive_abilities(self, ctx, other):
        return 0.33 if ctx.def_terrain.type == objects.TerrainType.forest else 0

    def defensive_abilities(self, ctx, other):
        return 0.33 if ctx.atk_terrain.type == objects.TerrainType.forest else 0

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
