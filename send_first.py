# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
# Copyright (C) 2012 - Carrasco Agustin
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
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

from gi.repository import GObject, Gtk, Peas, RB

from send_rb3compat import ActionGroup
from send_rb3compat import Action
from send_rb3compat import ApplicationShell

import gettext
gettext.install('rhythmbox', RB.locale_dir(), unicode=True)

ui_context_menu = """
<ui>
    <popup name="QueuePlaylistViewPopup">
        <placeholder name="PluginPlaceholder">
            <menuitem name="QueuePopupSendFirst" action="SendFirstAction"/>
        </placeholder>
    </popup>
    <popup name="BrowserSourceViewPopup">
        <placeholder name="PluginPlaceholder">
            <menuitem name="BrowserPopupQueueFirst" action="QueueFirstAction"/>
        </placeholder>
    </popup>
    <popup name="PlaylistViewPopup">
        <placeholder name="PluginPlaceholder">
            <menuitem name="BrowserPopupQueueFirst" action="QueueFirstAction"/>
        </placeholder>
    </popup>
    <popup name="PodcastViewPopup">
        <placeholder name="PluginPlaceholder">
	        <menuitem name="BrowserPopupQueueFirst" action="QueueFirstAction"/>
        </placeholder>
    </popup>
</ui>
"""

class SendFirstPlugin (GObject.Object, Peas.Activatable):
    __gtype_name = 'SendFirstPlugin'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

	def do_activate (self):
		self.shell = self.object
		
		#uim = self.shell.props.ui_manager	
        
        self.action_group = ActionGroup(self.shell, 'SendFirstPluginActionGroup')
        
        action = self.action_group.add_action(source=self.shell.props.queue_source,
            action_name='SendFirstAction', label=_('Send first'),
            func=self.send_first)
            
        action = self.action_group.add_action(source=self.shell.props.queue_source,
            shell = self.shell,
            action_name='QueueFirstAction', label=_('Queue first'),
            func=self.queue_first)

        self._appshell = ApplicationShell(self.shell)
        self._appshell.insert_action_group(self.action_group)
        self._appshell.add_browser_menuitems(ui_context_menu, self.action_group.name)

		#creamos las actions
        #self.sendfirst_action = Gtk.Action( 'SendFirstAction', 
        #                                     _('Send first'), 
        #                                     _('Send this song to the beginning of the list.'),
        #                                    Gtk.STOCK_GOTO_TOP )                                           
                                   
        #self.sendfirst_action.connect ( 'activate', self.send_first, 
        #                                            self.shell.props.queue_source )  
                                               
                                               #creamos las actions
        #self.queuefirst_action = Gtk.Action( 'QueueFirstAction', 
        #                                      _('Queue first'), 
        #                                      _('Send this song to the beginning of the play queue.'),
        #                                      Gtk.STOCK_ADD )                                           
                                   
        #self.queuefirst_action.connect ( 'activate', self.queue_first, 
        #                                             self.shell,
        #                                             self.shell.props.queue_source )       
                
        #creamos el action group y lo agregamos a la interfaz
        #self.action_group = Gtk.ActionGroup( 'SendFirstPluginActionGroup' )
        #self.action_group.add_action( self.sendfirst_action )    
        #self.action_group.add_action( self.queuefirst_action )    
        #uim.insert_action_group( self.action_group, -1 )
                
        #cargamos la definición de la ui y obtenemos el id del ui
        #self.ui_id = uim.add_ui_from_string( ui_context_menu )
        
        #updateamos la ui
        #uim.ensure_update()        
	
	def do_deactivate (self):
		self._appshell.cleanup()
		#uim = self.shell.props.ui_manager
		
		#uim.remove_action_group(self.action_group)
        #uim.remove_ui(self.ui_id)
        #uim.ensure_update()

        #del self.action_group
        #del self.sendfirst_action
        #del self.queuefirst_action

	def send_first(self, action, param, args):
	    #get the selected entries
        queue = args['source']
        
	    selected = queue.get_entry_view().get_selected_entries()
	    
	    #relocate them first
	    selected.reverse()
	    
	    for entry in selected:
	        queue.move_entry( entry, 0 )  
	        
	def queue_first(self, action, param, args ):
	    #get the selected entries
        shell = args['shell']
        queue = args['source']
        
	    page = shell.props.selected_page
	    selected = page.get_entry_view().get_selected_entries()
	    
	    #add them first
	    selected.reverse()
	    
	    for entry in selected:
	        queue.add_entry( entry, 0 )    
