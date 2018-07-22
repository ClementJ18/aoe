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
            type = objects.UnitType.cavalry
        )

    def offensive_abilities(self, ctx, other):
        self.health += 20
        return 0.33 if ctx.def_terrain.type == objects.TerrainType.plain and ctx.status == 0 else 0

class EliteTemplars(Templars):
    def __init__(self):
        super().__init__()
        self.name = "Elite Templar Knights"
        self.attack = 250
        self.defense = 250

class Knights(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 200,
            defense = 200,
            range = 1,
            movement = 10,
            vision = 7,
            type = objects.UnitType.cavalry
        )

    def offensive_abilities(self, ctx, other):
        return 0.33 if ctx.def_terrain.type == objects.TerrainType.plain and ctx.status == 0 else 0

class Cavaliers(Knights):
    def __init__(self):
        super().__init__()
        self.name = "Cavaliers"
        self.attack = 250
        self.defense = 250

class Paladins(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 300,
            defense = 300,
            range = 1,
            movement = 10,
            vision = 7,
            type = objects.UnitType.cavalry
        )

    def offensive_abilities(self, ctx, other):
        return 0.33 if ctx.def_terrain.type == objects.TerrainType.plain and ctx.status == 0 else 0

class Camels(objects.Unit):
    def __init__(self):
        super().__init__(
            attack = 200,
            defense = 200,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.cavalry
        )

    def offensive_abilities(self, ctx, other):
        base = 0
        if ctx.def_terrain.type == objects.TerrainType.desert and ctx.status == 0:
            base += 0.33

        if other.type == objects.UnitType.cavalry:
            base += 0.33

        return base

    def defensive_abilities(self, ctx, other):
        return 0.33 if other.type == objects.UnitType.cavalry else 0

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
            type = objects.UnitType.cavalry
        )

    def offensive_abilities(self, ctx, other):
        base = 0
        if ctx.def_terrain.type == objects.TerrainType.desert and ctx.status == 0:
            base += 0.33

        if other.type == objects.UnitType.cavalry:
            base += 0.33

        return base

    def defensive_abilities(self, ctx, other):
        return 0.33 if other.type == objects.UnitType.cavalry else 0

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

class LightCav(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Light Cavalry",
            attack = 150,
            defense = 150,
            range = 1,
            movement = 10,
            vision = 7,
            type = objects.UnitType.cavalry
        )

    def offensive_abilities(self, ctx, other):
        return 0.33 if ctx.def_terrain.type == objects.TerrainType.plain and ctx.status == 0 else 0


class WarElephants(objects.Unit):
    def __init__(self):
        super().__init__(
            name = "Persian War Elephant",
            attack = 200,
            defense = 250,
            range = 1,
            movement = 7,
            vision = 7,
            type = objects.UnitType.cavalry
        )