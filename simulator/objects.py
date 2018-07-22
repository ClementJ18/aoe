import enum

class Unit:
    def __init__(self, **kwargs):
        self.name = kwargs["name"] if "name" in kwargs else self.__class__.__name__
        self.health = kwargs["health"] if "health" in kwargs else 100
        self.movement = kwargs["movement"]
        self.attack = kwargs["attack"]
        self.defense = kwargs["defense"]
        self.vision = kwargs["vision"]
        self.type = kwargs["type"]
        self.range = kwargs["range"]
        self.battles = kwargs["battles"] if "battles" in kwargs else 0
        self.abilities = kwargs["abilities"] if "abilities" in kwargs else []
        self.def_upgrade = kwargs["def_upgrade"] if "def_upgrade" in kwargs else False
        self.atk_upgrade = kwargs["atk_upgrade"] if "atk_upgrade" in kwargs else False

    def __str__(self):
        return f"<{self.name} health={self.health} battles={self.battles}>"

    def set(self, attr, value):
        self.__setattr__(attr, value)

    def percent(self):
        return self.health / 100 if self.health <= 100 else 1

    def ribbons(self):
        return ((self.battles // 3) * 0.15) if self.battles < 9 else 0.45

    def offensive_abilities(self, ctx, other):
        return 0

    def defensive_abilities(self, ctx, other):
        return 0

    def armor_upgrade(self):
        return 0.25 if self.def_upgrade else 0

    def weapon_upgrade(self):
        return 0.25 if self.atk_upgrade else 0

    def fight(self, ctx, other):
        if self.health <= 0:
            return

        if (ctx.distance == 1 and ctx.status == 0) or (ctx.distance > 1 and ctx.status == 0):
            terrain_bonus = ctx.def_terrain.def_bonus
        elif ctx.distance > 1 and ctx.status == 1:
            terrain_bonus = ctx.atk_terrain.def_bonus
        else:
            terrain_bonus = 0

        attack = self.attack * (1 + bonus_dict[self.type][other.type] + self.ribbons() + self.offensive_abilities(ctx, other) + self.weapon_upgrade())
        attack = attack * self.percent()

        defense = other.defense * (1 + bonus_dict[other.type][self.type] + other.ribbons() + other.defensive_abilities(ctx, self) + other.armor_upgrade() + terrain_bonus)
        defense = defense * other.percent()

        if "cause fear" in self.abilities:
            defense -= other.defense * 0.25

        if "cause fear" in other.abilities:
            attack -= self.attack * 0.25

        print(f"attack of {self.name}: {attack}")
        print(f"defense of {other.name}: {defense}")
        print(f"health lost {(attack / (defense * 2)) * 100}")

        lost_h = round((attack / (defense * 2)) * 100)

        if lost_h > other.health:
            lost_h = other.health

        other.health -= lost_h

        if self.health > 100:
            self.health = 100

        if other.health > 100:
            other.health = 100

class Terrain:
    def __init__(self, **kwargs):
        self.mov_cost = kwargs["movement_cost"]
        self.vis_cost = kwargs["vision_cost"]
        self.def_bonus = kwargs["defense_bonus"] if "defense_bonus" in kwargs else 0
        self.rng_bonus = kwargs["range_bonus"] if "range_bonus" in kwargs else 0
        self.vis_bonus = kwargs["vision_bonus"] if "vision_bonus" in kwargs else 0
        self.type = kwargs["type"]
        self.sub_type = kwargs["sub_type"] if "sub_type" in kwargs else TerrainSubType.normal
        self.structure = kwargs["structure"] if "structure" in kwargs else False

    def __str__(self):
        return f"{self.type}({self.sub_type})"

    def set(self, attr, value):
        self.__setattr__(attr, value)

class UnitType(enum.Enum):
    infantry  = 0
    ranged    = 1
    cavalry   = 2
    siege     = 3
    structure = 4

class TerrainType(enum.Enum):
    plain     = 0
    desert    = 1
    structure = 2
    hill      = 3
    mountain  = 4
    forest    = 5
    swamp     = 6
    bridge    = 7
    ford      = 8

class TerrainSubType(enum.Enum):
    normal = 0
    road   = 1

class Context:
    def __init__(self, **kwargs):
        self.attacker = kwargs["attacker"]
        self.defender = kwargs["defender"]
        self.atk_terrain = kwargs["atk_terrain"]
        self.def_terrain = kwargs["def_terrain"]
        self.status = 0 #0 attack 1 counter attack
        self.distance = kwargs["distance"]

bonus_dict = {
    UnitType.infantry:  {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0.33, UnitType.structure: 0.33}, 
    UnitType.ranged:    {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.cavalry:   {UnitType.infantry: 0.33, UnitType.ranged: 0.33, UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.siege:     {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.structure: {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure:0}
}
