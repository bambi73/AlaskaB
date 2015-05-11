import sys, os, random
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs

HOME_MENU__PROPERTY_PREFIX             = "AlaskaB.Home.Background.%s"
HOME_MENU__PROPERTY_CURRENT_BACKGROUND = HOME_MENU__PROPERTY_PREFIX + ".CurrentBackground"

HOME_MENU__CONTAINER          = "Container(8000)"
HOME_MENU__LIST_ITEM          = HOME_MENU__CONTAINER + ".ListItem(%d)"
HOME_MENU__LIST_ITEM_PROPERTY = HOME_MENU__LIST_ITEM + ".Property(%s)"

# ====-------------------====

def setHomeMenuItemProperty(window, propertyName, propertyValue = None):
  if propertyValue:
    window.setProperty(propertyName, propertyValue)    
  else:
    window.clearProperty(propertyName)    

# ====-------------------====

def getHomeMenuItemProperty(window, propertyName):
  return window.getProperty(propertyName)    

# ====-------------------====

def updateHomeMenuItem(offset):
  backgroundVfs = xbmc.getInfoLabel(HOME_MENU__LIST_ITEM_PROPERTY % (offset, "background"))

  if backgroundVfs and len(backgroundVfs) > 0:
    background = xbmc.translatePath(backgroundVfs).decode('utf-8')

    if os.path.exists(background):
      labelID = xbmc.getInfoLabel(HOME_MENU__LIST_ITEM_PROPERTY % (offset, "labelID"))
      window = xbmcgui.Window(10000)

      if os.path.isdir(background):
        fileList = list()

        for file in os.listdir(background):
          if file.endswith(".jpg") or file.endswith(".png"):
            fileList.append(file)

        if len(fileList) > 0:
          currentFileName = getHomeMenuItemProperty(window, HOME_MENU__PROPERTY_CURRENT_BACKGROUND % labelID)
          fileName = None

          while True:
            fileName = fileList[random.randint(0, len(fileList)-1)]
            if not currentFileName or currentFileName != fileName:
              break

          setHomeMenuItemProperty(window, HOME_MENU__PROPERTY_PREFIX % labelID, os.path.join(background, fileName))
          setHomeMenuItemProperty(window, HOME_MENU__PROPERTY_CURRENT_BACKGROUND % labelID, fileName)
        else:
          setHomeMenuItemProperty(window, HOME_MENU__PROPERTY_PREFIX % labelID)
          setHomeMenuItemProperty(window, HOME_MENU__PROPERTY_CURRENT_BACKGROUND % labelID)
      else:
        setHomeMenuItemProperty(window, HOME_MENU__PROPERTY_PREFIX % labelID, background)
    else:
      xbmc.log("Background directory/file '%s' doesn't exists" % background)

# ====-------------------====

if sys.argv[1] == 'initHomeMenu':
  for offset in range(0, int(xbmc.getInfoLabel(HOME_MENU__CONTAINER + ".NumItems"))):
    updateHomeMenuItem(offset)

# ====-------------------====

if sys.argv[1] == 'updateHomeMenu':
  updateHomeMenuItem(0)

# ====-------------------====
