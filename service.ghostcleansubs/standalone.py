# ============================================================
# KODI Clean Subs - Version 7.0 by D. Lanik (2016)
# ------------------------------------------------------------
# Clean up downloaded subs from ads, etc
# ------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# ============================================================

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os.path

from default import process_subs
from default import getJson

# ============================================================
# Get extension
# ============================================================


def get_extension(filename):
    ext = os.path.splitext(filename)[1][1:].strip()
    return ext

# ============================================================
# Remove prefix
# ============================================================


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[text.startswith(prefix) and len(prefix):]
    else:
        return text

# ============================================================
# Decode file/folder names
# ============================================================


def decodeName(name):
    if type(name) == str:     # leave unicode ones alone
        try:
            name = name.decode('utf8')
        except Exception:
            name = name.decode('windows-1252')

    return name

# ============================================================
# Scan through folders of path(s) found
# ============================================================


def scanPaths(path, intOrder, intPaths, intLevels):
    global __addondir__

    intCancel = 0
    totalFiles = 0

    strMess = __addon__.getLocalizedString(30040)    # Scanning for subtitles
    strMess2 = __addon__.getLocalizedString(30041)   # Scanning folders and cleaning subtitles...
    progress = xbmcgui.DialogProgress()
    progress.create(strMess, strMess2)

    subdirs, files = xbmcvfs.listdir(path)

    intObjects = 0
    for f in files:
        intObjects += 1

    c = 0

    for f in files:
        fileExt = get_extension(f)
        if any(fileExt.lower() in i for i in ("sub", "srt")):
            xbmc.log("CLEANSUBS STANDALONE >> FILE (L1): >>" + f + "<<")

            percent = (c / intObjects) * 100
            message1 = "Path: " + path + " (" + str(intOrder) + " of " + str(intPaths) + ")"
            message2 = "Subfolder: " + f
            message3 = "Objects: " + str(c) + " of " + str(int(intObjects)) + " ( " + str(int(percent)) + "% )"
            progress.update(int(percent), decodeName(message1), decodeName(message2), str(message3))
            if progress.iscanceled():
                intCancel = 1
                break

            totalFiles += 1
            success = xbmcvfs.copy(os.path.join(path, f), os.path.join(xbmc.translatePath("special://temp"), f))
            if success:
                try:
                    process_subs(os.path.join(xbmc.translatePath("special://temp"), f), 1)
                    xbmcvfs.rename(os.path.join(path, f), os.path.join(path, f + "_ORIGINAL"))
                    success = xbmcvfs.copy(os.path.join(xbmc.translatePath("special://temp"), f), os.path.join(path, f))
                    xbmcvfs.delete(os.path.join(xbmc.translatePath("special://temp"), f))
                    xbmcvfs.delete(os.path.join(xbmc.translatePath("special://temp"), f + "_ORIGINAL"))
                except Exception as e:
                    xbmc.log("CLEANSUBS STANDALONE >> ERROR: >>" + e.message + "<<")
        c += 1

    c = 0

    intObjects = 0
    for f in subdirs:
        intObjects += 1

    for f in subdirs:
        xbmc.log("CLEANSUBS STANDALONE >> FOLDER (L1): >>" + f + "<<")

        percent = (c / intObjects) * 100
        message1 = "Path: " + path + " (" + str(intOrder) + " of " + str(intPaths) + ")"
        message2 = "Subfolder: " + f
        message3 = "Objects: " + str(c) + " of " + str(int(intObjects)) + " ( " + str(int(percent)) + "% )"
        progress.update(int(percent), decodeName(message1), decodeName(message2), str(message3))
        if progress.iscanceled():
            intCancel = 1
            break

        subdirs2, files2 = xbmcvfs.listdir(os.path.join(path, f))
        for f2 in files2:
            fileExt = get_extension(f2)
            if any(fileExt.lower() in i for i in ("sub", "srt")):
                xbmc.log("CLEANSUBS STANDALONE >> FILE (L2): >>" + f2 + "<<")
                totalFiles += 1
                success = xbmcvfs.copy(os.path.join(path, f, f2), os.path.join(xbmc.translatePath("special://temp"), f2))
                if success:
                    process_subs(os.path.join(xbmc.translatePath("special://temp"), f2), 1)
                    xbmcvfs.rename(os.path.join(path, f, f2), os.path.join(path, f, f2 + "_ORIGINAL"))
                    success = xbmcvfs.copy(os.path.join(xbmc.translatePath("special://temp"), f2), os.path.join(path, f, f2))
                    xbmcvfs.delete(os.path.join(xbmc.translatePath("special://temp"), f2))
                    xbmcvfs.delete(os.path.join(xbmc.translatePath("special://temp"), f2 + "_ORIGINAL"))
        c += 1

    progress.close()
    xbmc.log("CLEANSUBS STANDALONE >> TOTAL SUB FILES: >>" + str(totalFiles) + "<<")

    return intCancel

# ============================================================
# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
# ============================================================


__addon__ = xbmcaddon.Addon(id='service.ghostcleansubs')
__addonwd__ = xbmc.translatePath(__addon__.getAddonInfo('path'))
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')

sqlite_file = os.path.join(__addondir__, 'cleansubs.sqlite')
paths = []

if __name__ == '__main__':
    xbmc.log("CLEANSUBS STANDALONE >> STARTED VERSION %s" % (__version__))
    machineID = __addon__.getSetting('ID')
    manFolder = __addon__.getSetting('folder')

    # get paths from KODI sources configuration
    paths = getJson("Files.GetSources", "media", "video", "sources")

    for i, jj in enumerate(paths[:]):
        if jj["file"][:6] == "pvr://":
            del paths[i]

    for i, jj in enumerate(paths[:]):
        paths[i] = jj["file"]

    pathsNr = len(paths)

    for jj in paths:
        xbmc.log("CLEANSUBS >> VIDEO PATHS >> " + jj)

    actions = []
    strMess = __addon__.getLocalizedString(30063)    # Video libraries
    strMess2 = __addon__.getLocalizedString(30064)    # found
    actions.append(strMess + " (" + str(pathsNr) + ") " + strMess2)

    if manFolder == '':
        strMess2 = __addon__.getLocalizedString(30062)    # not set
    else:
        strMess2 = manFolder

    strMess = __addon__.getLocalizedString(30061)    # Arbitrary folder
    actions.append(strMess + " (" + strMess2 + ")")

    strMess = __addon__.getLocalizedString(30060)    # Settings
    actions.append(strMess)

    dialog = xbmcgui.Dialog()
    strMess = __addon__.getLocalizedString(30030)    # Choose what to scan:
    mode = xbmcgui.Dialog().select(strMess, actions)
    intCancel = 0

    if(mode != -1):
        if(mode == 0):
            if pathsNr > 0:
                strMess = __addon__.getLocalizedString(30031)     # Scan and clean subtitle files in [COLOR red]video libraries[/COLOR]?
                strMess2 = __addon__.getLocalizedString(30035)    # Start scan
                i = dialog.yesno(strMess2, strMess)
                if i == 1:
                    for g, path in enumerate(paths, 1):
                        intCancel = scanPaths(path, g, pathsNr, 3)
                        if intCancel == 1 or intCancel == 2:
                            break
                else:
                    intCancel = 1
            else:
                strMess = __addon__.getLocalizedString(30033)     # No [COLOR red]video libraries[/COLOR] found!
                strMess2 = __addon__.getLocalizedString(30036)    # Error
                i = dialog.ok(strMess2, strMess)
                intCancel = 1
        elif(mode == 1):
            if manFolder != '' and xbmcvfs.exists(manFolder):
                strMess = __addon__.getLocalizedString(30032) + "\n(" + manFolder + ")"    # Scan and clean subtitle files in [COLOR red]arbitrary folder[/COLOR]:
                strMess2 = __addon__.getLocalizedString(30035)    # Start scan
                i = dialog.yesno(strMess2, strMess)

                if i == 1:
                    intCancel = scanPaths(manFolder, 1, 1, 3)
                else:
                    intCancel = 1
            else:
                strMess = __addon__.getLocalizedString(30034)     # [COLOR red]Arbitrary folder[/COLOR] not found or not set!
                strMess2 = __addon__.getLocalizedString(30036)    # Error
                i = dialog.ok(strMess2, strMess)
                __addon__.openSettings()
                intCancel = 1
        elif(mode == 2):
            __addon__.openSettings()
            intCancel = 3
    else:
        intCancel = 1

    if intCancel == 1:
        strMess = __addon__.getLocalizedString(30050)     # Subtitles cleanup [COLOR red]interrupted[/COLOR].
        xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)" % (__addonname__, strMess, __addon__.getAddonInfo('icon')))
    elif intCancel == 2:
        strMess = __addon__.getLocalizedString(30052)     # NFS paths are [COLOR red]not supported[/COLOR], please use NFS paths at System (OS) level!
        xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)" % (__addonname__, strMess, __addon__.getAddonInfo('icon')))
    elif intCancel == 3:
        pass
    else:
        strMess = __addon__.getLocalizedString(30051)     # Subtitles cleanup [COLOR red]done[/COLOR].
        xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)" % (__addonname__, strMess, __addon__.getAddonInfo('icon')))

    xbmc.log("CLEANSUBS STANDALONE >> FINISHED")

# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
