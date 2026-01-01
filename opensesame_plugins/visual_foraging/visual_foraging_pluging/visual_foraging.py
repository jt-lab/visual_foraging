"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from random import randint
from qtpy import QtGui, QtCore, QtWidgets
from .serialization_helpers import serialize_elements, deserialize_elements
from .patch_helpers import get_element_instances
from .element_list import ElementList
from .background_picker import BackgroundPicker
from .generator_selector import GeneratorSelector
from .background_selector import BackgroundSelector
from .location_selector import LocationSelector
from .input_helpers import get_click
import pygame
from numpy import array
from numpy.linalg import norm

class VisualForaging(Item):
    
    loaded_images = {}
    element_instances = {}
    click_radius = 32 # Make control
    screen = None
    mouse = None
    
    def check_clicked(self, click_pos, time):
        click_pos = (click_pos[0], click_pos[1])
        #clicks.append({'position' : click_pos, 'time_stamp': time})
        print(click_pos)
        for ei in self.element_instances:
            element_pos = array([ei['x'], ei['y']])
            click_pos = array(click_pos)
            ei['dist_to_click'] = norm(element_pos-click_pos) 
        closest_element = self.element_instances[0]
        for ei in self.element_instances:
            if ei['dist_to_click'] < closest_element['dist_to_click']:
                closest_element = ei	  
        if closest_element['dist_to_click'] > self.click_radius:
            return
        # TODO: play sounds, etc
        print(closest_element)
        if closest_element in self.element_instances:
            self.element_instances.remove(closest_element)
    
    def check_complete(self):
        for ei in self.element_instances:
            if ei['role'] == 'target':
                return False
        return True
  

    def reset(self):
        """Resets plug-in to initial values."""
        self.var.show_mousepointer = 'yes'


    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()
        
        if self.screen is None:
            if self.var.fullscreen == 'yes':
                self.screen = pygame.display.set_mode((self.var.width, self.var.height),  pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((self.var.width, self.var.height))
            
        pygame.mouse.set_visible(self.var.show_mousepointer == 'yes')
        
        element_types = deserialize_elements(getattr(self.var, "elements", None))
        self.element_instances = get_element_instances(element_types)  
        
        # Load images
        self.loaded_images = {
            el["image"]: pygame.image.load(self.experiment.pool[el["image"]]) for el in element_types
        }
        
        print("POSITIONS: " + str(self.var.location_settings))
       

    def run(self):
        """The run phase of the plug-in goes here."""
        
        trial_start_time = self.clock.time()
        while not self.check_complete():
            print("COLOR: " + self.var.background['color'])
            self.screen.fill(pygame.Color(self.var.background))
            for ei in self.element_instances:
                img = self.loaded_images[ei['image']]
                self.screen.blit(img,
                    (int(ei['x'] - img.get_width() / 2),
                     int(ei['y'] - img.get_height() / 2))
                )
            pygame.display.flip()
            
            
            #button, pos, time = pygame.mouse.get_click()
            
            
            
            click_info = get_click()
            
            if click_info:
                # TODO: why not keep the dict and use it in check_clicked
                self.check_clicked((click_info['x'], click_info['y']), click_info['rt'])



class QtVisualForaging(VisualForaging, QtAutoPlugin):
    def __init__(self, name, experiment, script=None):
        VisualForaging.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        super().init_edit_widget()
        
        # --- Location selector ----------------------------------------------------
        self.location_selector = LocationSelector(plugin=self)
        self.location_selector.textChanged.connect(
                lambda txt: setattr(self.var, "location_settings", txt)
        )
        index = self.edit_vbox.count() - 2
        self.edit_vbox.insertWidget(index, self.location_selector)
        
        bg = BackgroundSelector(main_window=self.main_window, plugin=self)
        self.auto_line_edit['background'] = bg

        index = self.edit_vbox.count() - 2
        self.edit_vbox.insertWidget(index, bg)
        lbl = QtWidgets.QLabel("Elements:")
        lbl.setStyleSheet("font-weight: bold;")  
        index = self.edit_vbox.count() - 2
        self.edit_vbox.insertWidget(index, lbl)

        cl = ElementList(experiment=self.experiment,
                 main_window=self.main_window, plugin=self)

        index = self.edit_vbox.count() - 2
        self.edit_vbox.insertWidget(index, cl)
        

        self.auto_line_edit['elements'] = cl
        
        
        
        
