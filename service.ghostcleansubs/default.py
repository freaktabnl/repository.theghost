# ============================================================
# KODI Clean Subs - Version 7.0 by D. Lanik (2016)
# ------------------------------------------------------------
# Clean up downloaded subs from ads, etc
# ------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# ============================================================

import xbmc
import time
import xbmcaddon
import xbmcgui
import os.path
import urllib.request, urllib.error, urllib.parse
import codecs
import stat
import sqlite3
import hashlib
import uuid
import os
import re
import xbmcvfs
from shutil import copyfile
from threading import Timer
from xml.dom import minidom
import pipes
import json
import itertools
from distutils.util import strtobool
from lib.srt2ass import srt2ass

# ============================================================
# Check if string is valid hex color code
# ============================================================


def validColor(code):
    if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', code):
        return True
    else:
        return False

# ============================================================
# Define Settings Monitor Class
# ============================================================


class SettingMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        GetSettings(1)


# ============================================================
# Get settings
# ============================================================


def GetSettings(par1):
    global __addon__
    global __addonname__
    global booOn
    global booInfo
    global booLogo
    global manFolder
    global booCustom
    global booRemoveCC
    global intMethod
    global intHerlines
    global Charset
    global Languages
    global SubFirst
    global REM
    global booDelOrigSub
    global booRemoveTags
    global booBlackBar
    global saaTextColor

    errors = False
    __addon__ = xbmcaddon.Addon(id='service.ghostcleansubs')

    booOn = bool(strtobool(str(__addon__.getSetting('on').title())))
    booInfo = bool(strtobool(str(__addon__.getSetting('info').title())))
    booLogo = bool(strtobool(str(__addon__.getSetting('logo').title())))
    manFolder = __addon__.getSetting('folder')
    booCustom = bool(strtobool(str(__addon__.getSetting('custdef').title())))
    booRemoveCC = __addon__.getSetting('removecc').title()
    intMethod = int(__addon__.getSetting('method'))
    intHerlines = int(float(__addon__.getSetting('herlines')))
    booDelOrigSub = bool(strtobool(str(__addon__.getSetting('delorigsub').title())))
    booRemoveTags = bool(strtobool(str(__addon__.getSetting('removetags').title())))
    booBlackBar = bool(strtobool(str(__addon__.getSetting('blackbar').title())))

    txtColor = __addon__.getSetting('blackbar_textcolor')

    if txtColor[0] != "#":
        txtColor = "#" + txtColor
        __addon__.setSetting("blackbar_textcolor", txtColor)

    hBB = txtColor[1:3]
    hGG = txtColor[3:5]
    hRR = txtColor[5:7]
    saaTextColor = hRR + hGG + hBB

    SubFirst = getJson("Settings.GetSettingValue", "setting", "subtitles.downloadfirst", "value")
    Charset = getJson("Settings.GetSettingValue", "setting", "subtitles.charset", "value")
    Lang = getJson("Settings.GetSettingValue", "setting", "subtitles.languages", "value")

    xbmc.log('CLEANSUBS >> SETTING ON >> ' + str(booOn))
    xbmc.log('CLEANSUBS >> SETTING INFO >> ' + str(booInfo))
    xbmc.log('CLEANSUBS >> SETTING LOGO >> ' + str(booLogo))
    xbmc.log('CLEANSUBS >> SETTING FOLDER >> ' + manFolder)
    xbmc.log('CLEANSUBS >> SETTING CUSTOM DEF >> ' + str(booCustom))
    xbmc.log('CLEANSUBS >> SETTING REMOVE CC >> ' + booRemoveCC)
    xbmc.log('CLEANSUBS >> SETTING REMOVE TAGS >> ' + str(booRemoveTags))
    xbmc.log('CLEANSUBS >> SETTING SUBS BACKGROUND >> ' + str(booBlackBar))

    if not validColor('#' + saaTextColor):
        errstr = "Text color has no valid hex code: " + str(saaTextColor)
        xbmc.log("CLEANSUBS >> " + errstr.upper())
        errors = True
    else:
        xbmc.log('CLEANSUBS >> SETTING SUBS BACKGROUND TXT COLOR >> ' + saaTextColor)

    xbmc.log('CLEANSUBS >> SETTING METHOD >> ' + str(intMethod))
    xbmc.log('CLEANSUBS >> SETTING HEURISTICS LINES NR >> ' + str(intHerlines))
    xbmc.log('CLEANSUBS >> SETTING DELETE ORIGINAL SUBS >> ' + str(booDelOrigSub))

    xbmc.log('CLEANSUBS >> SETTING SUBFIRST >> ' + str(SubFirst))
    xbmc.log('CLEANSUBS >> SETTING CHARSET >> ' + str(Charset))

    for i, la in enumerate(Lang):
        Lang[i] = Lang[i].upper()

    Languages = []
    foundSH = False

    for la in Lang:
        if la == "SERBIAN" or la == "CROATIAN" or la == "SERBO-CROATIAN" or la == "BOSNIAN":
            foundSH = True
        else:
            Languages.append(la.upper())

    if foundSH:
        Languages.append("SERBO-CROATIAN")

    Languages.append("GENERIC")

    for la in Languages:
        xbmc.log("CLEANSUBS >> SETTING SUB LANGUAGES: >>" + la + "<<")

    REM = readDefinitions()

    if errors and par1 == 1:
        dialog = xbmcgui.Dialog()
        dialog.ok(__addonname__, errstr)
        __addon__.openSettings()

# ============================================================
# Define Overlay Class
# ============================================================


class OverlayText(object):
    def __init__(self, windowid):
        self.showing = False
        self.window = xbmcgui.Window(windowid)
        viewport_w, viewport_h = self._get_skin_resolution()

        pos = "-150,40".split(",")
        pos_x = (viewport_w + int(pos[0]), int(pos[0]))[int(pos[0]) > 0]
        pos_y = (viewport_h + int(pos[1]), int(pos[1]))[int(pos[1]) > 0]
        self.imgsubsok = xbmcgui.ControlImage(pos_x, pos_y, 140, 160, os.path.join("media", "OK01.png"), aspectRatio=2)

        pos = "-570,40".split(",")
        pos_x = (viewport_w + int(pos[0]), int(pos[0]))[int(pos[0]) > 0]
        pos_y = (viewport_h + int(pos[1]), int(pos[1]))[int(pos[1]) > 0]
        self.imgsubsprovider = xbmcgui.ControlImage(pos_x, pos_y, 566, 100, os.path.join("media", "subs_titlovi_com.png"), aspectRatio=2)

        pos = "-155,200,140,20".split(",")
        pos_x = (viewport_w + int(pos[0]), int(pos[0]))[int(pos[0]) > 0]
        pos_y = (viewport_h + int(pos[1]), int(pos[1]))[int(pos[1]) > 0]
        self.txtsubsok = xbmcgui.ControlLabel(pos_x, pos_y, int(pos[2]), int(pos[3]), "CLEANED!", font='font12', textColor='0xFFFFFFFF', alignment=int(1))

        pos = "-374,10,260,20".split(",")
        pos_x = (viewport_w + int(pos[0]), int(pos[0]))[int(pos[0]) > 0]
        pos_y = (viewport_h + int(pos[1]), int(pos[1]))[int(pos[1]) > 0]
        self.txtsubsprovider = xbmcgui.ControlLabel(pos_x, pos_y, int(pos[2]), int(pos[3]), "SUBTITLES PROVIDED BY", font='font10', textColor='0xFFFFFFFF', alignment=int(1))

    def show(self):
        self.showing = True
        self.window.addControl(self.imgsubsok)
        self.window.addControl(self.imgsubsprovider)
        self.window.addControl(self.txtsubsok)
        self.window.addControl(self.txtsubsprovider)

    def hide(self):
        self.showing = False
        self.window.removeControl(self.imgsubsok)
        self.window.removeControl(self.imgsubsprovider)
        self.window.removeControl(self.txtsubsok)
        self.window.removeControl(self.txtsubsprovider)

    def _close(self):
        if self.showing:
            self.hide()
        else:
            pass
        try:
            self.window.clearProperties()
        except Exception:
            pass

# ============================================================
# Get resolution
# ============================================================

    def _get_skin_resolution(self):
        xmlFile = os.path.join(xbmc.translatePath("special://skin/"), "addon.xml")
        xmldoc = minidom.parse(xmlFile)

        res = xmldoc.getElementsByTagName("res")
        xval = int(res[0].attributes["width"].value)
        yval = int(res[0].attributes["height"].value)

        return(xval, yval)

# ============================================================
# Define Subtitle Class
# ============================================================


class Subtitle():
    def __init__(self, index, timing, text, utext):
        self.index = index
        self.timing = timing
        self.text = text
        self.utext = utext

    def __repr__(self):
        return "%s %s %s %s" % (self.index, self.timing, self.text, self.utext)

    def __str__(self):
        return "%s %s %s %s" % (self.index, self.timing, self.text, self.text)

# ============================================================
# Remove CC and attributes from subs
# ============================================================


def remove_cc(text, brackets="()[]"):
    count = [0] * (len(brackets) // 2)                   # count open/close brackets
    saved_chars = []

    for character in text:
        for i, b in enumerate(brackets):
            if character == b:                           # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close            # `+1`: open, `-1`: close
                if count[kind] < 0:                      # unbalanced bracket
                    count[kind] = 0
                break
        else:                                            # character is not a bracket
            if not any(count):                           # outside brackets
                saved_chars.append(character)

    return ''.join(saved_chars)

# ============================================================
# Process subtitles - SRT and SUB format
# ============================================================


def process_subs(fileName, iMode):
    global player
    global __addon__
    global __addondir__
    global Charset
    global intMethod
    global sqlite_file
    global machineID
    global REM
    global subProviderLogo
    global intHerlines
    global booDelOrigSub
    global booRemoveCC
    global booRemoveTags
    global booBlackBar
    global saaTextColor

    start = time.time()

    originalfileName = None
    if fileName[:4] == "smb:":
        osWin = xbmc.getCondVisibility('System.Platform.Windows')
        if not osWin:
            originalfileName = fileName
            fileName = os.path.join(xbmc.translatePath("special://temp"), os.path.basename(fileName))
            xbmcvfs.copy(originalfileName, fileName)

    linepos = 0
    sublen = 0
    halflen = 0

    intMethod = int(__addon__.getSetting('method'))

    SubExt = os.path.splitext(fileName)[1][1:].strip()

    # turn off subtitles while we proccess them...
    xbmc.Player().showSubtitles(False)

    # check the file encoding
    try:
        file_stream = codecs.open(fileName, 'r')
        file_stream.close()
    except Exception:
        xbmc.log('CLEANSUBS >> PRE ENC >> CAN NOT OPEN SUBS!!!')

    SubCharset = ''
    encodings = ['utf-8', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp932']
    for e in encodings:
        try:
            file_stream = codecs.open(fileName, 'r', encoding=e)
            file_stream.readlines()
            file_stream.seek(0)
        except UnicodeDecodeError:
            xbmc.log('CLEANSUBS >> ENC >> TRYING ENCODING %s' % e)
            file_stream.close()
        except Exception:
            xbmc.log('CLEANSUBS >> ENC >> ERROR')
            SubCharset = ''

            try:
                if file_stream is not None:
                    file_stream.close()
            except Exception:
                pass
        else:
            xbmc.log('CLEANSUBS >> ENC >> OPENED WITH ENCODING: %s' % e)
            file_stream.close()
            SubCharset = e
            break

    if SubCharset == '':
        xbmc.log('CLEANSUBS >> ENC >> OPENED WITH KODI ENCODING: %s' % Charset)
        SubCharset = Charset

    line = ''
    SubNum = ''
    SubTime = ''
    SubText = ''
    subsSrt = []

    file_input = codecs.open(fileName, 'r', SubCharset, errors='ignore')

    # subtitles in SRT format
    if SubExt == "srt":
        # loop over file, parse lines
        while True:
            # read first line
            line = file_input.readline().strip()

            # fix (strip) encoding that might be in 1st line
            if len(line) == 4 and line[-1:] == "1" and not subsSrt:
                line = "1"

            # exit when there are no more lines
            if not line:
                break

            # parse lines
            while True:
                # this is index number
                if line.isdigit():
                    SubNum = line.strip()
                # this is timing
                elif " --> " in line:
                    SubTime = line.strip()
                # empty line, that means end of a block
                elif line == '':
                    # remove last linebreak
                    if SubText[-1:] == "\n":
                        SubText = SubText[:-1]
                    # save data to list
                    subsSrt.append(Subtitle(SubNum, SubTime, SubText, SubText.upper()))
                    SubText = ''
                    break
                # so this must be text
                else:
                    SubText = SubText + line.strip() + '\n'

                # read next line
                line = file_input.readline().strip()
    # subtitles in SUB format
    elif SubExt == "sub":
        # loop over file, parse lines
        while True:
            # read line
            line = file_input.readline().strip()

            # exit when there are no more lines
            if not line:
                break

            groups = line.split('}')
            SubTime = '}'.join(groups[:2]) + '}'
            SubText = '}'.join(groups[2:])
            subsSrt.append(Subtitle('1', SubTime, SubText, SubText.upper()))

    file_input.close()

    intRemoved = 0

    sublen = len(subsSrt) + 1
    halflen = sublen / 2

    # now clean the lines with definitions
    if intMethod == 0 or intMethod == 2:
        filtered_list = []

        for i, line in enumerate(subsSrt, 1):
            if i < halflen:
                linepos = i
            else:
                linepos = (sublen - i) * -1

            removed = False

            for item in REM:
                if item in line.utext:
                    removed = True
                    break

            if not removed:
                filtered_list.append(Subtitle(line.index, line.timing, line.text, line.utext))

        intRemoved = len(subsSrt) - len(filtered_list)
        subsSrt = []
        subsSrt = filtered_list[:]
        sublen = len(subsSrt) + 1
        halflen = sublen / 2

    # now clean the lines with heuristics
    if intMethod == 0 or intMethod == 1:
        hList = GetHeuristic()

        for i, line in enumerate(subsSrt[:]):
            j = i + 1
            if j < halflen:
                linepos = j
            else:
                linepos = (sublen - j) * -1

            for x in hList:
                subsPos = line.text.lower().find(x)
                if subsPos != -1:
                    if x[0] == '.':    # do not clean this
                        try:
                            if not line.text[subsPos - 1].isalnum():
                                continue
                        except Exception:
                            pass
                    elif x[0] == '@':    # do not clean this
                        try:
                            if not line.text[subsPos - 1].isalnum() or not line.text[subsPos + 1].isalnum():
                                continue
                        except Exception:
                            pass

                    # clean this
                    if i < intHerlines or i > (len(subsSrt[:]) - (intHerlines + 1)):
                        subsSrt.remove(line)
                        intRemoved += 1
                        break

    # remove CC, TAGS
    if booRemoveCC and booRemoveTags:                   # remove CC and remove tags
        strBrackets = "()[]<>"
    elif booRemoveCC:                                   # remove CC
        strBrackets = "()[]"
    elif booRemoveTags:                                 # remove tags
        strBrackets = "<>"

    # now clean the lines, CC and/or tags
    if booRemoveCC or booRemoveTags:
        filtered_list = []

        for i, line in enumerate(subsSrt, 1):
            if any(item in line.text for item in ['(', '[', '<']):
                intRemoved += 1
                text = remove_cc(line.text, brackets=strBrackets).strip()
                while "  " in text:
                    text = text.replace("  ", " ")
                if text != "" and text != "-":
                    filtered_list.append(Subtitle(line.index, line.timing, text, ""))
            else:
                filtered_list.append(Subtitle(line.index, line.timing, line.text, ""))

        subsSrt = []
        subsSrt = filtered_list[:]

    if intRemoved == 0:    # did we remove any lines? if not, no need to save anything...
        end = time.time()
        xbmc.log('CLEANSUBS >> PROCESSED IN %0.2f SECONDS, NO LINES REMOVED' % (end - start))
        return

    # subtitles in SRT format - no need to reindex SUB format since it has no index :)
    if SubExt == "srt":
        for i, line in enumerate(subsSrt, 1):    # reindex the lines
            subsSrt[i - 1].index = str(i)

    # now write out list to file
    file_output = codecs.open(fileName + "_W", 'w', 'utf8')
    for item in subsSrt:
        # subtitles in SRT format
        if SubExt == "srt":
            file_output.write("%s\n" % item.index)
            file_output.write("%s\n" % item.timing)
            file_output.write("%s\n\n" % item.text)
        # subtitles in SUB format
        elif SubExt == "sub":
            file_output.write("%s %s\n" % (item.timing, item.text))

    file_output.close()

    if booBlackBar:                                          # convert to ass
        if SubExt == "srt":
            fileName = srt2ass(fileName + "_W", saaTextColor)

            if originalfileName:          # this means smb path was used, file was processed in temp, so we need to copy the file back to smb
                success = xbmcvfs.copy(fileName, originalfileName + "_W")
                fileName = originalfileName
    else:
        if originalfileName:          # this means smb path was used, file was processed in temp, so we need to copy the file back to smb
            success = xbmcvfs.copy(fileName + "_W", originalfileName + "_W")
            fileName = originalfileName

    if iMode == 0:                # delete original file, rename modified file to original filename
        try:
            xbmcvfs.delete(fileName)
        except Exception:
            xbmc.log("CLEANSUBS >> COULDN'T DELETE ORIG SUBS - TRYING READ ONLY")
            try:
                os.chmod(remFile, stat.S_IWRITE)
                os.remove(fileName)
            except Exception:
                xbmc.log("CLEANSUBS >> COULDN'T DELETE ORIG SUBS!!!")

        try:
            xbmcvfs.rename(fileName + "_W", fileName)
        except Exception:
            xbmc.log("CLEANSUBS >> COULDN'T RENAME TEMP SUBS")

        player.setSubtitles(fileName)         # turn on subtitles
    else:                  # rename original file
        if booDelOrigSub:
            try:
                xbmcvfs.delete(fileName)
            except Exception:
                xbmc.log("CLEANSUBS >> COULDN'T DELETE ORIGINAL SUBS")
        else:
            if xbmcvfs.exists(fileName + "_ORIGINAL"):
                try:
                    xbmcvfs.delete(fileName + "_ORIGINAL")
                except Exception:
                    xbmc.log("CLEANSUBS >> COULDN'T DELETE ORIGINAL SUBS")

            try:
                xbmcvfs.rename(fileName, fileName + "_ORIGINAL")
            except Exception:
                xbmc.log("CLEANSUBS >> COULDN'T RENAME ORIGINAL SUBS")

        xbmcvfs.rename(fileName + "_W", fileName)

    end = time.time()
    xbmc.log('CLEANSUBS >> PROCESSED IN %0.2f SECONDS, REMOVED %d LINES' % (end - start, intRemoved))

# ============================================================
# Get timestamp
# ============================================================


def TimestampMillisec64():
    return int(round(time.time() * 1000))

# ============================================================
# Get Kodi settings
# ============================================================


def getJson(method, param1, param2, retname):
    command = '''{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "%s",
    "params": {
        "%s": "%s"
        }
    }'''

    result = xbmc.executeJSONRPC(command % (method, param1, param2))
    py = json.loads(result)
    if 'result' in py and retname in py['result']:
        a = py['result'][retname]
        return a
    else:
        return False

# ============================================================
# Download definitions file
# ============================================================


def getDefinitions():
    global __addondir__
    global __addonwd__
    global __addon__
    global machineID
    global Languages

    fileNameLocal = os.path.join(__addondir__, 'cleanupstrings.txt')
    fileNamePlugin = os.path.join(__addonwd__, 'cleanupstrings.txt')

    localLen = 0
    remoteLen = 0

    returnVal = 0

    if os.path.isfile(fileNameLocal):             # we have local definitions
        localLen = int(os.stat(fileNameLocal).st_size)
        returnVal = 1
    else:                                         # this shouldn't ever happen!
        if os.path.isfile(fileNamePlugin):        # so copy the copy of definitions from plugin folder
            try:
                copyfile(fileNamePlugin, fileNameLocal)
                returnVal = 1
            except Exception:
                xbmc.log("CLEANSUBS >> DEFINITIONS >> LOCAL COPY ERROR2")
                returnVal = 0

            if os.path.isfile(fileNameLocal):
                localLen = int(os.stat(fileNameLocal).st_size)
                returnVal = 1
                xbmc.log("CLEANSUBS >> DEFINITIONS >> COPIED LOCALY")
            else:
                xbmc.log("CLEANSUBS >> DEFINITIONS >> LOCAL COPY ERROR1")
                returnVal = 0
        else:                                      # and this is also unbeliveable, but let's prepare for any eventuality
            xbmc.log("CLEANSUBS >> DEFINITIONS >> NO LOCAL DEFINITIONS FILE IN PLUGIN FOLDER???")
            returnVal = 0

    deffile = "http://kodi.lanik.org/service.cleansubs/cleanupstrings.txt"

    try:
        fileNameRemote = urllib.request.urlopen(deffile)
    except Exception:
        xbmc.log("CLEANSUBS >> DEFINITIONS >> NO REMOTE FILE1: " + deffile)

    fileNameLocalTemp = os.path.join(__addondir__, 'cleanupstrings.new')

    try:
        remoteLen = int(fileNameRemote.info()['Content-Length'])
    except Exception:
        xbmc.log("CLEANSUBS >> DEFINITIONS >> NO REMOTE FILE1: " + deffile)

    if remoteLen != 0:
        if remoteLen != localLen:
            xbmc.log("CLEANSUBS >> DEFINITIONS >> TO DOWNLOAD (L:" + str(localLen) + " != R:" + str(remoteLen) + ")")
            try:
                with open(fileNameLocalTemp, 'wb') as output:
                    output.write(fileNameRemote.read())

                if os.path.isfile(fileNameLocal):
                    os.remove(fileNameLocal)
                os.rename(fileNameLocalTemp, fileNameLocal)

                xbmc.log('CLEANSUBS >> DEFINITIONS >> DOWNLOADED : ' + deffile)
                returnVal = 2
            except Exception:
                xbmc.log("CLEANSUBS >> DEFINITIONS >> DOWNLOAD ERROR: " + deffile)
        else:
            xbmc.log("CLEANSUBS >> DEFINITIONS >> NO NEW DEFINITIONS (L:" + str(localLen) + " == R:" + str(remoteLen) + ")")

    else:
        xbmc.log("CLEANSUBS >> DEFINITIONS >> NO REMOTE FILE2: " + deffile)

    return returnVal

# ============================================================
# Write definitions file into DB
# ============================================================


def writeDefinitions():
    global __addondir__
    global sqlite_file

    ActWin = xbmcgui.getCurrentWindowId()

    if ActWin != 12005:
        progress = xbmcgui.DialogProgressBG()
        strMess = "CleanSubs"
        strMess2 = ". / ."
        progress.create(strMess, strMess2)

    fileNameLocal = os.path.join(__addondir__, 'cleanupstrings.txt')

    if os.path.isfile(fileNameLocal):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        try:
            c.execute("DROP TABLE IF EXISTS definitions")
            c.execute('CREATE TABLE {tn} ({cn} {ft})'
                      .format(tn='definitions', cn='definition', ft='TEXT'))

            c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                      .format(tn='definitions', cn='language', ct='TEXT'))

            conn.commit()

            xbmc.log("CLEANSUBS >> DELETED AND CREATED NEW DEF DB")
        except Exception as e:
            xbmc.log("CLEANSUBS >> SQL ERROR IN MakeDatabase (DEFS) : " + str(e))

        # read cleanup definitions to database
        p = os.path.join(__addondir__, 'cleanupstrings.txt')
        intObjects = sum(1 for line in open(p, encoding='utf8')) + 0.1

        fp = codecs.open(p, "rb", "utf-8")
        for i, line in enumerate(fp):
            if ActWin != 12005:
                percent = (i / intObjects) * 100
                strMess2 = str(int(i)) + " / " + str(int(intObjects))
                progress.update(int(percent), str(strMess), str(strMess2))

            if i == 0:
                ts = line[1:].upper()
            else:
                ts = line.upper()

            text = ts[:60]

            if text == "____________________________________________________________":
                language = ts[60:].strip()
            else:
                definition = ts.strip()

                try:
                    data = (definition, language)
                    c.execute("INSERT INTO definitions VALUES(?, ?)", data)
                except Exception as e:
                    xbmc.log("CLEANSUBS >> SQL ERROR IN getDefinitions : " + str(e))

        xbmc.log('CLEANSUBS >> WROTE TOTAL DEFINITIONS TO DB: ' + str(i) + ' elements')

        conn.commit()
        conn.close()

    if ActWin != 12005:
        progress.close()

# ============================================================
# Read definitions file from DB
# ============================================================


def readDefinitions():
    global __addon__
    global booCustom
    global sqlite_file

    rrr = []

    booCustom = bool(strtobool(str(__addon__.getSetting('custdef').title())))

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    if booCustom:
        AllLang = GetAllLanguages()

        for lang in Languages:
            if lang in AllLang:
                c.execute("SELECT definition FROM definitions WHERE language='%s'" % lang)
                rrr = rrr + list(itertools.chain.from_iterable(c))
    else:
        c.execute("SELECT definition FROM definitions")
        rrr = list(itertools.chain.from_iterable(c))

    xbmc.log('CLEANSUBS >> USING TOTAL DEFINITIONS: ' + str(len(rrr)) + ' elements')

    conn.close()

    return rrr

# ============================================================
# Class for timer
# ============================================================


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def isrunning(self):
        if not self.is_running:
            self.is_running = False
        else:
            self.is_running = True

# ============================================================
# Class for KODI player
# ============================================================


class XBMCPlayer(xbmc.Player):
    def __init__(self, *args):
        pass

    def onPlayBackStarted(self):
        global rt
        global subsPath
        global SubFirst
        global before

        is_video = xbmc.getCondVisibility('Player.HasVideo')

        if is_video:
            xbmc.log("CLEANSUBS >> PLAYBACK >>PLAYING<<")
            subsPath = PlayingInfo()
            SubFirst = getJson("Settings.GetSettingValue", "setting", "subtitles.downloadfirst", "value")

            if SubFirst:
                rt.isrunning()
                if not rt.is_running:
                    xbmc.log('CLEANSUBS >> USE FIRST SUB - STARTING TIMER')

                    dirs, files = xbmcvfs.listdir(subsPath)
                    before = dict([(f, None) for f in files])

                    rt.start()
                    xbmc.sleep(8000)
                    rt.isrunning()
                    if rt.is_running:
                        xbmc.log('CLEANSUBS >> STOPPING TIMER - USE FIRST SUB EXPIRED AFTER 8 SECONDS')
                        rt.stop()

    def onPlayBackResumed(self):
        global subsPath

        is_video = xbmc.getCondVisibility('Player.HasVideo')

        if is_video:
            xbmc.log("CLEANSUBS >> PLAYBACK >>RESUMED<<")
            subsPath = PlayingInfo()

    def onPlayBackEnded(self):
        global rt
        global DelSubFile

        is_video = xbmc.getCondVisibility('Player.HasVideo')

        if is_video:
            xbmc.log("CLEANSUBS >> PLAYBACK >>ENDED<<")
            rt.stop()
            path = os.path.dirname(DelSubFile)
            if path == xbmc.translatePath("special://temp") and xbmcvfs.exists(DelSubFile):
                try:
                    xbmcvfs.delete(DelSubFile)
                    xbmc.log("CLEANSUBS >> PLAY_END SUBS DELETED >>" + DelSubFile)
                except Exception:
                    xbmc.log("CLEANSUBS >> PLAY_END SUBS DELETE FAILED >>" + DelSubFile)

    def onPlayBackStopped(self):
        global rt
        global DelSubFile

        is_video = xbmc.getCondVisibility('Player.HasVideo')

        if is_video:
            xbmc.log("CLEANSUBS >> PLAYBACK >>STOPPED<<")
            rt.stop()
            path = os.path.dirname(DelSubFile)
            if path == xbmc.translatePath("special://temp") and xbmcvfs.exists(DelSubFile):
                try:
                    xbmcvfs.delete(DelSubFile)
                    xbmc.log("CLEANSUBS >> PLAY_STOP SUBS DELETED >>" + DelSubFile)
                except Exception:
                    xbmc.log("CLEANSUBS >> PLAY_STOP SUBS DELETE FAILED >>" + DelSubFile)

# ============================================================
# Get playing item info
# ============================================================


def PlayingInfo():
    global __addon__
    global booOn

    __addon__ = xbmcaddon.Addon(id='service.ghostcleansubs')
    booOn = bool(strtobool(str(__addon__.getSetting('on').title())))

    stream = xbmc.getCondVisibility('Player.IsInternetStream')

    exodus = GetExSubs()
    custpath = getJson("Settings.GetSettingValue", "setting", "subtitles.custompath", "value")
    storagemode = getJson("Settings.GetSettingValue", "setting", "subtitles.storagemode", "value")

    if stream:
        if exodus and custpath == "":
            path = xbmc.translatePath("special://temp")
        elif xbmcvfs.exists(custpath):
            path = custpath
        else:
            path = xbmc.translatePath("special://temp")
    else:
        if storagemode == 1:
            if xbmcvfs.exists(custpath):
                path = custpath
            else:
                path = xbmc.translatePath("special://temp")
        else:
            filename = xbmc.getInfoLabel('Player.Folderpath')
            path = os.path.dirname(filename)

    osWin = xbmc.getCondVisibility('System.Platform.Windows')

    if path[:4] == "smb:" and osWin:
        path = path[4:]
        path = '\\'.join(path.split('/'))
        path = str(path)

    if booOn:
        if path == "":
            path = xbmc.translatePath("special://temp")

        xbmc.log("CLEANSUBS >> SUBTITLES DOWNLOAD PATH SET TO: " + pipes.quote(path))
    else:
        xbmc.log("CLEANSUBS >> SUBTITLES CLEAN OFF")

    return path

# ============================================================
# Read exodus subtitle settings
# ============================================================


def GetExSubs():
    strAddon = 'plugin.video.exodus'
    isEx = xbmc.getCondVisibility('System.HasAddon(%s)' % strAddon)

    exsubs = False

    if isEx == 1:
        _addon = xbmcaddon.Addon(id=strAddon)

        try:
            exsubs = bool(strtobool(str(_addon.getSetting('subtitles').title())))
        except Exception:
            exsubs = False
            pass

        xbmc.log("CLEANSUBS >> EXSUBS: " + str(exsubs))

    if exsubs:
        return(True)
    else:
        return(False)

# ============================================================
# remove all subtitle files in temp kodi folder
# ============================================================


def CleanTemp():
    dirs, files = xbmcvfs.listdir(xbmc.translatePath("special://temp"))

    for f in files:
        SubExt = os.path.splitext(f)[1][1:].strip()
        if SubExt == "srt" or SubExt == "sub":
            remFile = os.path.join(xbmc.translatePath("special://temp"), f)
            try:
                xbmcvfs.delete(remFile)
                xbmc.log("CLEANSUBS >> REMOVING TEMP FILE %s" % (remFile))
            except Exception:
                xbmc.log("CLEANSUBS >> ERROR REMOVING TEMP FILE %s, TRYING READONLY FLAG" % (remFile))
                try:
                    os.chmod(remFile, stat.S_IWRITE)
                    os.remove(remFile)
                except Exception:
                    xbmc.log("CLEANSUBS >> ERROR REMOVING TEMP FILE %s" % (remFile))

# ============================================================
# Display cleaned animation and provider logo
# ============================================================


def DispAni():
    global __addonwd__
    global __addon__
    global booInfo
    global booLogo
    global myWidget

    booInfo = bool(strtobool(str(__addon__.getSetting('info').title())))
    ActWin = xbmcgui.getCurrentWindowId()

    if booInfo and ActWin == 12005:
        myWidget.show()
        myWidget.imgsubsprovider.setImage("")
        myWidget.txtsubsprovider.setLabel("")
        myWidget.txtsubsok.setLabel("")

        for i in range(1, 47):
            myWidget.imgsubsok.setImage(os.path.join(__addonwd__, "media", 'OK%02d.png' % i))
            xbmc.sleep(50)

        xbmc.sleep(400)
        strMess = __addon__.getLocalizedString(30021)     # CLEANED!
        myWidget.txtsubsok.setLabel(strMess)

        for i in range(48, 73):
            myWidget.imgsubsok.setImage(os.path.join(__addonwd__, "media", 'OK%02d.png' % i))
            xbmc.sleep(50)

        xbmc.sleep(500)

        for i in range(74, 79):
            myWidget.imgsubsok.setImage(os.path.join(__addonwd__, "media", 'OK%02d.png' % i))
            xbmc.sleep(50)

        xbmc.sleep(100)
        myWidget.imgsubsok.setImage("")
        myWidget.txtsubsok.setLabel("")
        myWidget.hide()

    booLogo = bool(strtobool(str(__addon__.getSetting('logo').title())))
    ActWin = xbmcgui.getCurrentWindowId()

    if booLogo and subProviderLogo and ActWin == 12005:
        if os.path.isfile(subProviderLogo):
            xbmc.log("CLEANSUBS >> PROVIDER LOGO FOUND: " + subProviderLogo)

            myWidget.show()
            myWidget.txtsubsprovider.setLabel("SUBTITLES PROVIDED BY")

            myWidget.imgsubsprovider.setImage(subProviderLogo)
            xbmc.sleep(3000)
            myWidget.imgsubsprovider.setImage("")
            myWidget.txtsubsprovider.setLabel("")
            myWidget.hide()
        else:
            xbmc.log("CLEANSUBS >> PROVIDER LOGO DOESNT EXIST: " + subProviderLogo)

# ============================================================
# To be repeated every x seconds
# ============================================================


def hw():
    global RUNNING
    global before
    global DelSubFile
    global rt
    global subsPath

    if RUNNING == 1:
        return

    RUNNING = 1

    dirs, files = xbmcvfs.listdir(subsPath)
    after = dict([(f, None) for f in files])
    added = [f for f in after if not f in before]

    if added:
        for f in added:
            SubExt = os.path.splitext(f)[1][1:].strip()
            if SubExt == "srt" or SubExt == "sub":
                xbmc.log("CLEANSUBS >> SUBS ADDED >>" + f)
                process_subs(os.path.join(subsPath, f), 0)

                xbmc.log("CLEANSUBS >> SUBS PROCESSED >>" + f)

                DispAni()
                DelSubFile = os.path.join(xbmc.translatePath("special://temp"), f)
                break
    else:
        for f in after:
            SubExt = os.path.splitext(f)[1][1:].strip()
            if SubExt == "srt" or SubExt == "sub":
                try:
                    mtime = xbmcvfs.Stat(os.path.join(subsPath, f)).st_mtime()
                except OSError:
                    mtime = 0

                if time.time() - mtime < 5:
                    xbmc.log("CLEANSUBS >> SUBS TIMSTAMP CHANGED >> " + f)
                    process_subs(os.path.join(subsPath, f), 0)
                    xbmc.log("CLEANSUBS >> SUBS PROCESSED >>" + f)

                    DispAni()
                    break

    before = after

    RUNNING = 0

# ============================================================
# Create sql3lite database - stats
# ============================================================


def MakeDatabase(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    try:
        c.execute('CREATE TABLE {tn} ({nf} {ft})'
                  .format(tn='stats', nf='date', ft='TEXT'))

        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                  .format(tn='stats', cn='uuid', ct='TEXT'))

        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                  .format(tn='stats', cn='md5', ct='TEXT'))

        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                  .format(tn='stats', cn='row', ct='REAL'))

        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                  .format(tn='stats', cn='format', ct='TEXT'))

        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                  .format(tn='stats', cn='pattern', ct='TEXT'))

        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
                  .format(tn='stats', cn='text', ct='TEXT'))

        conn.commit()
    except Exception:
        xbmc.log("CLEANSUBS >> SQL ERROR IN MakeDatabase (STATS)")

    conn.close()

    return

# ============================================================
# Add record to sql3lite database table
# ============================================================


def AddtoDatabase(sqlite_file, fields, strMd5):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO stats VALUES(?, ?, ?, ?, ?, ?, ?)", fields)
        conn.commit()
        conn.close()
    except Exception as e:
        xbmc.log("CLEANSUBS >> SQL ERROR IN AddtoDatabase : " + str(e))

    return

# ============================================================
# Check if subtitle is already in local database
# ============================================================


def CheckDatabase(sqlite_file, strMd5):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    try:
        c.execute("SELECT md5 FROM stats WHERE md5 = ?", (strMd5,))
        data = c.fetchone()
    except Exception:
        xbmc.log("CLEANSUBS >> SQL ERROR IN CheckDatabase")
        data = None

    conn.close()

    if data is None:
        xbmc.log("CLEANSUBS >> SUB STATS WILL BE ADDED TO LOCAL DATABASE")
        return True
    else:
        xbmc.log("CLEANSUBS >> SUB STATS ALREADY IN DATABASE - WILL NOT BE ADDED")
        return False

# ============================================================
# Heuristic strings
# ============================================================


def GetHeuristic():
    global strLocalDomain

    List = ()

    List += ('http:',)
    List += ('@',)
    List += ('www.',)
    List += ('.com',)
    List += ('.org',)
    List += ('.net',)
    List += ('.cz',)
    List += ('.rs',)
    List += ('.sk',)
    List += ('.info',)
    List += ('.pl',)
    List += ('.de',)
    List += ('.uk',)
    List += ('.hr',)
    List += ('.ba',)
    List += ('.mk',)
    List += ('.gr',)
    List += ('.ro',)
    List += ('.si',)
    List += ('.at',)
    List += ('.hu',)
    List += ('.ru',)
    List += ('.ua',)
    List += ('.it',)
    List += ('.es',)
    List += ('.nl',)
    List += ('.be',)

    if strLocalDomain != "":
        if strLocalDomain not in List:
            List += ('.' + strLocalDomain,)

    return List

# ============================================================
# Languages strings
# ============================================================


def GetAllLanguages():
    List = ()

    List += ('GENERIC',)
    List += ('AFRIKAANS',)
    List += ('ALBANIAN',)
    List += ('AMHARIC',)
    List += ('ARABIC',)
    List += ('ARMENIAN',)
    List += ('ASTURIAN',)
    List += ('BASQUE',)
    List += ('BELARUSIAN',)
    List += ('BULGARIAN',)
    List += ('BURMESE',)
    List += ('CATALAN',)
    List += ('CHINESE',)
    List += ('CZECH',)
    List += ('DANISH',)
    List += ('DUTCH',)
    List += ('ENGLISH',)
    List += ('ESPERANTO',)
    List += ('ESTONIAN',)
    List += ('FAROESE',)
    List += ('FINNISH',)
    List += ('FRENCH',)
    List += ('GALICIAN',)
    List += ('GEORGIAN',)
    List += ('GERMAN',)
    List += ('GREEK',)
    List += ('HEBREW',)
    List += ('HUNGARIAN',)
    List += ('ICELANDIC',)
    List += ('INDONESIAN',)
    List += ('ITALIAN',)
    List += ('JAPANESE',)
    List += ('KOREAN',)
    List += ('LATVIAN',)
    List += ('LITHUANIAN',)
    List += ('MACEDONIAN',)
    List += ('MALAY',)
    List += ('MALAYALAM',)
    List += ('MALTESE',)
    List += ('NORWEGIAN',)
    List += ('PERSIAN',)
    List += ('POLISH',)
    List += ('PORTUGUESE',)
    List += ('ROMANIAN',)
    List += ('RUSSIAN',)
    List += ('SERBO-CROATIAN',)
    List += ('SINHALA',)
    List += ('SLOVAK',)
    List += ('SLOVENIAN',)
    List += ('SPANISH',)
    List += ('SWEDISH',)
    List += ('TAMIL',)
    List += ('THAI',)
    List += ('TURKISH',)
    List += ('UKRAINIAN',)
    List += ('UZBEK',)
    List += ('VIETNAMESE',)
    List += ('WELSH',)

    return List

# ============================================================
# Get local domain
# ============================================================


def GetLocalDomain():
    try:
        response = urllib.request.urlopen('http://ipinfo.io/json')
        data = json.load(response)
        country = data['country'].lower()

        return country
    except Exception:
        return ""

# ============================================================
# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
# ============================================================


__addon__ = xbmcaddon.Addon(id='service.ghostcleansubs')
__addonname__ = __addon__.getAddonInfo('name')
__addonwd__ = xbmc.translatePath(__addon__.getAddonInfo('path'))
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__version__ = __addon__.getAddonInfo('version')

REM = []
booOn = bool(strtobool(str(__addon__.getSetting('on').title())))
sqlite_file = os.path.join(__addondir__, 'cleansubs.sqlite')
machineID = __addon__.getSetting('ID')
IDSynced = __addon__.getSetting('IDSynced')
booInfo = bool(strtobool(str(__addon__.getSetting('info').title())))
booLogo = bool(strtobool(str(__addon__.getSetting('logo').title())))
manFolder = __addon__.getSetting('folder')
booCustom = bool(strtobool(str(__addon__.getSetting('custdef').title())))
booRemoveCC = bool(strtobool(str(__addon__.getSetting('removecc').title())))
booDelOrigSub = bool(strtobool(str(__addon__.getSetting('delorigsub').title())))
booRemoveTags = bool(strtobool(str(__addon__.getSetting('removetags').title())))
intMethod = int(__addon__.getSetting('method'))
intHerlines = int(float(__addon__.getSetting('herlines')))
subsPath = xbmc.translatePath("special://temp")
booOverlayInit = False
booBlackBar = False
subProviderLogo = ""
Charset = ""
Languages = []
SubFirst = False

dirs, files = xbmcvfs.listdir(subsPath)
before = dict([(f, None) for f in files])

strLocalDomain = ""
saaTextColor = '00FFFF'

if __name__ == '__main__':
    xbmc.log("CLEANSUBS >> STARTED VERSION %s" % (__version__))

    a = __addon__.getSetting('on')
    __addon__.setSetting("on", a)

    a = getDefinitions()
    if a == 2:
        writeDefinitions()
    else:
        try:
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("SELECT COUNT (*) FROM definitions")
            numberOfRows = c.fetchone()[0]
            conn.close()
            if numberOfRows < 800:
                writeDefinitions()
        except Exception as e:
            try:
                conn.close()
            except Exception:
                pass
            writeDefinitions()

    GetSettings(0)
    monsettings = SettingMonitor()
    strLocalDomain = GetLocalDomain()

    if not machineID:
        machineID = str(uuid.uuid4())                # create random machine ID
        __addon__.setSetting('ID', machineID)

    xbmc.log("CLEANSUBS >> UUID is %s" % (machineID))

    CleanTemp()         # remove all subtitle files in temp kodi folder

    dirs, files = xbmcvfs.listdir(subsPath)
    before = dict([(f, None) for f in files])

    RUNNING = 0
    DelSubFile = ''

    if len(REM) != 0:
        player = XBMCPlayer()
        monitor = xbmc.Monitor()
        rt = RepeatedTimer(0.5, hw)
        rt.stop()

        iCounter = 0
        auto_lastrun = int(round(time.time()))

        while True:
            if monitor.waitForAbort(1):    # Sleep/wait for abort
                rt.stop()

                try:
                    myWidget._close()
                except Exception:
                    pass

                xbmc.log('CLEANSUBS >> EXIT')
                break                      # Abort was requested while waiting. Exit the while loop.
            else:
                iCounter += 1

                if iCounter > 300:         # Once every 5 minutes is OK
                    iCounter = 0
                    date_now = int(round(time.time()))
                    time_difference = int(date_now - auto_lastrun) / 60           # difference in minutes

                    xbmc.log("CLEANSUBS >> LAST RUN " + str(time_difference) + " MINUTES AGO")

                    if time_difference > 100:
                        xbmc.log('CLEANSUBS >> RUNNING AUTO UPDATE DEFINITIONS...')

                        if getDefinitions() == 2:
                            writeDefinitions()

                        auto_lastrun = int(round(time.time()))

                if booOn:
                    ActDialog = xbmcgui.getCurrentWindowDialogId()

                    if ActDialog == 10153:
                        subProviderLogo = xbmc.getInfoLabel('Control.GetLabel(110)')

                        rt.isrunning()
                        if not rt.is_running:
                            xbmc.log('CLEANSUBS >> CURRENT WINDOW %s - STARTING TIMER' % str(ActDialog))
                            subsPath = PlayingInfo()
                            if xbmcvfs.exists(subsPath + '/'):
                                dirs, files = xbmcvfs.listdir(subsPath)
                                before = dict([(f, None) for f in files])
                                rt.start()
                                xbmc.sleep(100)
                            else:
                                xbmc.log('CLEANSUBS >> PATH %s DOES NOT EXIST' % str(subsPath))
                    else:
                        rt.isrunning()
                        if rt.is_running:
                            xbmc.log('CLEANSUBS >> STOPPING TIMER - NOT IN SUBS DIALOG ANYMORE')
                            rt.stop()

                            dirs, files = xbmcvfs.listdir(subsPath)
                            before = dict([(f, None) for f in files])

                    ActWin = xbmcgui.getCurrentWindowId()

                    if not booOverlayInit and ActWin == 12005:
                        try:
                            x = myWidget
                        except NameError:
                            booOverlayInit = True
                            myWidget = OverlayText(12005)     # 12005: fullscreenvideo
                            xbmc.log('CLEANSUBS >> INITIALIZING OVERLAY')

    else:
        strMess = __addon__.getLocalizedString(30020)     # Definitions not found! See log for more details.
        xbmc.executebuiltin("XBMC.Notification(%s,%s,5000,%s)" % ('CleanSubs', strMess, __addon__.getAddonInfo('icon')))
        xbmc.log("CLEANSUBS >> DEFINITIONS >> DEFINITIONS MISSING!")

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
