import sys
import xbmc, xbmcaddon, xbmcgui, xbmcplugin

def movetile():
    label = xbmc.getInfoLabel("Skin.String(home."+str(i)+".label)")
    path = xbmc.getInfoLabel("Skin.String(home."+str(i)+".path)")
    icon = xbmc.getInfoLabel("Skin.String(home."+str(i)+".icon)")
    bgcolor = xbmc.getInfoLabel("Skin.String(home."+str(i)+".bgcolor)")
    bgwidget = xbmc.getInfoLabel("Skin.String(home."+str(i)+".bgwidget)")
    bgwidgettype = xbmc.getInfoLabel("Skin.String(home."+str(i)+".bgwidget.type)")
    enabled = xbmc.getInfoLabel("Skin.HasSetting(home."+str(i)+".enabled)")
    
    # Disable the tile
    xbmc.executebuiltin("Skin.Reset(home."+str(i)+".enabled)")
    
    # Only move info and enable tile if it was enabled before
    if str(enabled) == "True":
        xbmc.executebuiltin("Skin.SetBool(home."+str(o)+".enabled)")
        xbmc.executebuiltin("Skin.SetString(home."+str(o)+".label,"+str(label)+")")
        xbmc.executebuiltin("Skin.SetString(home."+str(o)+".path,"+str(path)+")")
        xbmc.executebuiltin("Skin.SetString(home."+str(o)+".icon,"+str(icon)+")")
        xbmc.executebuiltin("Skin.SetString(home."+str(o)+".bgcolor,"+str(bgcolor)+")")
        xbmc.executebuiltin("Skin.SetString(home."+str(o)+".bgwidget,"+str(bgwidget)+")")
        xbmc.executebuiltin("Skin.SetString(home."+str(o)+".bgwidget.type,"+str(bgwidgettype)+")")

def removetile():
    xbmc.executebuiltin("Skin.Reset("+str(sys.argv[2])+".enabled)")
    xbmc.executebuiltin("Skin.Reset("+str(sys.argv[2])+".label)")
    xbmc.executebuiltin("Skin.Reset("+str(sys.argv[2])+".path)")
    xbmc.executebuiltin("Skin.Reset("+str(sys.argv[2])+".icon)")
    xbmc.executebuiltin("Skin.Reset("+str(sys.argv[2])+".bgwidget)")
    xbmc.executebuiltin("Skin.Reset("+str(sys.argv[2])+".bgwidget.type)")

def get_class_members(klass):
    ret = dir(klass)
    if hasattr(klass,'__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret

def uniq( seq ): 
    """ the 'set()' way ( use dict when there's no set ) """
    return list(set(seq))
    
def get_object_attrs( obj ):
    # code borrowed from the rlcompleter module ( see the code for Completer::attr_matches() )
    ret = dir( obj )
    ## if "__builtins__" in ret:
    ##    ret.remove("__builtins__")

    if hasattr( obj, '__class__'):
        ret.append('__class__')
        ret.extend( get_class_members(obj.__class__) )

        ret = uniq( ret )

    return ret
    
def prepareShutdownMenu(window, list, buttonId):
    if(xbmc.getCondVisibility("Control.IsVisible(%i)" % buttonId)):
        button = window.getControl(buttonId)
        listItem = xbmcgui.ListItem(label=button.getLabel())
        listItem.setPath(path='plugin://plugin.bambi.utils?type=bzzz')
        #xbmcplugin.addDirectoryItem( int( sys.argv[ 1 ] ), item2[ "file" ], liz, False, self.LIMIT )
        list.addItem(listItem)
        xbmc.log("adding %i" % buttonId)
    
class Utils:
    def __init__(self):
        self._parse_argv()
        self.WINDOW_10111 = xbmcgui.Window(10111)

        xbmc.log("self.TYPE: %s" % self.TYPE) 
        xbmc.log("self.LIST_ID: %i" % self.LIST_ID) 
        xbmc.log("self.START_BUTTON_ID: %i" % self.START_BUTTON_ID) 
        xbmc.log("self.END_BUTTON_ID: %i" % self.END_BUTTON_ID) 
        
        
    def _parse_argv( self ):
        try:
            params = dict( arg.split( "=" ) for arg in sys.argv[ 2 ].split( "&" ) )
        except:
            params = {}
        self.TYPE = params.get( "?type", "loadShutdownMenu" )
        self.LIST_ID = params.get( "listId", -1 )
        self.START_BUTTON_ID = params.get( "startButtonId", -1 )
        self.END_BUTTON_ID = params.get( "endButtonId", -1 )
        
# -----------------------------------------------------------------------   


#xbmc.log('Starting Alaska utils') 
#Utils()    
#xbmc.log('Finished Alaska utils') 
    
DIALOGBUTTONMENU_PROPERTY_PREFIX = "AlaskaB.DialogButtonMenu.ListItem_%i."
DIALOGBUTTONMENU_PROPERTY_LABEL = DIALOGBUTTONMENU_PROPERTY_PREFIX + "Label"
DIALOGBUTTONMENU_PROPERTY_VISIBLE = DIALOGBUTTONMENU_PROPERTY_PREFIX + "Visible"
DIALOGBUTTONMENU_PROPERTY_ONCLICK_1 = DIALOGBUTTONMENU_PROPERTY_PREFIX + "OnClick_1"
DIALOGBUTTONMENU_PROPERTY_ONCLICK_2 = DIALOGBUTTONMENU_PROPERTY_PREFIX + "OnClick_2"
    
    
if sys.argv[1] == 'prepareShutdownMenu':
    window = xbmcgui.Window(10111)       
    listItemList = list()
    
    for buttonId in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
        if(xbmc.getCondVisibility("Control.IsVisible(%i)" % buttonId)):
            button = window.getControl(buttonId)
            listItem = xbmcgui.ListItem(label=button.getLabel())
            listItem.setProperty('onClick','Quit()')
            listItem.setProperty('buttonId', str(buttonId))
            listItemList.append(listItem)
            xbmc.log("adding %i" % buttonId)

    list = window.getControl(int(sys.argv[2]))
    list.setStaticContent(listItemList)
    
    #list.reset()
    
    #for buttonId in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
    #    prepareShutdownMenu(window, list, buttonId)

if sys.argv[1] == 'prepareShutdownMenu2':
    window = xbmcgui.Window(10111)       
    listItemList = list()
    
    for index in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
        xbmc.log(str(index))
        xbmc.log(window.getProperty(DIALOGBUTTONMENU_PROPERTY_LABEL % index))
        xbmc.log(window.getProperty(DIALOGBUTTONMENU_PROPERTY_VISIBLE % index))
        xbmc.log(window.getProperty(DIALOGBUTTONMENU_PROPERTY_ONCLICK_1 % index))
        xbmc.log(window.getProperty(DIALOGBUTTONMENU_PROPERTY_ONCLICK_2 % index))
    
        if(xbmc.getCondVisibility(window.getProperty(DIALOGBUTTONMENU_PROPERTY_VISIBLE % index))):
            listItem = xbmcgui.ListItem(label=window.getProperty(DIALOGBUTTONMENU_PROPERTY_LABEL % index))
            listItem.setProperty('onClick1',window.getProperty(DIALOGBUTTONMENU_PROPERTY_ONCLICK_1 % index))
            onClick2 = window.getProperty(DIALOGBUTTONMENU_PROPERTY_ONCLICK_2 % index)
            if onClick2:
              listItem.setProperty('onClick2',onClick2)
            listItemList.append(listItem)
            xbmc.log("adding %i" % index)

    list = window.getControl(int(sys.argv[2]))
    list.setStaticContent(listItemList)

if sys.argv[1] == 'processShutdownMenu':    
    xbmc.log('processShutdownMenu')

if sys.argv[1] == 'prepareContextMenu':
    translationIDs = [ 208, 13347, 586, 14076, 20351, 16103, 16104, 16105, 16106, 16107, 646 ]

    #for buttonId in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        #xbmc.log('      <control type="group">')
        #xbmc.log('        <visible>Control.IsVisible(%i)</visible>' % buttonId)
        
        #for translationID in translationIDs:
          #xbmc.log('        <control type="button" id="%i">' % (buttonId + 1000))
          #xbmc.log('          <include>HiddenControl</include>')
          #xbmc.log('          <label>$LOCALIZE[%i]</label>' % translationID)
          #xbmc.log('          <visible>StringCompare(Control.GetLabel(%i),$LOCALIZE[%i])</visible>' % (buttonId, translationID))
          #xbmc.log('        </control>')

        #xbmc.log('      </control>')

    for buttonId in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        xbmc.log('        <item>')
        xbmc.log('          <label>$INFO[Control.GetLabel(%i)]</label>' % (buttonId + 1000))
        xbmc.log('          <onclick>Control.Message(%i,click)</onclick>' % buttonId)
        xbmc.log('          <visible>Control.IsVisible(%i)</visible>' % (buttonId + 1000))
        xbmc.log('        </item>')
        #xbmc.log('        <item>')
        #xbmc.log('          <label>$INFO[Control.GetLabel(%i)]</label>' % buttonId)
        #xbmc.log('          <onclick>Control.Message(%i,click)</onclick>' % buttonId)
        #xbmc.log('          <visible>!Control.IsVisible(%i)</visible>' % (buttonId + 1000))
        #xbmc.log('        </item>')
        

    #newButton = xbmcgui.ControlButton(-10, -50, 1, 1, 'XX$LOCALIZE[208]')
    #newButton.setVisibleCondition('StringCompare(Control.GetLabel(1001),$LOCALIZE[208])')
    #window.addControl(newButton)
    
    #for buttonId in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        #if(xbmc.getCondVisibility("Control.IsVisible(%i)" % buttonId)):
            #button = window.getControl(buttonId)
            #localizedString = xbmc.getLocalizedString(208)
            #if(localizedString and localizedString == button.getLabel()):
                #xbmc.log("localized string matched %s" % localizedString)
                #xbmc.log("new buttonId %i" % newButton.getId())
            
            #buttonDest = window.getControl(buttonId + 1000)
            #if(buttonDest):
                #xbmc.log("setting button %i label to %s" % (buttonId + 1000, buttonSrc.getLabel()))
                #buttonDest.setLabel(buttonSrc.getLabel())
                #buttonDest.setLabel('PlayXXX')
                #window.setProperty('AlaskaB.DialogContextMenu.Label_%i' % buttonId, '%s-%s' % (buttonSrc.getLabel(), 'X'))
            #else:
                #xbmc.log("not found button %i" % (buttonId + 1000))
            
            #listItem = xbmcgui.ListItem(label=button.getLabel())
            #listItem.setProperty('onClick','Quit()')
            #listItem.setProperty('buttonId', str(buttonId))
            #listItemList.append(listItem)
            #xbmc.log("adding %i" % buttonId)

if sys.argv[1] == 'prepareHome':
  window = xbmcgui.Window(10000)

  # xbmc.log("%s" % xbmc.getInfoLabel('Container(8000).Position'))
  # xbmc.log("%s" % xbmc.getInfoLabel('Container(8000).NumItems'))

  counterStr = window.getProperty('counter')
  if not counterStr or int(counterStr) >= 10:
    counter = 0
  else:
    counter = int(counterStr)

  counter += 1
  counterStr = ('0%d' % counter)[-2:]

  # xbmc.log("%d -> %s" % (counter, counterStr))

  for index in range(0, int(xbmc.getInfoLabel('Container(8000).NumItems'))):
    labelID = xbmc.getInfoLabel('Container(8000).ListItem(%d).Property(labelID)' % index)
    # xbmc.log(labelID)

    propertyName = 'AlaskaB.Home.Background.%s' % labelID
    propertyValue = 'special://skin/media/home/%s/%s.jpg' % (labelID, counterStr)

    window.setProperty(propertyName, propertyValue)
    xbmc.log("%s -> %s" % (propertyName, propertyValue))

  window.setProperty('counter', str(counter))

  


#  xbmc.log(mainMenuListItem.getProperty('labelID'))
#  xbmc.log(mainMenuListItem.getProperty('background'))

def 
