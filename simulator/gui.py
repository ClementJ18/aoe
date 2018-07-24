from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, 
    QSplitter, QStyleFactory, QApplication, QMessageBox, QLabel, 
    QComboBox, QLineEdit, QPushButton, QCheckBox, QSlider, QLCDNumber,
    QPlainTextEdit)
from PyQt5.QtCore import Qt
import sys
import _io

import units
import terrains
import objects

class RedirectStream(_io.TextIOWrapper):
    def __init__(self, box):
        self.box = box

    def write(self, text):
        self.box.insertPlainText(text)

class SideFrame(QFrame):
    def __init__(self, parent, **args):
        super().__init__(parent)

        self.unit = units.Arbalests()
        self.terrain = terrains.Bridge()
        self.parent = parent
        self.name = args["name"]

        self.unit_construct()
        self.unit_set()

        self.terrain_construct()
        self.terrain_set()

    def unit_construct(self):

        self.UnitComboBox = QComboBox(self)
        unit = QLabel(self.name, self)
        self.UnitComboBox.addItems(self.parent.unit_list)

        self.UnitComboBox.activated[str].connect(self.unit_selected)

        unit.move(300, 35)
        self.UnitComboBox.move(385, 35)

        QLabel("Health", self).move(25, 100)
        self.health = QLineEdit(self)
        self.health.move(150, 100)
        self.health.textEdited.connect(lambda text : self.unit.set("health", int(text)) if text.isdigit() else self.unit.set("health", 100))

        QLabel("Attack", self).move(25, 150)
        self.attack = QLineEdit(self)
        self.attack.move(150, 150)
        self.attack.textEdited.connect(lambda text : self.unit.set("attack", int(text)) if text.isdigit() else self.unit.set("attack", 50))

        self.atk_upgrade = QCheckBox("Upgraded?", self)
        self.atk_upgrade.move(150, 185)
        self.atk_upgrade.stateChanged.connect(lambda state: self.unit.set("atk_upgrade", state == Qt.Checked))

        QLabel("Defense", self).move(25, 250)
        self.defense = QLineEdit(self)
        self.defense.move(150, 250)
        self.defense.textEdited.connect(lambda text : self.unit.set("defense", int(text)) if text.isdigit() else self.unit.set("defense", 50))

        self.def_upgrade = QCheckBox("Upgraded?", self)
        self.def_upgrade.move(150, 285)
        self.def_upgrade.stateChanged.connect(lambda state: self.unit.set("def_upgrade", state == Qt.Checked))

        QLabel("Range", self).move(25, 350)
        self.range = QLineEdit(self)
        self.range.move(150, 350)
        self.range.textEdited.connect(lambda text : self.unit.set("range", int(text)) if text.isdigit() else self.unit.set("range", 1))

        QLabel("Vision", self).move(450, 100)
        self.vision = QLineEdit(self)
        self.vision.move(575, 100)
        self.vision.textEdited.connect(lambda text : self.unit.set("vision", int(text)) if text.isdigit() else self.unit.set("vision", 7))

        QLabel("Movement", self).move(450, 150)
        self.movement = QLineEdit(self)
        self.movement.move(575, 150)
        self.movement.textEdited.connect(lambda text : self.unit.set("movement", int(text)) if text.isdigit() else self.unit.set("movement", 7))

        QLabel("Type", self).move(450, 200)
        self.type = QComboBox(self)
        self.type.addItems(self.parent.types)
        self.type.move(575, 200)
        self.type.activated[str].connect(lambda text : self.unit.set("type", objects.UnitType[text]))

        QLabel("Battles", self).move(450, 250)
        self.battles = QLineEdit(self)
        self.battles.move(575, 250)
        self.battles.textEdited.connect(lambda text : self.unit.set("battles", int(text)) if text.isdigit() else self.unit.set("battles", 0))

    def unit_set(self):
        self.health.setText(str(self.unit.health))
        self.attack.setText(str(self.unit.attack))
        self.defense.setText(str(self.unit.defense))
        self.range.setText(str(self.unit.range))
        self.battles.setText(str(self.unit.battles))
        self.vision.setText(str(self.unit.vision))
        self.movement.setText(str(self.unit.movement))
        self.type.setCurrentIndex(self.parent.types.index(self.unit.type.name))
        self.atk_upgrade.setChecked(self.unit.atk_upgrade)
        self.def_upgrade.setChecked(self.unit.def_upgrade)

    def terrain_construct(self):
        self.TerrainComboBox = QComboBox(self)
        terrain = QLabel("Terrain", self)
        self.TerrainComboBox.addItems(self.parent.terrains_list)
        
        self.TerrainComboBox.activated[str].connect(self.terrain_selected)

        terrain.move(300, 435)
        self.TerrainComboBox.move(400, 435)

        QLabel("Defense+", self).move(25, 500)
        self.tdefense = QLineEdit(self)
        self.tdefense.move(150, 500)
        self.tdefense.textEdited.connect(lambda text : self.terrain.set("def_bonus", float(text)) if text.isdigit() else self.terrain.set("def_bonus", 0))

        QLabel("Range+", self).move(25, 550)
        self.trange = QLineEdit(self)
        self.trange.move(150, 550)
        self.trange.textEdited.connect(lambda text : self.terrain.set("rng_bonus", int(text)) if text.isdigit() else self.terrain.set("rng_bonus", 0))

        QLabel("Vision+", self).move(25, 600)
        self.tvision = QLineEdit(self)
        self.tvision.move(150, 600)
        self.tvision.textEdited.connect(lambda text : self.terrain.set("vis_bonus", int(text)) if text.isdigit() else self.terrain.set("vis_bonus", 0))

        QLabel("Type", self).move(25, 650)
        self.ttype = QComboBox(self)
        self.ttype.addItems(self.parent.ttypes)
        self.ttype.move(150, 650)
        self.ttype.activated[str].connect(lambda text : self.terrain.set("type", objects.TerrainType[text]))

        QLabel("Movement", self).move(450, 500)
        self.tmovement = QLineEdit(self)
        self.tmovement.move(575, 500)
        self.tmovement.textEdited.connect(lambda text : self.terrain.set("mov_cost", int(text)) if text.isdigit() else self.terrain.set("mov_cost", 1))

        QLabel("Vision", self).move(450, 550)
        self.tvis = QLineEdit(self)
        self.tvis.move(575, 550)
        self.tvis.textEdited.connect(lambda text : self.terrain.set("vis_cost", int(text)) if text.isdigit() else self.terrain.set("vis_cost", 1))

        QLabel("Road?", self).move(450, 600)
        self.tsubtype = QCheckBox("", self)
        self.tsubtype.move(575, 600)
        self.tsubtype.stateChanged.connect(lambda state: self.terrain.set("sub_type", objects.TerrainSubType.road) if state == Qt.Checked else self.terrain.set("sub_type", objects.TerrainSubType.normal))

    def terrain_set(self):
        self.tdefense.setText(str(self.terrain.def_bonus * 100))
        self.trange.setText(str(self.terrain.rng_bonus))
        self.tvision.setText(str(self.terrain.vis_bonus))
        self.tmovement.setText(str(self.terrain.mov_cost))
        self.tvis.setText(str(self.terrain.vis_cost))
        self.ttype.setCurrentIndex(self.parent.ttypes.index(self.terrain.type.name))
        self.tsubtype.setChecked(self.terrain.sub_type == objects.TerrainSubType.road)
        
    def unit_selected(self, text):
        c = getattr(units, text)
        self.unit = c()
        self.unit_set()

    def terrain_selected(self, text):
        c = getattr(terrains, text)
        self.terrain = c()
        self.terrain_set()



class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.unit_list = ['Arbalests', 'Archers', 'Axemen', 'Berserkers', 'Bombards', 'Camels', 'Cavaliers', 'Champions', 'ChuKoNu', 'Crossbowmen', 'EliteArchers', 'EliteAxemen', 'EliteBerserkers', 'EliteJanissaries', 'EliteLongbowmen', 'EliteMameluks', 'EliteMangudai', 'EliteMonks', 'ElitePikemen', 'EliteRaiders', 'EliteSamurai', 'EliteSkirmishers', 'EliteTemplars', 'ExpertSkirmishers', 'HandCanon', 'HeavyCamels', 'HeavyHorseArchers', 'HeavyScorpions', 'HorseArchers', 'Janissaries', 'Knights', 'LightCav', 'Longbowmen', 'Longswordsmen', 'MaA', 'Mameluks', 'Mangudai', 'Milita', 'Monks', 'Onager', 'Paladins', 'Pikemen', 'Raiders', 'Rams', 'Samurai', 'Scorpions', 'ScoutCav', 'SiegeRams', 'Skirmishers', 'Spearmen', 'Templars', 'Trebuchets', 'TwoHanded', 'Villager', 'WarElephants']
        self.terrains_list = ['Bridge', 'Desert', 'DesertRoad', 'Ford', 'Forest', 'Hill', 'HillRoad', 'Mountain', 'MountainRoad', 'Plain', 'PlainRoad', 'Swamp']
        self.types = ['cavalry', 'infantry', 'ranged', 'siege', 'structure']
        self.ttypes = ['bridge', 'desert', 'ford', 'forest', 'hill', 'mountain', 'plain', 'structure', 'swamp']

        self.distance = 1
        self.debug = False

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        self.left = SideFrame(self, name="Attacker")
        self.left.setFrameShape(QFrame.StyledPanel)
 
        self.right = SideFrame(self, name="Defender")
        self.right.setFrameShape(QFrame.StyledPanel)

        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.left)
        splitter1.addWidget(self.right)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.fight_btn = QPushButton("Fight", self.bottom)
        self.fight_btn.resize(self.fight_btn.sizeHint())
        self.fight_btn.move(50, 50) 
        self.fight_btn.clicked.connect(self.initiate)

        self.inv_btn = QPushButton("Inverse Units", self.bottom)
        self.inv_btn.resize(self.inv_btn.sizeHint())
        self.inv_btn.move(250, 50) 
        self.inv_btn.clicked.connect(self.inverse_units)

        self.inv2_btn = QPushButton("Inverse Terrains", self.bottom)
        self.inv2_btn.resize(self.inv2_btn.sizeHint())
        self.inv2_btn.move(450, 50) 
        self.inv2_btn.clicked.connect(self.inverse_terrain)

        QLabel("Distance", self.bottom).move(50, 150)
        self.dist_box = QComboBox(self.bottom)
        self.dist_box.addItems([str(x) for x in range(1, 7)])
        self.dist_box.activated[str].connect(lambda text: self.__setattr__("distance", int(text)))
        self.dist_box.move(150, 150)

        self.b = QPlainTextEdit(self.bottom)
        self.b.setReadOnly(True)
        self.b.move(800, 50)
        self.b.resize(700, 500)
        sys.stdout = RedirectStream(self.b)

        self.inv2_btn = QPushButton("Clear", self.bottom)
        self.inv2_btn.resize(self.inv2_btn.sizeHint())
        self.inv2_btn.move(1350, 560) 
        self.inv2_btn.clicked.connect(lambda : self.b.clear())

        self.debug_b = QCheckBox("Debug?", self.bottom)
        self.debug_b.move(650, 60)
        self.debug_b.stateChanged.connect(lambda state: self.__setattr__("debug", state == Qt.Checked))

        self.setGeometry(300, 300, 900, 900)
        self.setWindowTitle('AoE: Age of Kings Battle Simulator')
        self.showMaximized()

        self.show()

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def battle(self, ctx):
        ctx.attacker.battles += 1
        ctx.defender.battles += 1

        if "first strike" in ctx.defender.abilities or ("skirmish" in ctx.defender.abilities and ctx.distance == 1) or ("anti-cavalry" in ctx.defender.abilities and ctx.attacker.type == objects.UnitType.cavalry):
            if ctx.distance <= ctx.defender.range:
                ctx.status = 1
                ctx.defender.fight(ctx, ctx.attacker)

            ctx.status = 0
            ctx.attacker.fight(ctx, ctx.defender)
        else:
            ctx.attacker.fight(ctx, ctx.defender)
            if ctx.distance <= ctx.defender.range:
                ctx.status = 1
                ctx.defender.fight(ctx, ctx.attacker)

            if "rapid fire" in ctx.attacker.abilities:
                ctx.attacker.fight(ctx, ctx.defender)

    def initiate(self):
        if self.left.unit.health == 0 or self.right.unit.health == 0:
            print("!One of the units is dead!\n")
            return

        ctx = objects.Context(
                attacker = self.left.unit,
                defender = self.right.unit,
                atk_terrain = self.left.terrain,
                def_terrain = self.right.terrain,
                distance = self.distance,
                debug = self.debug
            )

        print("[battle]")
        self.battle(ctx)

        print("[Final Stats]")
        self.left.unit = ctx.attacker
        self.right.unit = ctx.defender
        print(ctx.attacker)
        print("...")
        print(ctx.defender)

        print("")
        self.left.unit_set()
        self.right.unit_set()

    def inverse_units(self):
        temp = self.left.unit
        temp2 = self.right.unit
        self.right.UnitComboBox.setCurrentIndex(self.unit_list.index(temp.__class__.__name__))
        self.left.UnitComboBox.setCurrentIndex(self.unit_list.index(temp2.__class__.__name__))

        self.left.unit = temp2
        self.right.unit = temp

        self.left.unit_set()
        self.right.unit_set()

    def inverse_terrain(self):
        temp = self.left.terrain
        temp2 = self.right.terrain

        self.right.TerrainComboBox.setCurrentIndex(self.terrains_list.index(temp.name))
        self.left.TerrainComboBox.setCurrentIndex(self.terrains_list.index(temp2.name))
        
        self.left.terrain = temp2
        self.right.terrain = temp

        self.left.terrain_set()
        self.right.terrain_set()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())