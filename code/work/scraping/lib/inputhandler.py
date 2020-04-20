import os, csv, sys, hashlib
from . import constants as const
from . import settings

class InputHandler:
    def __init__(self, settings):
        self.settings = settings
        self.path = self.settings.inputImageFolder
        print(self.path)
        self.imgcol = settings.imagesColumn
        self.linkcol = settings.linkColumn

        self.inputtype = const.FOLDER

        fulllist = os.listdir(self.path)
        self.filelist = []
        # Filter files for image files
        supported_types=['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.ico', '.pdf', '.tiff']

        for file in fulllist:
            ext = os.path.splitext(file)[1]
            if ext in supported_types:
                self.filelist.append(file)
        if len(self.filelist)==0:
            raise FileNotFoundError('Folder indicated as input does not contain image files.')

        # Cap total number of images if it is larger than the processing limit
        settings.numImages = len(self.filelist)

        if settings.numImages < settings.procLimit:
            settings.procLimit = settings.numImages
        elif settings.procLimit == 0:
            settings.procLimit = settings.numImages

        self.iterindex = 0


    def update(self):
        try:
            imgpath = self.filelist[self.iterindex]

            # Check type of path
            if imgpath.startswith("http://") or imgpath.startswith("https://"):
                isremote = True
            else:
                isremote = False
            if not os.path.isabs(imgpath):
                isabs = False
                imgpath = os.path.join(settings.inputImageFolder, imgpath)
            else:
                isabs = True

            # Extract filename and extension
            imgfn = os.path.basename(imgpath)
            imgex = os.path.splitext(imgpath)[1]

            # Clean extension (especially for remote images)
            if "?" in imgex:
                imgex = imgex.split("?")[0]

            # Set image id
            if not isremote:
                imgid = imgfn.split(".")[0]
            else:
                hashobj = hashlib.sha1(imgpath.encode('utf8'))
                imgid = hashobj.hexdigest()

            if self.inputtype == const.CSV:
                self.curRow = next(self.csv)
                link = self.curRow[self.linkcol]
            else:
                link = imgpath

            # Create copy filename if that is the case
            if (isremote or isabs) and settings.saveImageCopy:
                copyfn = imgid + imgex
                copyfp = os.path.join(settings.imageCpFolder, copyfn)
            else:
                copyfn = "NONE"
                copyfp = "NONE"

            self.curimg = {'id': imgid, 'path':imgpath, 'origfn': imgfn, 'ext': imgex, 'isremote': isremote, 'isabs': isabs, 'copyfn': copyfn, 'copyfp': copyfp, 'link': link}

            return True
        except IndexError:
            print("\n**END OF FILE**\n")
            return False
        except Exception as exc:
            print(exc)

    # Move to next entry in input file or to next image in folder

    def next(self):
        self.update()
        self.iterindex += 1

    def getCurImg(self):
        return self.curimg

    def getCurRow(self):
        if self.inputtype == const.CSV:
            return self.curRow
        else:
            return False

    def reset(self):
        self.iterindex=0
        self.file.seek(0)
        next(self.csv)
        if self.inputtype == const.CSV:
            self.curRow = next(self.csv)

    def getNumImages(self):
        return len(self.filelist)

    def getInputType(self):
        return self.inputtype

    def getCSVDialect(self):
        return self.csv.dialect

    def getCSVFieldnames(self):
        return self.csv.fieldnames
