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


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.unit_list = ['Arbalests', 'Archers', 'Axemen', 'Berserkers', 'Bombards', 'Camels', 'Cavaliers', 'Champions', 'ChuKoNu', 'Crossbowmen', 'EliteArchers', 'EliteAxemen', 'EliteBerserkers', 'EliteJanissaries', 'EliteLongbowmen', 'EliteMameluks', 'EliteMangudai', 'EliteMonks', 'ElitePikemen', 'EliteRaiders', 'EliteSamurai', 'EliteSkirmishers', 'EliteTemplars', 'ExpertSkirmishers', 'HandCanon', 'HeavyCamels', 'HeavyHorseArchers', 'HeavyScorpions', 'HorseArchers', 'Janissaries', 'Knights', 'LightCav', 'Longbowmen', 'Longswordsmen', 'MaA', 'Mameluks', 'Mangudai', 'Milita', 'Monks', 'Onager', 'Paladins', 'Pikemen', 'Raiders', 'Rams', 'Samurai', 'Scorpions', 'ScoutCav', 'SiegeRams', 'Skirmishers', 'Spearmen', 'Templars', 'Trebuchets', 'TwoHanded', 'Villager', 'WarElephants']
        self.terrains_list = ['Bridge', 'Desert', 'DesertRoad', 'Ford', 'Forest', 'Hill', 'HillRoad', 'Mountain', 'MountainRoad', 'Plain', 'PlainRoad', 'Swamp']
        self.types = ['cavalry', 'infantry', 'ranged', 'siege', 'structure']
        self.ttypes = ['bridge', 'desert', 'ford', 'forest', 'hill', 'mountain', 'plain', 'structure', 'swamp']

        self.unit1 = units.Arbalests()
        self.unit2 = units.Arbalests()

        self.terrain1 = terrains.Bridge()
        self.terrain2 = terrains.Bridge()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        self.left = QFrame(self)
        self.left.setFrameShape(QFrame.StyledPanel)
 
        self.right = QFrame(self)
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

        self.unit1_construct()
        self.unit1_set()

        self.unit2_construct()
        self.unit2_set()

        self.terrain1_construct()
        self.terrain1_set()

        self.terrain2_construct()
        self.terrain2_set()


        self.fight_btn = QPushButton("Fight", self.bottom)
        self.fight_btn.resize(self.fight_btn.sizeHint())
        self.fight_btn.move(50, 50) 
        self.fight_btn.clicked.connect(self.initiate)

        QLabel("Distance", self.bottom).move(50, 150)
        self.slider = QSlider(Qt.Horizontal, parent=self.bottom)
        self.slider.resize(self.slider.sizeHint())
        lcd = QLCDNumber(self.bottom)
        self.slider.move(150, 150)
        lcd.move(250, 150)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        
        self.slider.valueChanged.connect(lcd.display)

        self.b = QPlainTextEdit(self.bottom)
        self.b.move(800, 50)
        self.b.resize(700, 500)
        sys.stdout = RedirectStream(self.b)


        self.setGeometry(300, 300, 900, 900)
        self.setWindowTitle('AoE: Age of Kings Battle Simulator')
        self.showMaximized()

        self.show()

    def unit1_construct(self):

        UnitComboBoxLeft = QComboBox(self.left)
        unit1 = QLabel("Unit", self.left)
        UnitComboBoxLeft.addItems(self.unit_list)

        UnitComboBoxLeft.activated[str].connect(self.unit1_selected)

        unit1.move(300, 35)
        UnitComboBoxLeft.move(385, 35)

        QLabel("Health", self.left).move(25, 100)
        self.health_left = QLineEdit(self.left)
        self.health_left.move(150, 100)
        self.health_left.textEdited.connect(lambda text : self.unit1.set("health", int(text)) if text.isdigit() else self.unit1.set("health", 100))

        QLabel("Attack", self.left).move(25, 150)
        self.attack_left = QLineEdit(self.left)
        self.attack_left.move(150, 150)
        self.attack_left.textEdited.connect(lambda text : self.unit1.set("attack", int(text)) if text.isdigit() else self.unit1.set("attack", 50))

        self.atk_upgrade_left = QCheckBox("Upgraded?", self.left)
        self.atk_upgrade_left.move(150, 185)
        self.atk_upgrade_left.stateChanged.connect(lambda state: self.unit1.set("atk_upgrade", state == Qt.Checked))

        QLabel("Defense", self.left).move(25, 250)
        self.defense_left = QLineEdit(self.left)
        self.defense_left.move(150, 250)
        self.defense_left.textEdited.connect(lambda text : self.unit1.set("defense", int(text)) if text.isdigit() else self.unit1.set("defense", 50))

        self.def_upgrade_left = QCheckBox("Upgraded?", self.left)
        self.def_upgrade_left.move(150, 285)
        self.def_upgrade_left.stateChanged.connect(lambda state: self.unit1.set("def_upgrade", state == Qt.Checked))

        QLabel("Range", self.left).move(25, 350)
        self.range_left = QLineEdit(self.left)
        self.range_left.move(150, 350)
        self.range_left.textEdited.connect(lambda text : self.unit1.set("range", int(text)) if text.isdigit() else self.unit1.set("range", 1))

        QLabel("Vision", self.left).move(450, 100)
        self.vision_left = QLineEdit(self.left)
        self.vision_left.move(575, 100)
        self.vision_left.textEdited.connect(lambda text : self.unit1.set("vision", int(text)) if text.isdigit() else self.unit1.set("vision", 7))

        QLabel("Movement", self.left).move(450, 150)
        self.movement_left = QLineEdit(self.left)
        self.movement_left.move(575, 150)
        self.movement_left.textEdited.connect(lambda text : self.unit1.set("movement", int(text)) if text.isdigit() else self.unit1.set("movement", 7))

        QLabel("Type", self.left).move(450, 200)
        self.type_left = QComboBox(self.left)
        self.type_left.addItems(self.types)
        self.type_left.move(575, 200)
        self.type_left.activated[str].connect(lambda text : self.unit1.set("type", objects.UnitType[text]))

        QLabel("Battles", self.left).move(450, 250)
        self.battles_left = QLineEdit(self.left)
        self.battles_left.move(575, 250)
        self.battles_left.textEdited.connect(lambda text : self.unit1.set("battles", int(text)) if text.isdigit() else self.unit1.set("battles", 0))

    def unit1_set(self):
        self.health_left.setText(str(self.unit1.health))
        self.attack_left.setText(str(self.unit1.attack))
        self.defense_left.setText(str(self.unit1.defense))
        self.range_left.setText(str(self.unit1.range))
        self.battles_left.setText(str(self.unit1.battles))
        self.vision_left.setText(str(self.unit1.vision))
        self.movement_left.setText(str(self.unit1.movement))
        self.type_left.setCurrentIndex(self.types.index(self.unit1.type.name))

    def terrain1_construct(self):
        TerrainComboBoxLeft = QComboBox(self.left)
        terrain1 = QLabel("Terrain", self.left)
        TerrainComboBoxLeft.addItems(self.terrains_list)
        
        TerrainComboBoxLeft.activated[str].connect(self.terrain1_selected)

        terrain1.move(300, 435)
        TerrainComboBoxLeft.move(400, 435)

        QLabel("Defense+", self.left).move(25, 500)
        self.tdefense_left = QLineEdit(self.left)
        self.tdefense_left.move(150, 500)
        self.tdefense_left.textEdited.connect(lambda text : self.terrain1.set("def_bonus", float(text)) if text.isdigit() else self.terrain1.set("def_bonus", 0))

        QLabel("Range+", self.left).move(25, 550)
        self.trange_left = QLineEdit(self.left)
        self.trange_left.move(150, 550)
        self.trange_left.textEdited.connect(lambda text : self.terrain1.set("rng_bonus", int(text)) if text.isdigit() else self.terrain1.set("rng_bonus", 0))

        QLabel("Vision+", self.left).move(25, 600)
        self.tvision_left = QLineEdit(self.left)
        self.tvision_left.move(150, 600)
        self.tvision_left.textEdited.connect(lambda text : self.terrain1.set("vis_bonus", int(text)) if text.isdigit() else self.terrain1.set("vis_bonus", 0))

        QLabel("Type", self.left).move(25, 650)
        self.ttype_left = QComboBox(self.left)
        self.ttype_left.addItems(self.ttypes)
        self.ttype_left.move(150, 650)
        self.ttype_left.activated[str].connect(lambda text : self.terrain1.set("type", objects.TerrainType[text]))

        QLabel("Movement", self.left).move(450, 500)
        self.tmovement_left = QLineEdit(self.left)
        self.tmovement_left.move(575, 500)
        self.tmovement_left.textEdited.connect(lambda text : self.terrain1.set("mov_cost", int(text)) if text.isdigit() else self.terrain1.set("mov_cost", 1))

        QLabel("Vision", self.left).move(450, 550)
        self.tvis_left = QLineEdit(self.left)
        self.tvis_left.move(575, 550)
        self.tvis_left.textEdited.connect(lambda text : self.terrain1.set("vis_cost", int(text)) if text.isdigit() else self.terrain1.set("vis_cost", 1))

        QLabel("Road?", self.left).move(450, 600)
        self.tsubtype_left = QCheckBox("", self.left)
        self.tsubtype_left.move(575, 600)
        self.tsubtype_left.stateChanged.connect(lambda state: self.terrain1.set("sub_type", objects.TerrainSubType.road) if state == Qt.Checked else self.terrain1.set("sub_type", objects.TerrainSubType.normal))

    def terrain1_set(self):
        self.tdefense_left.setText(str(self.terrain1.def_bonus * 100))
        self.trange_left.setText(str(self.terrain1.rng_bonus))
        self.tvision_left.setText(str(self.terrain1.vis_bonus))
        self.tmovement_left.setText(str(self.terrain1.mov_cost))
        self.tvis_left.setText(str(self.terrain1.vis_cost))
        self.ttype_left.setCurrentIndex(self.ttypes.index(self.terrain1.type.name))
        self.tsubtype_left.setChecked(self.terrain1.sub_type == objects.TerrainSubType.road)
        
    def unit1_selected(self, text):
        c = getattr(units, text)
        self.unit1 = c()
        self.unit1_set()

    def terrain1_selected(self, text):
        c = getattr(terrains, text)
        self.terrain1 = c()
        self.terrain1_set()

    def unit2_construct(self):
        UnitComboBoxRight = QComboBox(self.right)
        unit2 = QLabel("Defender ", self.right)
        UnitComboBoxRight.addItems(self.unit_list)

        UnitComboBoxRight.activated[str].connect(self.unit2_selected)

        unit2.move(300, 35)
        UnitComboBoxRight.move(400, 35)

        QLabel("Health", self.right).move(25, 100)
        self.health_right = QLineEdit(self.right)
        self.health_right.move(150, 100)
        self.health_right.textEdited.connect(lambda text : self.unit2.set("health", int(text)) if text.isdigit() else self.unit2.set("health", 100))

        QLabel("Attack", self.right).move(25, 150)
        self.attack_right = QLineEdit(self.right)
        self.attack_right.move(150, 150)
        self.attack_right.textEdited.connect(lambda text : self.unit2.set("attack", int(text)) if text.isdigit() else self.unit2.set("attack", 50))

        self.atk_upgrade_right = QCheckBox("Upgraded?", self.right)
        self.atk_upgrade_right.move(150, 185)
        self.atk_upgrade_right.stateChanged.connect(lambda state: self.unit2.set("atk_upgrade", state == Qt.Checked))

        QLabel("Defense", self.right).move(25, 250)
        self.defense_right = QLineEdit(self.right)
        self.defense_right.move(150, 250)
        self.defense_right.textEdited.connect(lambda text : self.unit2.set("defense", int(text)) if text.isdigit() else self.unit2.set("defense", 50))

        self.def_upgrade_right = QCheckBox("Upgraded?", self.right)
        self.def_upgrade_right.move(150, 285)
        self.def_upgrade_right.stateChanged.connect(lambda state: self.unit2.set("def_upgrade", state == Qt.Checked))

        QLabel("Range", self.right).move(25, 350)
        self.range_right = QLineEdit(self.right)
        self.range_right.move(150, 350)
        self.range_right.textEdited.connect(lambda text : self.unit2.set("range", int(text)) if text.isdigit() else self.unit2.set("range", 1))

        QLabel("Vision", self.right).move(450, 100)
        self.vision_right = QLineEdit(self.right)
        self.vision_right.move(575, 100)
        self.vision_right.textEdited.connect(lambda text : self.unit2.set("vision", int(text)) if text.isdigit() else self.unit2.set("vision", 7))

        QLabel("Movement", self.right).move(450, 150)
        self.movement_right = QLineEdit(self.right)
        self.movement_right.move(575, 150)
        self.movement_right.textEdited.connect(lambda text : self.unit2.set("movement", int(text)) if text.isdigit() else self.unit2.set("movement", 7))

        QLabel("Type", self.right).move(450, 200)
        self.type_right = QComboBox(self.right)
        self.type_right.addItems(self.types)
        self.type_right.move(575, 200)
        self.type_right.activated[str].connect(lambda text : self.unit2.set("type", objects.UnitType[text]))

        QLabel("Battles", self.right).move(450, 250)
        self.battles_right = QLineEdit(self.right)
        self.battles_right.move(575, 250)
        self.battles_right.textEdited.connect(lambda text : self.unit2.set("battles", int(text)) if text.isdigit() else self.unit2.set("battles", 0))
        
    def unit2_set(self):
        self.health_right.setText(str(self.unit2.health))
        self.attack_right.setText(str(self.unit2.attack))
        self.defense_right.setText(str(self.unit2.defense))
        self.range_right.setText(str(self.unit2.range))
        self.battles_right.setText(str(self.unit2.battles))
        self.vision_right.setText(str(self.unit2.vision))
        self.movement_right.setText(str(self.unit2.movement))
        self.type_right.setCurrentIndex(self.types.index(self.unit2.type.name))

    def terrain2_construct(self):
        TerrainComboBoxright = QComboBox(self.right)
        terrain2 = QLabel("Terrain", self.right)
        TerrainComboBoxright.addItems(self.terrains_list)
        
        TerrainComboBoxright.activated[str].connect(self.terrain2_selected)

        terrain2.move(300, 435)
        TerrainComboBoxright.move(400, 435)

        QLabel("Defense+", self.right).move(25, 500)
        self.tdefense_right = QLineEdit(self.right)
        self.tdefense_right.move(150, 500)
        self.tdefense_right.textEdited.connect(lambda text : self.terrain2.set("def_bonus", float(text)) if text.isdigit() else self.terrain2.set("def_bonus", 0))

        QLabel("Range+", self.right).move(25, 550)
        self.trange_right = QLineEdit(self.right)
        self.trange_right.move(150, 550)
        self.trange_right.textEdited.connect(lambda text : self.terrain2.set("rng_bonus", int(text)) if text.isdigit() else self.terrain2.set("rng_bonus", 0))

        QLabel("Vision+", self.right).move(25, 600)
        self.tvision_right = QLineEdit(self.right)
        self.tvision_right.move(150, 600)
        self.tvision_right.textEdited.connect(lambda text : self.terrain2.set("vis_bonus", int(text)) if text.isdigit() else self.terrain2.set("vis_bonus", 0))

        QLabel("Type", self.right).move(25, 650)
        self.ttype_right = QComboBox(self.right)
        self.ttype_right.addItems(self.ttypes)
        self.ttype_right.move(150, 650)
        self.ttype_right.activated[str].connect(lambda text : self.terrain2.set("type", objects.TerrainType[text]))

        QLabel("Movement", self.right).move(450, 500)
        self.tmovement_right = QLineEdit(self.right)
        self.tmovement_right.move(575, 500)
        self.tmovement_right.textEdited.connect(lambda text : self.terrain2.set("mov_cost", int(text)) if text.isdigit() else self.terrain2.set("mov_cost", 1))

        QLabel("Vision", self.right).move(450, 550)
        self.tvis_right = QLineEdit(self.right)
        self.tvis_right.move(575, 550)
        self.tvis_right.textEdited.connect(lambda text : self.terrain2.set("vis_cost", int(text)) if text.isdigit() else self.terrain2.set("vis_cost", 1))

        QLabel("Road?", self.right).move(450, 600)
        self.tsubtype_right = QCheckBox("", self.right)
        self.tsubtype_right.move(575, 600)
        self.tsubtype_right.stateChanged.connect(lambda state: self.terrain2.set("sub_type", objects.TerrainSubType.road) if state == Qt.Checked else self.terrain2.set("sub_type", objects.TerrainSubType.normal))

    def terrain2_set(self):
        self.tdefense_right.setText(str(self.terrain2.def_bonus * 100))
        self.trange_right.setText(str(self.terrain2.rng_bonus))
        self.tvision_right.setText(str(self.terrain2.vis_bonus))
        self.tmovement_right.setText(str(self.terrain2.mov_cost))
        self.tvis_right.setText(str(self.terrain2.vis_cost))
        self.ttype_right.setCurrentIndex(self.ttypes.index(self.terrain2.type.name))
        self.tsubtype_right.setChecked(self.terrain2.sub_type == objects.TerrainSubType.road)

    def unit2_selected(self, text):
        c = getattr(units, text)
        self.unit2 = c()
        self.unit2_set()

    def terrain2_selected(self, text):
        c = getattr(terrains, text)
        self.terrain2 = c()
        self.terrain2_set()

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
            ctx.status = 1
            ctx.defender.fight(ctx, ctx.attacker)
            ctx.status = 0
            ctx.attacker.fight(ctx, ctx.defender)
        else:
            ctx.attacker.fight(ctx, ctx.defender)
            ctx.status = 1
            ctx.defender.fight(ctx, ctx.attacker)

            if "rapid fire" in ctx.attacker.abilities:
                ctx.attacker.fight(ctx, ctx.defender)

    def initiate(self):
        print("initating....")
        ctx = objects.Context(
                attacker=self.unit1,
                defender=self.unit2,
                atk_terrain=self.terrain1,
                def_terrain=self.terrain2,
                distance=1
            )
        print("battle...")
        self.battle(ctx)

        print("stats..")
        self.unit1 = ctx.attacker
        self.unit2 = ctx.defender
        print(self.unit1)
        print("...")
        print(self.unit2)

        print("setting...")
        self.unit1_set()
        self.unit2_set()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())