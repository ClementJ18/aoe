import enum
import abilities
from simpleeval import simple_eval
import sys

class Unit:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        self.health = kwargs.get("health", 100)
        self.movement = kwargs.get("movement")
        self.attack = kwargs.get("attack")
        self.defense = kwargs.get("defense")
        self.vision = kwargs.get("vision")
        self.type = kwargs.get("type")
        self.range = kwargs.get("range")
        self.battles = kwargs.get("battles", 0)
        self.abilities = kwargs.get("abilities", [])
        self.def_upgrade = kwargs.get("def_upgrade", False)
        self.atk_upgrade = kwargs.get("atk_upgrade", False)

    def __str__(self):
        return f"<{self.name} health={self.health} battles={self.battles}>"

    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.__dict__ == other.__dict__

        return False

    def set(self, attr, value):
        self.__setattr__(attr, value)

    def percent(self):
        if "berserker" in self.abilities:
            return 1

        return self.health / 100 if self.health <= 100 else 1

    def ribbons(self):
        if "veteran" in self.abilities:
            return ((self.battles // 2) * 0.15) if self.battles < 6 else 0.45

        return ((self.battles // 3) * 0.15) if self.battles < 9 else 0.45

    @property   
    def armor_upgrade(self):
        return 0.25 if self.def_upgrade else 0

    @property
    def weapon_upgrade(self):
        return 0.25 if self.atk_upgrade else 0

    def process_abilities(self, ctx, other):
        self.env = {
            "enemy": other,
            "ctx": ctx,
            "self": self,
            "objects": sys.modules["objects"],
            "attack": ctx.status == 0,
            "counterattack": ctx.status == 1,
            "is_defender": ctx.defender == self,
            "is_attacker": ctx.attacker == self,
            "attacker_terrain": ctx.atk_terrain,
            "defender_terrain": ctx.def_terrain,
            "self_terrain": ctx.atk_terrain if ctx.attacker == self else ctx.def_terrain,
            "enemy_terrain": ctx.atk_terrain if ctx.attacker == other else ctx.def_terrain,
            "attacking": (ctx.attacker == self and ctx.status == 0) or (ctx.defender == self and ctx.status == 1),
            "defending": (ctx.attacker == self and ctx.status == 1) or (ctx.defender == self and ctx.status == 0),
            "infantry": UnitType.infantry,  
            "ranged": UnitType.ranged,    
            "cavalry": UnitType.cavalry,   
            "siege": UnitType.siege,     
            "structure": UnitType.structure,
            "plain": TerrainType.plain,
            "desert": TerrainType.desert,
            "hill": TerrainType.hill,
            "mountain": TerrainType.mountain,
            "forest": TerrainType.forest,
            "swamp": TerrainType.swamp,
            "bridge": TerrainType.bridge,
            "ford": TerrainType.ford,
            "road": TerrainSubType.road,
            "normal": TerrainSubType.normal
        }

        abilities_modif = 0
        for ability in self.abilities:
            try:
                abilities_modif += abilities.ability_dict[ability](self, ctx, other)
            except KeyError:
                abilities_modif += simple_eval(ctx.custom_abilities[ability], names=self.env)
            except TypeError:
                pass

        return abilities_modif

    def fight(self, ctx, other):
        if self.health <= 0:
            return

        if "no counter" in self.abilities and ctx.status == 1:
            return

        if "only buildings" in self.abilities and other.type != UnitType.structure:
            return

        if "only units" in self.abilities and other.type == UnitType.structure:
            return

        if ctx.status == 0:
            terrain_bonus = ctx.def_terrain.def_bonus
        elif ctx.distance > 1 and ctx.status == 1:
            terrain_bonus = ctx.atk_terrain.def_bonus
        else:
            terrain_bonus = 0

        atk_modif = 1 + bonus_dict[self.type][other.type] + self.ribbons() + self.process_abilities(ctx, other) + self.weapon_upgrade
        attack_nopercent = self.attack * atk_modif
        attack = attack_nopercent * self.percent()

        def_modif = 1 + bonus_dict[other.type][self.type] + other.ribbons() + other.process_abilities(ctx, self) + other.armor_upgrade + terrain_bonus
        defense_nopercent = other.defense * def_modif
        defense = defense_nopercent * other.percent()

        if "cause fear" in self.abilities:
            defense -= other.defense * 0.25

        if "cause fear" in other.abilities:
            attack -= self.attack * 0.25

        lost_h = round((attack / (defense * 2)) * 100)

        print(f"real attack of {self.name}: {attack} - modifier: {atk_modif} - net atk: {round(attack_nopercent)}")
        if ctx.debug:
            print(f"net atk: {self.attack * atk_modif} \n{bonus_dict[self.type][other.type]} + {self.ribbons()} + {self.process_abilities(ctx, other)} + {self.weapon_upgrade}")

        print(f"real defense of {other.name}: {defense} - modifier: {def_modif} - net def {round(defense_nopercent)}")
        if ctx.debug:
            print(f"net defense {other.defense * def_modif} \n{bonus_dict[other.type][self.type]} + {other.ribbons()} + {other.process_abilities(ctx, self)} + {other.armor_upgrade} + {terrain_bonus}")

        print(f"health lost {lost_h}")
        print("")

        if lost_h > other.health:
            lost_h = other.health

        other.health -= lost_h

class Terrain:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        self.mov_cost = kwargs.get("mov_cost")
        self.vis_cost = kwargs.get("vis_cost")
        self.def_bonus = kwargs.get("def_bonus", 0)
        self.rng_bonus = kwargs.get("rng_bonus", 0)
        self.vis_bonus = kwargs.get("vis_bonus", 0)
        self.type = kwargs.get("type")
        self.sub_type = kwargs.get("sub_type", TerrainSubType.normal)
        self.structure = kwargs.get("structure", False)

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
    hill      = 2
    mountain  = 3
    forest    = 4
    swamp     = 5
    bridge    = 6
    ford      = 7

class TerrainSubType(enum.Enum):
    normal = 0
    road   = 1

class Context:
    def __init__(self, **kwargs):
        self.attacker = kwargs.get("attacker")
        self.defender = kwargs.get("defender")
        self.atk_terrain = kwargs.get("atk_terrain")
        self.def_terrain = kwargs.get("def_terrain")
        self.status = 0 #0 attack 1 counter attack
        self.distance = kwargs.get("distance")
        self.debug = kwargs.get("debug")
        self.custom_abilities = kwargs.get("custom_abilities")


bonus_dict = {
    UnitType.infantry:  {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0.33, UnitType.structure: 0.33}, 
    UnitType.ranged:    {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.cavalry:   {UnitType.infantry: 0.33, UnitType.ranged: 0.33, UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.siege:     {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure: -0.5},
    UnitType.structure: {UnitType.infantry: 0,    UnitType.ranged: 0,    UnitType.cavalry: 0, UnitType.siege: 0,    UnitType.structure:0}
}
