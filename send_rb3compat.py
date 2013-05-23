# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

from gi.repository import Gtk
from gi.repository import Gio
import sys
import rb
import lxml.etree as ET

PYVER = sys.version_info[0]

if PYVER >= 3:
    import urllib.request, urllib.parse, urllib.error
else:
    import urllib
    from urlparse import urlparse as rb2urlparse

if PYVER >= 3:
    import http.client
else:
    import httplib
    
def responses():
    if PYVER >=3:
        return http.client.responses
    else:
        return httplib.responses

def unicodestr(param, charset):
    if PYVER >=3:
        return str(param, charset)
    else:
        return unicode(param, charset)
        
def unicodeencode(param, charset):
    if PYVER >=3:
        return str(param).encode(charset)
    else:
        return unicode(param).encode(charset)

def urlparse(uri):
    if PYVER >=3:
        return urllib.parse.urlparse(uri)
    else:
        return rb2urlparse(uri)
        
def url2pathname(url):
    if PYVER >=3:
        return urllib.request.url2pathname(url)
    else:
        return urllib.url2pathname(url)

def urlopen(filename):
    if PYVER >=3:
        return urllib.request.urlopen(filename)
    else:
        return urllib.urlopen(filename)
        
def pathname2url(filename):
    if PYVER >=3:
        return urllib.request.pathname2url(filename)
    else:
        return urllib.pathname2url(filename)

def unquote(uri):
    if PYVER >=3:
        return urllib.parse.unquote(uri)
    else:
        return urllib.unquote(uri)
                
def quote(uri, safe=None):
    if PYVER >=3:
        if safe:
            return urllib.parse.quote(uri,safe=safe)
        else:
            return urllib.parse.quote(uri)
    else:
        if safe:
            return urllib.quote(uri, safe=safe)
        else:
            return urllib.quote(uri)
        
def quote_plus(uri):
    if PYVER >=3:
        return urllib.parse.quote_plus(uri)
    else:
        return urllib.quote_plus(uri)

        
def is_rb3(shell):
	if hasattr( shell.props.window, 'add_action' ):
		return True
	else:
		return False 	
		
class Menu(object):
    '''
    Menu object used to create window popup menus
    '''
	def __init__(self, plugin, shell):
        '''
        Initializes the menu.
        '''
		self.plugin = plugin
		self.shell = shell
        self._unique_num = 0
        
        self._rbmenu_items = {}
        
    def add_menu_item(self, menubar, section_name, label, action):
        '''
        add a new menu item to the popup
        :param menubar: `str` is the name GtkMenu (or blank for RB2.99+)
        :param section_name: `str` is the name of the section to add the item to
        :param label: `str` is the text of the menu item displayed to the user
        :param action: `GtkAction` or `Gio.SimpleAction associated with the menu item
        '''
        return self.insert_menu_item(menubar, section_name, -1, label, action)

    def insert_menu_item(self, menubar, section_name, position, label, action):
        if is_rb3(self.shell):
            app = self.shell.props.application
            item = Gio.MenuItem()
            item.set_label(label)
            item.set_detailed_action('win.'+action.get_name())
            
            if not section_name in self._rbmenu_items:
                self._rbmenu_items[section_name] = []
            self._rbmenu_items[section_name].append(label)
            
            app.add_plugin_menu_item(section_name, label, item)
        else:
            item = Gtk.MenuItem(label=label)
            item.set_related_action(action)
            self._rbmenu_items[label] = item
            bar = self.get_menu_object(menubar)
            if position == -1:
                bar.append(item)
            else:
                bar.insert(item, position)
            bar.show_all()
            uim = self.shell.props.ui_manager
            uim.ensure_update()

        return item

    def insert_separator(self, menubar, at_position):
        if not is_rb3(self.shell):
            menu_item = Gtk.SeparatorMenuItem().new()
            menu_item.set_visible(True)
            self._rbmenu_items['separator' + str(self._unique_num)] = menu_item
            self._unique_num = self._unique_num + 1
            bar = self.get_menu_object(menubar)
            bar.insert(menu_item, at_position)
            bar.show_all()
            uim = self.shell.props.ui_manager
            uim.ensure_update()

    def remove_menu_items(self, menubar, section_name):
        '''
        utility function to remove all menuitems associated with the menu section
        :param menubar: `str` is the name of the section containing the menu items
        '''
        if is_rb3(self.shell):
            if not section_name in self._rbmenu_items:
                return
                
            app = self.shell.props.application
            
            for menu_item in self._rbmenu_items[section_name]:
                app.remove_plugin_menu_item(section_name, menu_item)

            if self._rbmenu_items[section_name]:
                del self._rbmenu_items[section_name][:]
            
        else:

            if not self._rbmenu_items:
                return

            uim = self.shell.props.ui_manager
            bar = self.get_menu_object(menubar)

            for menu_item in self._rbmenu_items:
                bar.remove(self._rbmenu_items[menu_item])

            #del self._rbmenu_items[:]
            
            bar.show_all()
            uim.ensure_update()
		
	def load_from_file(self, rb2_ui_filename, rb3_ui_filename ):
        '''
        utility function to load the menu structure
        :param rb2_ui_filename: `str` RB2.98 and below UI file
        :param rb3_ui_filename: `str` RB2.99 and higher UI file
        '''
		from coverart_browser_prefs import CoverLocale
		cl = CoverLocale()
		self.builder = Gtk.Builder()
        self.builder.set_translation_domain(cl.Locale.LOCALE_DOMAIN)
        
        if is_rb3(self.shell):
			ui_filename = rb3_ui_filename
		else:
			ui_filename = rb2_ui_filename
			
        self.builder.add_from_file(rb.find_plugin_file(self.plugin,
            ui_filename))

    def _connect_rb3_signals(self, signals):
		def _menu_connect(action_name, func):
			action = Gio.SimpleAction(name=action_name)
			action.connect('activate', func)
			action.set_enabled(True)
			self.shell.props.window.add_action(action)
			
		for key,value in signals.items():
			_menu_connect( key, value)
		
	def _connect_rb2_signals(self, signals):
		def _menu_connect(menu_item_name, func):
			menu_item = self.builder.get_object(menu_item_name)
			menu_item.connect('activate', func)
			
		for key,value in signals.items():
			_menu_connect( key, value)
			
	def connect_signals(self, signals):
        '''
        connect all signal handlers with their menuitem counterparts
        :param signals: `dict` key is the name of the menuitem 
             and value is the function callback when the menu is activated
        '''		
        if is_rb3(self.shell):
			self._connect_rb3_signals(signals)
		else:
			self._connect_rb2_signals(signals)
            
    def get_gtkmenu(self, source, popup_name):
        '''
        utility function to obtain the GtkMenu from the menu UI file
        :param popup_name: `str` is the name menu-id in the UI file
        '''
        item = self.builder.get_object(popup_name)
        
        if is_rb3(self.shell):
            app = self.shell.props.application
            app.link_shared_menus(item)
            popup_menu = Gtk.Menu.new_from_model(item)
            popup_menu.attach_to_widget(source, None)
        else:
            popup_menu = item
        
        return popup_menu
			
	def get_menu_object(self, menu_name_or_link):
        '''
        utility function returns the GtkMenuItem/Gio.MenuItem
        :param menu_name_or_link: `str` to search for in the UI file
        '''
		item = self.builder.get_object(menu_name_or_link)

		if is_rb3(self.shell):
            if item:
                popup_menu = item
            else:
                app = self.shell.props.application
                popup_menu = app.get_plugin_menu(menu_name_or_link)
		else:
			popup_menu = item
			
		return popup_menu

	def set_sensitive(self, menu_or_action_item, enable):
		'''
        utility function to enable/disable a menu-item
        :param menu_or_action_item: `GtkMenuItem` or `Gio.SimpleAction`
           that is to be enabled/disabled
        :param enable: `bool` value to enable/disable
        '''
        
		if is_rb3(self.shell):
			item = self.shell.props.window.lookup_action(menu_or_action_item)
			item.set_enabled(enable)
		else:
			item = self.builder.get_object(menu_or_action_item)
			item.set_sensitive(enable)
			
class ActionGroup(object):
	def __init__(self, shell, group_name):
		self.group_name = group_name
		self.shell = shell
    
        self._actions = {}
        
		if is_rb3(self.shell):
			self.actiongroup = Gio.SimpleActionGroup()
		else:			
			self.actiongroup = Gtk.ActionGroup(group_name)
			uim = self.shell.props.ui_manager
			uim.insert_action_group(self.actiongroup)

    @property
    def name(self):
        return self.group_name
            
    def remove_actions(self):
        for action in self.actiongroup.list_actions():
            self.actiongroup.remove_action(action)
            
    def get_action(self, action_name):
        return self._actions[action_name]
            
    def add_action(self, func, action_name, **args ):
        
        if 'label' in args:
            label = args['label']
        else:
            label=action_name
        
        if is_rb3(self.shell):
            action = Gio.SimpleAction.new(action_name, None)
            action.connect('activate', func, args)
            action_type = 'win'
            if 'action_type' in args:
                if args['action_type'] == 'app':
                    action_type = 'app'

            if action_type == 'app':
                app = Gio.Application.get_default()
                app.add_action(action)
            else:
                self.shell.props.window.add_action(action)
                self.actiongroup.add_action(action)
        else:
            action = Gtk.Action(label=label,
                name=action_name,
               tooltip='', stock_id=Gtk.STOCK_CLEAR)
            action.connect('activate', func, None, args)
            self.actiongroup.add_action(action)
            
        act = Action(self.shell, action)
        act.label = label
            
        self._actions[action_name] = act
            
        return act

class ApplicationShell(object):
    # storage for the instance reference
    __instance = None
    
    class __impl:
        """ Implementation of the singleton interface """
        def __init__(self, shell):
            self.shell = shell
            
            if is_rb3(self.shell):
                self._uids = {}
            else:
                self._uids = []
                
            self._action_groups = {}
            
        def insert_action_group(self, action_group):
            self._action_groups[action_group.name] = action_group
            
        def lookup_action(self, action_group_name, action_name, action_type='app'):
            if is_rb3(self.shell):
                if action_type == "app":
                    action = self.shell.props.application.lookup_action(action_name)
                else:
                    action = self.shell.props.window.lookup_action(action_name)

            else:
                uim = self.shell.props.ui_manager
                ui_actiongroups = uim.get_action_groups()

                actiongroup = None
                for actiongroup in ui_actiongroups:
                    if actiongroup.get_name() == action_group_name:
                        break

                action = None
                if actiongroup:
                    action = actiongroup.get_action(action_name)

            return Action(self.shell, action)

        def add_app_menuitems(self, ui_string, group_name):
            if is_rb3(self.shell):
                root = ET.fromstring(ui_string)
                for elem in root.findall(".//menuitem"):
                    action_name = elem.attrib['action']
                    item_name = elem.attrib['name']
                    
                    group = self._action_groups[group_name]
                    act = group.get_action(action_name)
                    
                    item = Gio.MenuItem()
                    item.set_label(act.label)
                    item.set_detailed_action('app.' + action_name)
                    app = Gio.Application.get_default()
                    app.add_plugin_menu_item('tools', 
                        action_name, item)
                    self._uids[action_name] = 'tools'
            else:
                uim = self.shell.props.ui_manager
                self._uids.append(uim.add_ui_from_string(ui_string))
                uim.ensure_update()
                
        def add_browser_menuitems(self, ui_string, group_name):
            if is_rb3(self.shell):
                root = ET.fromstring(ui_string)
                for elem in root.findall("./popup"):
                    popup_name = elem.attrib['name']
                    
                    menuelem = elem.find('.//menuitem')
                    action_name = menuelem.attrib['action']
                    item_name = menuelem.attrib['name']
                    
                    group = self._action_groups[group_name]
                    act = group.get_action(action_name)
                    
                    item = Gio.MenuItem()
                    item.set_label(act.label)
                    item.set_detailed_action('win.' + action_name)
                    app = Gio.Application.get_default()
                    
                    if popup_name == 'QueuePlaylistViewPopup':
                        plugin_type = 'queue-popup'
                    elif popup_name == 'BrowserSourceViewPopup':
                        plugin_type = 'browser-popup'
                    elif popup_name == 'PlaylistViewPopup':
                        plugin_type = 'playlist-popup'
                    elif popup_name == 'PodcastViewPopup':
                        plugin_type = 'podcast-episode-popup'
                    else:
                        print "unknown type %s" % plugin_type
                        
                    app.add_plugin_menu_item(plugin_type, action_name, item)
                    self._uids[plugin_type]=action_name
            else:
                uim = self.shell.props.ui_manager
                self._uids.append(uim.add_ui_from_string(ui_string))
                uim.ensure_update()

        def cleanup(self):
            if is_rb3(self.shell):
                for uid in self._uids:
                    
                    Gio.Application.get_default().remove_plugin_menu_item(uid, 
                        self._uids[uid])
            else:
                uim = self.shell.props.ui_manager
                for uid in self._uids:
                    uim.remove_ui(uid)
                uim.ensure_update();

    def __init__(self, shell):
        """ Create singleton instance """
        # Check whether we already have an instance
        if ApplicationShell.__instance is None:
            # Create and remember instance
            ApplicationShell.__instance = ApplicationShell.__impl(shell)

        # Store instance reference as the only member in the handle
        self.__dict__['_ApplicationShell__instance'] = ApplicationShell.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

class Action(object):
    def __init__(self, shell, action):
		self.shell = shell
        self.action = action
        
        self._label = ''

    @property
    def label(self):
        if not is_rb3(self.shell):
            return self.action.get_label()
        else:
            return self._label
            
    @label.setter
    def label(self, new_label):
        self._label = new_label

    def get_sensitive(self):
        if is_rb3(self.shell):
            return self.action.get_enabled()
        else:
            return self.action.get_sensitive()
            
    def activate(self):
        if is_rb3(self.shell):
            self.action.activate(None)
        else:
            self.action.activate()
        