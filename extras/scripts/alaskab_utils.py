import sys, os, random, hashlib
import xml.etree.ElementTree as xmltree

import xbmc, xbmcgui, xbmcvfs

HOME_MENU__PROPERTY_PREFIX             = "AlaskaB.Home.Background.%s"
HOME_MENU__PROPERTY_CURRENT_BACKGROUND = HOME_MENU__PROPERTY_PREFIX + ".CurrentBackground"

HOME_MENU__CONTAINER          = "Container(8000)"
HOME_MENU__LIST_ITEM          = HOME_MENU__CONTAINER + ".ListItem(%d)"
HOME_MENU__LIST_ITEM_PROPERTY = HOME_MENU__LIST_ITEM + ".Property(%s)"

__includepath__   = xbmc.translatePath("special://skin/16x9/script-skinshortcuts-includes.xml").decode("utf-8")
__hashfilepath__ = xbmc.translatePath("special://masterprofile/addon_data/script.skinshortcuts/skin.alaskab.hash").decode('utf-8')

# ====-------------------====

def updateSkinshortcutsIncludeHash():
  try:
    hashList = eval(xbmcvfs.File(__hashfilepath__).read())
  except:
    return        

  for hash in hashList:
    if hash[0] == __includepath__:
      hasher = hashlib.md5()
      hasher.update(xbmcvfs.File(__includepath__).read())
      hash[1] = hasher.hexdigest()
      
  file = xbmcvfs.File(__hashfilepath__, "w")
  file.write(repr(hashList))
  file.close
    
# ====-------------------====

def updateSkinshortcutsInclude():
  modified = False
  
  includePath = xbmc.translatePath("special://skin/16x9/script-skinshortcuts-includes.xml").decode("utf-8")
  includeTree = xmltree.parse(includePath)
  
  for include in includeTree.findall("include"):
    includeName = include.get("name")
    if includeName and includeName == "skinshortcuts-mainmenu":
      for item in include.findall("item"):
        labelIDProperty = None
        backgroundProperty = None
        backgroundPropertyProperty = None
        
        for property in item.findall("property"):
          propertyName = property.get("name")
          if propertyName == "labelID":
            labelIDProperty = property
          elif propertyName == "background":
            backgroundProperty = property
          elif propertyName == "backgroundProperty":
            backgroundPropertyProperty = property

        if labelIDProperty is not None and labelIDProperty.text and backgroundProperty is not None and backgroundProperty.text:
          labelID = labelIDProperty.text
          if labelID.isdigit():
            labelIDTranslation = xbmc.getLocalizedString(int(labelID))
            if labelIDTranslation:
              labelID = labelIDTranslation
        
          backgroundPropertyInfoLabel = "$INFO[Window(Home).Property(AlaskaB.Home.Background.%s)]" % labelID
          
          if backgroundPropertyProperty is not None and backgroundPropertyProperty.text:
            if backgroundPropertyInfoLabel.lower() != backgroundPropertyProperty.text.lower():
              xbmc.log("  backgroundProperty changed: %s --> %s" % (backgroundPropertyProperty.text, backgroundPropertyInfoLabel))
              backgroundPropertyProperty.text = backgroundPropertyInfoLabel
              modified = True
          else:
            xbmc.log("  backgroundProperty not exist, adding: %s" % backgroundPropertyInfoLabel)
            backgroundPropertyProperty = xmltree.Element("property")
            backgroundPropertyProperty.set("name", "backgroundProperty")
            backgroundPropertyProperty.text = backgroundPropertyInfoLabel
            item.append(backgroundPropertyProperty)
            modified = True
            
  if modified:
    xbmc.log("XML modified, writing to file")
    includeTree.write(includePath)
    updateSkinshortcutsIncludeHash()
    xbmc.executebuiltin("ReloadSkin()")

        
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

  # xbmc.log("backgroundVfs: %s" % backgroundVfs)

  if backgroundVfs and len(backgroundVfs) > 0:
    background = xbmc.translatePath(backgroundVfs).decode('utf-8')

    if os.path.exists(background):
      labelID = xbmc.getInfoLabel(HOME_MENU__LIST_ITEM_PROPERTY % (offset, "labelID"))
      window = xbmcgui.Window(10000)

#      xbmc.log("labelID: %s" % labelID)

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

#          xbmc.log("fileName: %s" % fileName)
#          xbmc.log("HOME_MENU__PROPERTY_PREFIX: %s" % (HOME_MENU__PROPERTY_PREFIX % labelID))

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
  homeMenuItemCount = xbmc.getInfoLabel(HOME_MENU__CONTAINER + ".NumItems")
  if homeMenuItemCount:
    for offset in range(0, int(homeMenuItemCount)):
      updateHomeMenuItem(offset)

# ====-------------------====

if sys.argv[1] == 'updateHomeMenu':
  updateHomeMenuItem(0)

# ====-------------------====

if sys.argv[1] == 'updateSkinshortcutsInclude':
  xbmc.executebuiltin("RunScript(script.skinshortcuts,%s)" % sys.argv[2])
  xbmc.sleep(1000)

  while (not xbmc.abortRequested) and xbmcgui.Window(10000).getProperty("skinshortcuts-isrunning") == "True":
    xbmc.sleep(100)
  
  updateSkinshortcutsInclude()

# ====-------------------====
