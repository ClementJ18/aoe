import objects

class System:
    def __init__(self):
        self.priority = ("skirmish", "first strike")
        self.unit_list = ['Arbalests', 'Archers', 'Axemen', 'Berserkers', 'Bombards', 'Camels', 'Cavaliers', 'Champions', 'ChuKoNu', 'Crossbowmen', 'EliteArchers', 'EliteAxemen', 'EliteBerserkers', 'EliteJanissaries', 'EliteLongbowmen', 'EliteMameluks', 'EliteMangudai', 'EliteMonks', 'ElitePikemen', 'EliteRaiders', 'EliteSamurai', 'EliteSkirmishers', 'EliteTemplars', 'ExpertSkirmishers', 'HandCanon', 'HeavyCamels', 'HeavyHorseArchers', 'HeavyScorpions', 'HorseArchers', 'Janissaries', 'Knights', 'LightCav', 'Longbowmen', 'Longswordsmen', 'MaA', 'Mameluks', 'Mangudai', 'Milita', 'Monks', 'Onager', 'Paladins', 'Pikemen', 'Raiders', 'Rams', 'Samurai', 'Scorpions', 'ScoutCav', 'SiegeRams', 'Skirmishers', 'Spearmen', 'Templars', 'Trebuchets', 'TwoHanded', 'Villager', 'WarElephants']
        self.terrains_list = ['Bridge', 'Desert', 'DesertRoad', 'Ford', 'Forest', 'Hill', 'HillRoad', 'Mountain', 'MountainRoad', 'Plain', 'PlainRoad', 'Swamp']

    def battle(self, ctx):
        ctx.attacker.battles += 1
        ctx.defender.battles += 1

        if "first strike" in ctx.defender.abilities or ("skirmish" in ctx.defender.abilities and ctx.distance == 1) or ("anti-cavalry" in ctx.defender.abilities and ctx.attacker.type == UnitType.cavalry):
            ctx.defender.fight(ctx, ctx.attacker)
            ctx.status = 1
            ctx.attacker.fight(ctx, ctx.defender)
        else:
            ctx.attacker.fight(ctx, ctx.defender)
            ctx.status = 1
            ctx.defender.fight(ctx, ctx.attacker)

            if "rapid fire" in ctx.attacker.abilities:
                ctx.attacker.fight(ctx, ctx.defender)

            

    def initiate(self, **kwargs):
        ctx = objects.Context(kwargs)
        battle(ctx)

