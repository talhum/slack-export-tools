from src.stats import *
from src.pins import *
from src.files import *
from src.avatars import *

# CONSTANTS
SWITCH_CHAR = '-'
# Each switch maps to a boolean value, indicating whether or not data is required
# Default data is also contained for certain switches
SWITCH_DATA = {'a': False,
               'aa': True,
               'c': True,
               'de': True,
               'df': True,
               'ds': True,
               'et': False,
               'ej': False,
               'eh': False,
               'f': False,
               'i': True,
               'l': True,
               'o': True,
               'oi': True,
               'p': False,
               's': False}
SWITCH_DEFAULT = {'a': "avatars",
                  'et': "export_text",
                  'ej': "export_json",
                  'eh': "export_html",
                  'f': "files",
                  'p': "pins"}
SWITCH_STATS = ('s',)

# Vars
switches = {}
date_start = None
date_end = None

# FUNCS
# Exporting
def exportHistory():
    e = export(slack)

    if 'et' in switches:
        e.exportChannelData(io.text_dir, exportModes.TEXT)

    if 'ej' in switches:
        e.exportChannelData(io.json_dir, exportModes.JSON)

    if 'eh' in switches:
        e.exportChannelData(io.html_dir, exportModes.HTML)

def exportOther():
    if 'p' in switches:
        p = pins(slack)
        p.export(io.pins_dir)

    if 'f' in switches:
        f = files(slack)
        f.downloadFiles()

    if 'a' in switches:
        a = avatars(slack)
        a.exportAvatars(io.avatar_dir)

def exportStatistics():
    if not any(x in SWITCH_STATS for x in switches):
        return

    s = stats(slack)

    if 's' in switches:
        s.exportPostStats()

# Output info
def outputUsers():
    print("List of users:")
    for i in slack.metadata.users:
        print(i)

def outputSubtypes():
    subtypes = set()

    print("Scanning history")
    for channel in slack.channel_data:
        for message in slack.channel_data[channel]:
            if "subtype" in message:
                subtypes.add(message['subtype'])

    print("Subtypes found in message history:")
    for i in sorted(subtypes):
        print(i)

def outputTypes():
    # On the test data set, only 'message' is contained, so this is fairly redundant atm
    types = set()

    print("Scanning history")
    for channel in slack.channel_data:
        for message in slack.channel_data[channel]:
            if "type" in message:
                types.add(message['type'])

    print("Types found in message history:")
    for i in sorted(types):
        print(i)

# Runtime
def loadArgs():
    interpretArgs(sys.argv)
    setSlackSource()
    setLogMode()
    setAvatarMode()
    setExportMode()
    setExportLocations()
    setStatsMode()
    setDateModes()

def interpretArgs(argv):
    # Remove script location
    argv = argv[1:]

    i = 0
    while i < len(argv):
        # Argument must be a switch
        if not argv[i].startswith(SWITCH_CHAR):
            sys.exit("Incorrect args. Expected a switch")

        # Switch must be valid
        switch = argv[i][1:]
        if switch not in SWITCH_DATA:
            sys.exit("Incorrect args. Switch '" + switch + "' not found")

        # Switch must not have been added already
        if switch in switches:
            sys.exit("Incorrect args. Switch '" + switch + "' has already been added")

        # Does switch require an argument
        if SWITCH_DATA[switch]:
            i += 1
            if i >= len(argv):
                sys.exit("Incorrect args. Required an argument for '" + switch + "', but ran out of arguments")

            if argv[i].startswith(SWITCH_CHAR):
                sys.exit("Incorrect args. Required argument for '" + switch + "', but found a switch")

            switches[switch] = argv[i]
        else:
            i += 1

            # If there are no more arguments or next argument is a switch then either add none or the appropriate value
            if i >= len(argv) or argv[i].startswith(SWITCH_CHAR):
                if switch in SWITCH_DEFAULT:
                    switches[switch] = SWITCH_DEFAULT[switch]
                else:
                    switches[switch] = None
                continue

            switches[switch] = argv[i]

        i += 1

def setDateModes():
    global date_start, date_end

    if 'df' in switches:
        misc.dateMode = misc.strToEnum(dateModes, switches['df'])

    if 'ds' in switches:
        date_start = misc.interpretDate(switches['ds'])

    if 'de' in switches:
        date_end = misc.interpretDate(switches['de'])

def setSlackSource():
    if 'i' not in switches or switches['i'] == "":
        source_dir = ""
    else:
        source_dir = switches['i']
        if not source_dir.endswith("\\"):
            source_dir += "\\"

    io.source_dir = source_dir

def setStatsMode():
    if 's' not in switches or switches['s'] is None:
        return

    stats.mode = misc.strToEnum(statsModes, switches['s'])

def setLogMode():
    if 'l' not in switches:
        return

    log.mode = misc.strToEnum(logModes, switches['l'])

def setExportLocations():
    # Main dir, files, pins, stats
    io.setExportDir(switches.get('o', ""))
    io.setAvatarDir(switches.get('a', SWITCH_DEFAULT['a']))
    io.setFileDir(switches.get('f', SWITCH_DEFAULT['f']))
    io.setInfoDir(switches.get('oi', "info"))
    io.setPinsDir(switches.get('p', SWITCH_DEFAULT['p']))

    # History export
    io.setHtmlDir(switches.get('eh', SWITCH_DEFAULT['eh']))
    io.setJsonDir(switches.get('ej', SWITCH_DEFAULT['ej']))
    io.setTextDir(switches.get('et', SWITCH_DEFAULT['et']))

def setExportMode():
    mode = False
    if 'c' in switches:
        mode = misc.strToBool(switches['c'])

    export.COMPACT_EXPORT = mode

def setAvatarMode():
    mode = False
    if 'aa' in switches:
        mode = misc.strToBool(switches['aa'])
    avatars.ALL_USERS = mode

# START OF PROGRAM
loadArgs()

slack = slackData()
slack.loadSlack()
if date_start is not None or date_end is not None:
    slack.filter(date_start, date_end)

exportHistory()
exportStatistics()
exportOther()
log.log(logModes.LOW, "Finished")