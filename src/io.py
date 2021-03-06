from src.log import *
import json
import os

class io():
    # Store parts so we can reconstruct the full path
    __info_dir = ""
    __avatar_dir = ""
    __pins_dir = ""

    __file_dir = ""
    __html_dir = ""
    __json_dir = ""
    __text_dir = ""

    source_dir = ""
    export_dir = ""

    info_dir = __info_dir
    avatar_dir = __avatar_dir
    pins_dir = __pins_dir

    file_dir = __file_dir
    html_dir = __html_dir
    json_dir = __json_dir
    text_dir = __text_dir

    def __init__(self):
        pass

    @staticmethod
    def refreshDirLocations():
        io.avatar_dir = io.combinePaths(io.export_dir, io.__info_dir, io.__avatar_dir)
        io.file_dir = io.combinePaths(io.export_dir, io.__file_dir)
        io.html_dir = io.combinePaths(io.export_dir, io.__html_dir)
        io.info_dir = io.combinePaths(io.export_dir, io.__info_dir)
        io.json_dir = io.combinePaths(io.export_dir, io.__json_dir)
        io.pins_dir = io.combinePaths(io.export_dir, io.__info_dir, io.__pins_dir)
        io.text_dir = io.combinePaths(io.export_dir, io.__text_dir)

    @staticmethod
    def combinePaths(*args: str):
        dir = ""
        for arg in args:
            dir += arg
            if arg != "" and not arg.endswith("\\"):
                dir += "\\"

        return dir

    @staticmethod
    def setExportDir(dir: str):
        io.export_dir = io.combinePaths(dir)
        io.refreshDirLocations()

    @staticmethod
    def setFileDir(dir: str):
        io.__file_dir = dir
        io.refreshDirLocations()

    @staticmethod
    def setHtmlDir(dir: str):
        io.__html_dir = dir
        io.refreshDirLocations()

    @staticmethod
    def setJsonDir(dir: str):
        io.__json_dir = dir
        io.refreshDirLocations()

    @staticmethod
    def setAvatarDir(dir: str):
        io.__avatar_dir = dir
        io.refreshDirLocations()

    @staticmethod
    def setPinsDir(dir: str):
        io.__pins_dir = dir
        io.refreshDirLocations()

    @staticmethod
    def setInfoDir(dir: str):
        io.__info_dir = dir
        io.refreshDirLocations()

    @staticmethod
    def setTextDir(dir: str):
        io.__text_dir = dir
        io.refreshDirLocations()

    @staticmethod
    def bytesToStr(size: int, precision=2):
        # https://stackoverflow.com/a/32009595
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
            suffixIndex += 1  # increment the index of the suffix
            size = size / 1024.0  # apply the division
        return "%.*f%s" % (precision, size, suffixes[suffixIndex])

    @staticmethod
    def ensureDir(dir: str):
        if dir == '':
            return

        if not os.path.exists(dir):
            os.makedirs(dir)

    @staticmethod
    def loadJSONFile(file):
        loc = io.source_dir + file

        log.log(logModes.FULL, "Reading '" + loc + "'")

        file = open(loc, "r", encoding="utf8")
        data = file.read()
        data = json.loads(data)
        file.close()

        return data