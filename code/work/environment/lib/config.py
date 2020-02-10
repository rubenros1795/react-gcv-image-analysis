import configparser, argparse, os, sys
from . import constants as const
from . import settings

def cleanQuotes(path):
    if (path.startswith('\'') and path.endswith('\'')) or (path.startswith('\"') and path.endswith('\"')):
       return path[1:-1]
    else:
        return path

def parsearg():
    parser = argparse.ArgumentParser(description='Process images through Google Cloud Vision API')

    parser.add_argument(    '--input_folder',
                             metavar="INPUT_PATH",
                             nargs=1,
                             default='NONE',
                             required=False,
                             help='Receives string for path to file with image list or folder containing images to be processed. Required in case no config file is available.'
                         )


    parser.add_argument(    '--key',
                             nargs=1,
                             default="NONE",
                             help='Receives string containing the API key for accessing Google\'s services.'
                         )


    parser.add_argument(    '--output_folder',
                            metavar="INPUT_PATH",
                            nargs=1,
                            default='NONE',
                            required=False,
                            help='Receives string for folder where images + annotations should be stored.'
                             )
    parser.add_argument(    '--iteration',
                            metavar="INPUT_PATH",
                            nargs=1,
                            default='NONE',
                            required=False,
                            help='identifier for iteration'
                                 )

    return parser.parse_args()

def parseconfiginput(args):

    try:
        #settings.inputImageFolder      = str(args.input_folder[0])
        #settings.projectFolder     = configfile.get('Project', 'projectFolder')
        #settings.outputsFolder     = os.path.join(settings.dir_path, str(args.output_folder[0]))

        fn_cacheFolder = str(args.output_folder[0]) + "_" + str(args.iteration[0])
        settings.cacheFolder   = os.path.join(settings.dir_path, fn_cacheFolder)

        #settings.imageCpFolder     = os.path.join(settings.outputsFolder, configfile.get('Advanced settings','ImageCopyFolder'))
        #settings.logsFolder        = os.path.join(settings.outputsFolder, configfile.get('Advanced settings', 'LogFolder'))

        settings.saveImageCopy     = True
        settings.timeseries        = True
        settings.labelThreshold    = 0.5

        settings.forceBase64       = True
        settings.inputImageFolder  = str(args.input_folder) #cleanQuotes(configfile.get('Input configuration','InputImageFolder'))


        settings.procLimit         = 0

        #settings.labelDetection    = #configfile.getboolean('Api setup','Label')
        #settings.safeSearchDetection = #configfile.getboolean('Api setup','SafeSearch')
        #settings.textDetection     = #configfile.getboolean('Api setup','Text')
        settings.webDetection      = True #configfile.getboolean('Api setup','Web')
        #settings.faceDetection     = #configfile.getboolean('Api setup','Face')

        settings.maxResults        = 1000000 #configfile.getint('Api setup','MaxResults')
        settings.apiKey            = args.key #configfile.get('Api setup','ApiKey')

        if settings.maxResults == 0:
            settings.setMaxResults = False
        else:
            settings.setMaxResults = True

    except Exception as exc:
        print(exc)
        print(const.config_parse_error)
        sys.exit()

def initconfig():
    args = parsearg()
    parseconfiginput(args)
