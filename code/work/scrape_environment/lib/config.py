import os, sys
from . import constants as const
from . import settings

def cleanQuotes(path):
    if (path.startswith('\'') and path.endswith('\'')) or (path.startswith('\"') and path.endswith('\"')):
       return path[1:-1]
    else:
        return path

def parseconfiginput(input_folder, key, output_folder, iteration):

    try:

        fn_cacheFolder = str(output_folder) + str(iteration)
        settings.cacheFolder   = os.path.join(settings.dir_path, fn_cacheFolder)
        settings.saveImageCopy     = True
        settings.timeseries        = True
        settings.labelThreshold    = 0.5
        settings.forceBase64       = True
        settings.inputImageFolder  = str(input_folder)
        settings.procLimit         = 0
        settings.webDetection      = True
        settings.maxResults        = 1000
        settings.apiKey            = key

        if settings.maxResults == 0:
            settings.setMaxResults = False
        else:
            settings.setMaxResults = True

    except Exception as exc:
        print(exc)
        print(const.config_parse_error)
        sys.exit()

def initconfig(input_folder, key, output_folder, iteration):
    parseconfiginput(input_folder, key, output_folder, iteration)
