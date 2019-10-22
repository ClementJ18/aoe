from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, 
    QSplitter, QStyleFactory, QApplication, QMessageBox, QLabel, 
    QComboBox, QLineEdit, QPushButton, QCheckBox, QSlider, QLCDNumber,
    QPlainTextEdit, QMenuBar, QMainWindow)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import sys
import _io
import json
import traceback

import units
import terrains
import objects
import abilities

class RedirectStream(_io.TextIOWrapper):
    def __init__(self, box):
        self.box = box

    def write(self, text):
        self.box.insertPlainText(text)

class AbilityPicker(QMainWindow):
    def __init__(self, parent=None):
        super(AbilityPicker, self).__init__(parent)
        self.parent = parent
        self.gui = parent.parent
        self.widgets = []
        self.initUI()

    def initUI(self):
        horizontal = 50
        vertical = 50
        ability_list = [ability for ability in abilities.ability_dict] + [ability for ability in self.gui.custom_abilities]

        for ability in ability_list:
            check = QCheckBox(ability, self)
            check.move(horizontal, vertical)
            check.stateChanged.connect(lambda state: self.parent.unit.abilities.append(ability) if state == Qt.Checked else self.parent.unit.abilities.remove(ability))
            check.setChecked(ability in self.parent.unit.abilities)
            check.resize(check.sizeHint())
            self.widgets.append(check)

            if ability in self.gui.custom_abilities:
                del_button = QPushButton("X", self)
                del_button.move(horizontal + 200, vertical)
                del_button.resize(25, 25)
                del_button.clicked.connect(lambda: self.remove_ability(ability))
                self.widgets.append(del_button)

            if vertical == 500:
                vertical = 0
                horizontal += 250

            vertical += 50

        self.setWindowTitle("Ability Picker")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon("icon.png"))

    def remove_ability(self, ability):
        units = self.get_units_with_ability(ability)
        widget_i = self.widgets.index(next((x for x in self.widgets if x.text() == ability), 0))
        reset = self.widgets[widget_i:]

        if len(units) == 0:
            del self.gui.custom_abilities[ability]
        else:
            msg = f"The following units have that ability: {', '.join(units)}\n Do you still wish to continue? (Continuing will remove the ability from the units)"
            reply = QMessageBox.question(self, 'Critical',
            msg, QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                for unit in units:
                    if unit in self.gui.custom_units:
                        self.gui.custom_units[unit]["abilities"].remove(ability)
                    else:
                        self.parent.unit.abilities.remove(ability)

                del self.gui.custom_abilities[ability]
            else:
                return

        reset.pop(0).setParent(None)
        reset.pop(0).setParent(None)
        for widget in reset:
            if widget.y() == 50:
                widget.move(widget.x() - 250, 400)

            widget.move(widget.x(), widget.y() - 50)

    def get_units_with_ability(self, ability):
        units_list = []

        for unit in self.gui.unit_list:
            if unit in self.gui.custom_units:
                inst = self.gui.custom_units[unit]
                if ability in inst["abilities"]:
                    units_list.append(inst["name"])
            elif unit == self.parent.unit.__class__.__name__:
                if ability in self.parent.unit.abilities:
                    units_list.append(self.parent.unit.name)
            elif unit == self.parent.other.__class__.__name__:
                if ability in self.parent.other.unit.abilities:
                    units_list.append(self.parent.other .unit.name)

        return units_list

class AbilityCreator(QMainWindow):
    def __init__(self, parent=None):
        super(AbilityCreator, self).__init__(parent)
        self.parent = parent
        self.gui = parent.parent().parent()
        self.env = {
            "enemy": "Medium level keyword. This represents the enemy object, this is useful for advanced users that wish to user different attributes.",
            "ctx": "Low level keyword. This is the context object, it contains everything the code uses to process battles.",
            "self": "Medium level keyword. This is the unit object that the ability is attached to, same as with enemy",
            "objects": "Low level keyword. This represents the module itself and can be used to reach the base classes and compare certain attributes",
            "attack": "High level keyword. Can be used to check if the current phase of the battle is the inital attack",
            "counterattack": "High level keyword. Can be used to check if the current phase of the battle is the counter attack made by the defender",
            "attacking": "High level keyword. This can be used to check if the unit is currently attacking.",
            "defending": "High level keyword. This can be used to check if the unit is currently defending. ",
            "is_defender": "High level keyword. Can be used to check if the unit is the defending unit (unit on the right).",
            "is_attacker": "High level keyword. Can be used to check if the unit is the attacking unit (unit on the left).",
            "attacker_terrain": "Medium level keyword. Can be used to access attributes of the terrain the attacker is standing on.",
            "defender_terrain": "Medium level keyword. Can be used to access attributes of the terrain the defender is standing on.",
            "self_terrain": "Medium level keyword. This represents the terrain the unit for which abilities are currently being checked is standing on.",
            "enemy_terrain": "Medium level keyword. This represents the terrain the enemy of the unit for which abilities are currently being checked is standing on.",
            "infantry": "High level keyword. A unit type, can be compared to unit objects' type attribute, represents infantry units.",  
            "ranged": "High level keyword. A unit type, can be compared to unit objects' type attribute, represents ranged units.",    
            "cavalry": "High level keyword. A unit type, can be compared to unit objects' type attribute, represents cavalry units.",   
            "siege": "High level keyword. A unit type, can be compared to unit objects' type attribute, represents siege units.",     
            "structure": "High level keyword. A unit type, can be compared to unit objects' type attribute, represents structures.",
            "plain": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents plains",
            "desert": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents desert",
            "hill": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents hills",
            "mountain": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents mountains",
            "forest": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents forests",
            "swamp": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents swamps",
            "bridge": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents bridges",
            "ford": "High level keyword. A terrain type, can be compared to terrain objects' type attribute, represents fords",
            "road": "High level keyword. A terrain sub type, can be compared to terrain objects' sub_type attribute, represents roads",
            "normal": "High level keyword. A terrain sub type, can be compared to terrain objects' sub_type attribute, represents non-road terrain"
        }

        self.levels = "<b>High level</b>: keyword representing a single value <br><b>Medium level</b>: keyword representing objects which have high level attributes which can be access through dot notation (medium_level.high_level)<br><b>Low level</b>: keyword representing objects with high, medium and low level attributes which can be access through dot notation."
        self.initUI()

        self.box = QMessageBox()
        self.box.setIcon(QMessageBox.Information)
        self.box.setText("Reserved ability keywords are classified in three categories:")
        self.box.setInformativeText(self.levels)
        self.box.setWindowTitle("Keyword Levels")
        self.box.setWindowIcon(QIcon("icon.png"))
        self.box.setStandardButtons(QMessageBox.Ok)
        self.box.buttonClicked.connect(lambda: self.box.close())

    def initUI(self):
        QLabel("Name", self).move(50, 50)
        self.name = QLineEdit(self)
        self.name.move(150, 50)
        self.name.resize(200, 40)

        QLabel("Modifiers", self).move(50, 220)
        QLabel("If True", self).move(50, 250)
        self.modifier_true = QLineEdit(self)
        self.modifier_true.move(150, 250)
        self.modifier_true.setToolTip("This is the modifier that will be added to the rest of the modifiers if the condition is fulfilled")

        QLabel("If False", self).move(50, 280)
        self.modifier_false = QLineEdit(self)
        self.modifier_false.move(150, 280)
        self.modifier_false.setToolTip("This is the modifier that will be added to the rest of the modifiers if the condition fails")

        QLabel("Condition", self).move(50, 120)
        QLabel("if", self).move(50, 150)
        self.func = QLineEdit(self)
        self.func.move(75, 150)
        self.func.resize(600 , 30)

        self.abilities_btn = QPushButton("Add Ability", self)
        self.abilities_btn.resize(self.abilities_btn.sizeHint())
        self.abilities_btn.move(50, 400)
        self.abilities_btn.clicked.connect(self.add_ability)

        self.levels_btn = QPushButton("Levels?", self)
        self.levels_btn.resize(self.levels_btn.sizeHint())
        self.levels_btn.move(600, 210)
        self.levels_btn.clicked.connect(lambda: self.box.show())

        self.text_box = QPlainTextEdit(self)
        self.text_box.setReadOnly(True)
        self.text_box.move(350, 270)
        self.text_box.resize(400, 200)
        self.text_box.insertPlainText(f'{self.env["enemy"]}')

        def editor(text):
            self.text_box.clear()
            self.text_box.insertPlainText(f'{self.env[text]}')

        self.tooltip_box = QComboBox(self)
        self.tooltip_box.addItems(self.env.keys())
        self.tooltip_box.resize(self.tooltip_box.sizeHint())
        self.tooltip_box.move(350, 220)
        self.tooltip_box.activated[str].connect(editor)

        self.set_default()

        self.setWindowTitle("Ability Creator")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowModality(Qt.ApplicationModal)        


    def add_ability(self):
        self.parent.parent().parent().custom_abilities[self.name.text()] = f"{self.modifier_true.text()} if {self.func.text()} else {self.modifier_false.text()}"
        self.set_default()
        self.close() 

    def set_default(self):
        self.name.setText("Ability Name")
        self.modifier_true.setText("0")
        self.modifier_false.setText("0")
        self.func.setText("True")

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
        QLabel(self.name, self).move(300, 35)
        self.UnitComboBox.addItems(self.parent.unit_list)
        self.UnitComboBox.activated[str].connect(self.unit_selected)
        self.UnitComboBox.move(395, 35)

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

        QLabel("Name", self).move(850, 100)
        self.c_name = QLineEdit(self)
        self.c_name.move(975, 100)
        self.c_name.textEdited.connect(lambda text : self.unit.set("name", text) if text.isalpha() else self.unit.set("name", self.unit.name))

        self.c_save = QPushButton("Save Unit", self)
        self.c_save.resize(self.c_save.sizeHint())
        self.c_save.move(1250, 100) 
        self.c_save.clicked.connect(self.save_unit)

        self.unit_deleter = QPushButton("Delete Unit", self)
        self.unit_deleter.resize(self.unit_deleter.sizeHint())
        self.unit_deleter.move(1250, 150)
        self.unit_deleter.hide()
        self.unit_deleter.clicked.connect(self.remove_unit)

        self.abilities_btn = QPushButton("Ability Picker", self)
        self.abilities_btn.resize(self.abilities_btn.sizeHint())
        self.abilities_btn.move(1350, 350)
        self.abilities_btn.clicked.connect(self.init_picker)  

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
        self.c_name.setText(self.unit.name)
        if self.unit.name in self.parent.custom_units:
            self.unit_deleter.show()
        else:
            self.unit_deleter.hide()

    def init_picker(self):
        ability_picker = AbilityPicker(self)
        ability_picker.resize(800, 600)
        ability_picker.show()

    def terrain_construct(self):
        self.TerrainComboBox = QComboBox(self)
        QLabel("Terrain", self).move(300, 435)
        self.TerrainComboBox.addItems(self.parent.terrain_list)
        self.TerrainComboBox.activated[str].connect(self.terrain_selected)
        self.TerrainComboBox.move(400, 435)

        QLabel("Defense+", self).move(25, 500)
        self.tdefense = QLineEdit(self)
        self.tdefense.move(150, 500)
        self.tdefense.textEdited.connect(lambda text : self.terrain.set("def_bonus", float(text)/100) if text.isdigit() else self.terrain.set("def_bonus", self.terrain.def_bonus))

        QLabel("Range+", self).move(25, 550)
        self.trange = QLineEdit(self)
        self.trange.move(150, 550)
        self.trange.textEdited.connect(lambda text : self.terrain.set("rng_bonus", int(text)) if text.isdigit() else self.terrain.set("rng_bonus", self.terrain.rng_bonus))

        QLabel("Vision+", self).move(25, 600)
        self.tvision = QLineEdit(self)
        self.tvision.move(150, 600)
        self.tvision.textEdited.connect(lambda text : self.terrain.set("vis_bonus", int(text)) if text.isdigit() else self.terrain.set("vis_bonus", self.terrain.vis_bonus))

        QLabel("Type", self).move(25, 650)
        self.ttype = QComboBox(self)
        self.ttype.addItems(self.parent.ttypes)
        self.ttype.move(150, 650)
        self.ttype.activated[str].connect(lambda text : self.terrain.set("type", objects.TerrainType[text]))

        QLabel("Movement", self).move(450, 500)
        self.tmovement = QLineEdit(self)
        self.tmovement.move(575, 500)
        self.tmovement.textEdited.connect(lambda text : self.terrain.set("mov_cost", int(text)) if text.isdigit() else self.terrain.set("mov_cost", self.terrain.mov_cost))

        QLabel("Vision", self).move(450, 550)
        self.tvis = QLineEdit(self)
        self.tvis.move(575, 550)
        self.tvis.textEdited.connect(lambda text : self.terrain.set("vis_cost", int(text)) if text.isdigit() else self.terrain.set("vis_cost", self.terrain.vis_cost))

        QLabel("Road?", self).move(450, 600)
        self.tsubtype = QCheckBox("", self)
        self.tsubtype.move(575, 600)
        self.tsubtype.stateChanged.connect(lambda state: self.terrain.set("sub_type", objects.TerrainSubType.road) if state == Qt.Checked else self.terrain.set("sub_type", objects.TerrainSubType.normal))

        QLabel("Name", self).move(850, 500)
        self.c_tname = QLineEdit(self)
        self.c_tname.move(975, 500)
        self.c_tname.textEdited.connect(lambda text : self.terrain.set("name", text) if text.isalpha() else self.terrain.set("name", self.terrain.name))

        self.c_tsave = QPushButton("Save Terrain", self)
        self.c_tsave.resize(self.c_save.sizeHint())
        self.c_tsave.move(1250, 500) 
        self.c_tsave.clicked.connect(self.save_terrain)

        self.terrain_deleter = QPushButton("Delete Terrain", self)
        self.terrain_deleter.resize(self.terrain_deleter.sizeHint())
        self.terrain_deleter.move(1250, 550)
        self.terrain_deleter.hide()
        self.terrain_deleter.clicked.connect(self.remove_terrain)   

    def terrain_set(self):
        self.tdefense.setText(str(self.terrain.def_bonus * 100))
        self.trange.setText(str(self.terrain.rng_bonus))
        self.tvision.setText(str(self.terrain.vis_bonus))
        self.tmovement.setText(str(self.terrain.mov_cost))
        self.tvis.setText(str(self.terrain.vis_cost))
        self.ttype.setCurrentIndex(self.parent.ttypes.index(self.terrain.type.name))
        self.tsubtype.setChecked(self.terrain.sub_type == objects.TerrainSubType.road)
        self.c_tname.setText(self.terrain.name)

        if self.unit.name in self.parent.custom_terrains:
            self.terrain_deleter.show()
        else:
            self.terrain_deleter.hide()
        
    def unit_selected(self, text):
        if text in dir(units):
            c = getattr(units, text)
            self.unit = c()
            self.unit_deleter.hide()
        elif text in self.parent.custom_units:
            u_dict = self.parent.custom_units[text].copy()
            u_dict["type"] = objects.UnitType[u_dict["type"]]  
            self.unit = objects.Unit(**u_dict)
            self.unit.__class__.__name__ = self.unit.name
            self.unit_deleter.show()

        self.unit_set()

    def terrain_selected(self, text):
        if text in dir(terrains):
            c = getattr(terrains, text)
            self.terrain = c()
            self.terrain_deleter.hide()
        elif text in self.parent.custom_terrains:
            u_dict = self.parent.custom_terrains[text].copy()
            u_dict["type"] = objects.TerrainType[u_dict["type"]]
            u_dict["sub_type"] = objects.TerrainSubType[u_dict["sub_type"]]  
            self.terrain = objects.Terrain(**u_dict)
            self.terrain.__class__.__name__ = self.terrain.name
            self.terrain_deleter.show()

        self.terrain_set()

    def save_unit(self):
        name = self.unit.name
        u_dict = self.unit.__dict__.copy()
        u_dict["type"] = u_dict["type"].name

        self.parent.custom_units[name] = u_dict
        self.parent.unit_list.append(name)
        self.UnitComboBox.addItem(name)
        self.UnitComboBox.setCurrentIndex(self.parent.unit_list.index(name))

        self.other.UnitComboBox.addItem(name)
        self.unit_deleter.show()

    def remove_unit(self):
        name = self.unit.name

        self.UnitComboBox.setCurrentIndex(0)
        self.UnitComboBox.removeItem(self.parent.unit_list.index(name))

        if self.other.unit.name == name:
            self.other.UnitComboBox.setCurrentIndex(0)
            self.other.UnitComboBox.removeItem(self.parent.unit_list.index(name))
            self.other.unit_selected("Arbalests")

        del self.parent.custom_units[name]
        self.parent.unit_list.remove(name)

        self.unit_selected("Arbalests")

    def save_terrain(self):
        name = self.terrain.name
        u_dict = self.terrain.__dict__.copy()
        u_dict["type"] = u_dict["type"].name
        u_dict["sub_type"] = u_dict["sub_type"].name

        self.parent.custom_terrains[name] = u_dict
        self.parent.terrain_list.append(name)
        self.TerrainComboBox.addItem(name)
        self.TerrainComboBox.setCurrentIndex(self.parent.terrain_list.index(name))

        self.other.TerrainComboBox.addItem(name)
        self.terrain_deleter.show()

    def remove_terrain(self):
        name = self.terrain.name

        self.TerrainComboBox.setCurrentIndex(0)
        self.TerrainComboBox.removeItem(self.parent.terrain_list.index(name))

        if self.other.terrain.name == name:
            self.other.TerrainComboBox.setCurrentIndex(0)
            self.other.TerrainComboBox.removeItem(self.parent.terrain_list.index(name))
            self.other.terrain_selected("Bridge")

        del self.parent.custom_terrains[name]
        self.parent.terrain_list.remove(name)

        self.terrain_selected("Bridge")

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.unit_list = ['Arbalests', 'Archers', 'Axemen', 'Berserkers', 'Bombards', 'Camels', 'Cavaliers', 'Champions', 'ChuKoNu', 'Crossbowmen', 'EliteArchers', 'EliteAxemen', 'EliteBerserkers', 'EliteJanissaries', 'EliteLongbowmen', 'EliteMameluks', 'EliteMangudai', 'EliteMonks', 'ElitePikemen', 'EliteRaiders', 'EliteSamurai', 'EliteSkirmishers', 'EliteTemplars', 'ExpertSkirmishers', 'HandCanon', 'HeavyCamels', 'HeavyHorseArchers', 'HeavyScorpions', 'HorseArchers', 'Janissaries', 'Knights', 'LightCav', 'Longbowmen', 'Longswordsmen', 'MaA', 'Mameluks', 'Mangudai', 'Milita', 'Monks', 'Onager', 'Paladins', 'Pikemen', 'Raiders', 'Rams', 'Samurai', 'Scorpions', 'ScoutCav', 'SiegeRams', 'Skirmishers', 'Spearmen', 'Templars', 'Trebuchets', 'TwoHanded', 'Villager', 'WarElephants']
        self.terrain_list = ['Bridge', 'Desert', 'DesertRoad', 'Ford', 'Forest', 'Hill', 'HillRoad', 'Mountain', 'MountainRoad', 'Plain', 'PlainRoad', 'Swamp']
        self.types = ['cavalry', 'infantry', 'ranged', 'siege', 'structure']
        self.ttypes = ['bridge', 'desert', 'ford', 'forest', 'hill', 'mountain', 'plain', 'structure', 'swamp']
        
        with open("custom_units.json", "r") as f:
            self.custom_units = json.load(f)
        
        self.unit_list += self.custom_units.keys()
        self.unit_list = sorted(self.unit_list)

        with open("custom_terrains.json", "r") as f:
            self.custom_terrains = json.load(f)
        
        self.terrain_list += self.custom_terrains.keys()
        self.terrain_list = sorted(self.terrain_list)

        with open("custom_abilities.json", "r") as f:
            self.custom_abilities = json.load(f)

        self.distance = 1
        self.debug = False

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        self.left = SideFrame(self, name="Attacker")
        self.left.setFrameShape(QFrame.StyledPanel)
 
        self.right = SideFrame(self, name="Defender")
        self.right.setFrameShape(QFrame.StyledPanel)

        self.right.other = self.left
        self.left.other = self.right

        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)

        self.ability_creator = AbilityCreator(self.bottom)
        self.ability_creator.resize(800, 500)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.left)
        splitter1.addWidget(self.right)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        splitter2.setSizes([400, 400])

        self.init_bottom()

        self.setGeometry(300, 300, 900, 900)
        self.setWindowTitle('AoE: Age of Kings Battle Simulator')
        self.showMaximized()
        self.setWindowIcon(QIcon("icon.png"))

        self.show()

    def init_bottom(self):
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

        self.abilities_btn = QPushButton("Ability Creator", self.bottom)
        self.abilities_btn.resize(self.abilities_btn.sizeHint())
        self.abilities_btn.move(250, 150)
        self.abilities_btn.clicked.connect(lambda: self.ability_creator.show())

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
        self.debug_b.stateChanged.connect(self.debug_checker)

        self.cmd = QPlainTextEdit(self.bottom)
        self.cmd.resize(700, 40)
        self.cmd.move(1550, 50)
        self.cmd.hide()

        self.cmd_run = QPushButton("Run", self.bottom)
        self.cmd_run.resize(self.cmd_run.sizeHint())
        self.cmd_run.move(1550, 110)
        self.cmd_run.clicked.connect(self.eval_code)
        self.cmd_run.hide()

    def debug_checker(self, state):
        self.__setattr__("debug", state == Qt.Checked)
        if state == Qt.Checked:
            self.cmd.show()
            self.cmd_run.show()
        else:
            self.cmd.hide()
            self.cmd_run.hide()

    def eval_code(self):
        try:
            eval(self.cmd.toPlainText())
        except Exception as e:
            print(e)
            traceback.format_exc()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Do you wish to save the changes you made?", QMessageBox.Yes | 
            QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)

        if reply == QMessageBox.Yes:
            with open("custom_units.json", "w") as f:
                json.dump(self.custom_units, f)

            with open("custom_terrains.json", "w") as f:
                json.dump(self.custom_terrains, f)

            with open("custom_abilities.json", "w") as f:
                json.dump(self.custom_abilities, f)

            event.accept()
        elif reply == QMessageBox.Cancel:
            event.ignore()
        else:
            event.accept()

    def battle(self, ctx):
        def priority_check():
            if "first strike" in ctx.attacker.abilities:
                return False

            if "first strike" in ctx.defender.abilities:
                return True 

            if ctx.distance > 1:
                return False

            if "skirmish" in ctx.defender.abilities:
                return True

            if "anti-cavalry" in ctx.defender.abilities and ctx.attacker.type == objects.UnitType.cavalry:
                return True

            return False

        if priority_check():
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

        if "zeal" in ctx.attacker.abilities and ctx.attacker.health > 0:
            ctx.attacker.health += 20 if ctx.attacker.health + 20 <= 100 else 100 - ctx.attacker.health

        if "zeal" in ctx.defender.abilities and ctx.defender.health > 0:
            ctx.defender.health += 20 if ctx.defender.health + 20 <= 100 else 100 - ctx.defender.health

        ctx.attacker.battles += 1
        ctx.defender.battles += 1

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
                debug = self.debug,
                custom_abilities = self.custom_abilities
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
        self.right.UnitComboBox.setCurrentIndex(self.unit_list.index(self.left.unit.__class__.__name__))
        self.left.UnitComboBox.setCurrentIndex(self.unit_list.index(self.right.unit.__class__.__name__))

        self.left.unit, self.right.unit = self.right.unit, self.left.unit

        self.left.unit_set()
        self.right.unit_set()

    def inverse_terrain(self):
        self.right.TerrainComboBox.setCurrentIndex(self.terrain_list.index(self.left.terrain.name))
        self.left.TerrainComboBox.setCurrentIndex(self.terrain_list.index(self.right.terrain.name))
        
        self.left.terrain, self.right.terrain = self.right.terrain, self.left.terrain

        self.left.terrain_set()
        self.right.terrain_set()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = GUI()
    sys.exit(app.exec_())
