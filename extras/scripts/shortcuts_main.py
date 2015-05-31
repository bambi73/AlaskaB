# coding=utf-8
import os, sys
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, urllib, xbmcvfs
import xml.etree.ElementTree as xmltree
import cPickle as pickle
import cProfile
import pstats
import random
import time
from time import gmtime, strftime
from datetime import datetime
from traceback import print_exc

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

#__addonid__    = "skin.alaskab"
__addonid__    = "script.skinshortcuts"
__language__   = xbmc.getLocalizedString
__cwd__        = xbmc.translatePath("special://skin/").decode('utf-8')
__datapath__   = os.path.join(xbmc.translatePath("special://profile/").decode('utf-8'), "addon_data", __addonid__)
__masterpath__ = os.path.join(xbmc.translatePath("special://masterprofile/").decode('utf-8'), "addon_data", __addonid__)

import shortcuts_xml
XML = shortcuts_xml.XMLFunctions()

hashlist = []

def log(txt):
    if isinstance (txt, str):
        txt = txt.decode('utf-8')
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode('utf-8'), level=xbmc.LOGDEBUG)
        
class Main:

    def __init__(self):
        self._parse_argv()
        self.WINDOW = xbmcgui.Window(10000)    
        
        # Create data and master paths if not exists
        if not xbmcvfs.exists(__datapath__):
            xbmcvfs.mkdir(__datapath__)
        if not xbmcvfs.exists(__masterpath__):        # TODO???
            xbmcvfs.mkdir(__masterpath__)
        
        if self.TYPE == "buildxml":
            XML.buildMenu(self.MAINMENUID, self.GROUP, self.LEVELS, self.MODE, self.OPTIONS)
        elif self.TYPE == "manage":
            self._manage_shortcuts(self.GROUP, self.GROUPNAME)
        elif self.TYPE == "resetall":
            try:
                xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
            except:
                log("Not launched from a list item")
            self._reset_all_shortcuts()


    def _parse_argv(self):
        try:
            params = dict(arg.split("=") for arg in sys.argv[ 1 ].split("&"))
            self.TYPE = params.get("type", "")
        except:
            self.TYPE = ""
            params = {}
        
        self.GROUP = params.get("group", "")
        self.GROUPNAME = params.get( "groupname", None )
        self.MAINMENUID = params.get("mainmenuID", "0")
        
    # -----------------
    # PRIMARY FUNCTIONS
    # -----------------

    def _manage_shortcuts(self, group, groupname):            
        import shortcuts_gui
        ui = shortcuts_gui.GUI("script-skinshortcuts.xml", __cwd__, "default", group=group, groupname=groupname)
        ui.doModal()
        del ui
        
        # Clear window properties for this group, and for backgrounds, widgets, properties
        xbmcgui.Window(10000).clearProperty("skinshortcuts-" + group)        
        xbmcgui.Window(10000).clearProperty("skinshortcutsWidgets")        
        xbmcgui.Window(10000).clearProperty("skinshortcutsCustomProperties")        
        xbmcgui.Window(10000).clearProperty("skinshortcutsBackgrounds")        


    def _reset_all_shortcuts(self):
        log("### Resetting all shortcuts")
        
        dialog = xbmcgui.Dialog()
        shouldRun = dialog.yesno(__language__(32037), __language__(32038))
        
        if shouldRun:
            for files in xbmcvfs.listdir(__datapath__):
                # Try deleting all shortcuts
                if files:
                    for file in files:
                        if file != "settings.xml":
                            file_path = os.path.join(__datapath__, file.decode('utf-8')).encode('utf-8')
                            if xbmcvfs.exists(file_path):
                                try:
                                    xbmcvfs.delete(file_path)
                                except:
                                    print_exc()
                                    log("### ERROR could not delete file %s" % file[0])
        
            # Reset all window properties (so menus will be reloaded)
            self.reset_window_properties()
        
    
    # ----------------
    # SKINSETTINGS.XML
    # ----------------
                            
    
    def reset_window_properties(self):
        xbmcgui.Window(10000).clearProperty("skinshortcuts-overrides-skin")


if __name__ == "__main__" :
    Main()
