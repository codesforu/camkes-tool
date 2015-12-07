#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc, six, sys, os
from gi.repository import Gtk


class Controller(six.with_metaclass(abc.ABCMeta, object)):

    # --- Properties ---
    '''
    The parent_controller property gives the controller access to its parent. If the controller
    has no parent, this will be None. Hence, one must check before it assumes there is a parent.
    '''

    @property
    def parent_controller(self):
        return self._parent_controller
    
    @parent_controller.setter
    def parent_controller(self, value):
        assert issubclass(value.__class__, Controller) or isinstance(value, Controller)
        self._parent_controller = value

    '''
    Every controller must have a view that it controls. This property will hold the root view.

    To keep consistent with GTK terminology, we shall call views, widgets.
    This widget could be a subclass of Gtk.Widget. If using a subclass of widget, the
    subclass of Controller is expected to override the getter/setter, to assert the expect subclass.
    '''
    @property
    def root_widget(self):
        return self._root_widget

    @root_widget.setter
    def root_widget(self, value):
        assert issubclass(value.__class__, Gtk.Widget) or isinstance(value, Gtk.Widget)
        self._root_widget = value

    # --- Methods ---
    '''
    The subclass is expected to load their model and widgets when initialised.
    '''
    def __init__(self):
        super(Controller,self).__init__()
        self._parent_controller = None
        self._root_widget = None
