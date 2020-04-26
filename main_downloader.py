# Neutron -- a download manager
import requests
import mimetypes
import os
import time
import warnings
from tqdm import tqdm
from .constants import *
warnings.filterwarnings('ignore')

class Downloader:
    ''':dUrl: - url to download from
    :sess: None - `requests.Session` obj
    :customName: None - Name for the file
    :customPath: None - Full path to the directory where file
                        will be downloaded
    '''

    groupExt = mainExtensions

    def __str__(self):
        return self.downloadPath

    def __init__(self, dUrl, sess=None, customName=None, customPath=None):
        print('Downloading from\n', dUrl)
        
        self.customName = customName
        self.customPath = customPath
        
        if self.customPath is None:
            self.dwnld = os.path.join(os.path.expanduser('~'), 'Downloads')
            self.makeDirIfNoDir(self.dwnld)
        else:
            os.makedirs(self.customPath, exist_ok=True)

        if sess is None:
            sess = requests.Session()

        with sess as self.sess:
            req = requests.Request('GET', dUrl)
            self.prep = self.sess.prepare_request(req)
            self.chunkSize = 1024 * 8
            self.downloadPath = self.mainDownloader()
        
    @staticmethod
    def fileAlreadyExists(fp):
        '''check if file already exists. if it does, tries to number it.'''
        i = 0
        parent, fullname = os.path.split(fp)
        # '.'.join(f.split('.')[:-1]), f.split('.')[-1]
        justname, dotExt = os.path.splitext(fullname)

        def keepChecking(innerFilename):
            nonlocal i
            if innerFilename in os.listdir(parent):
                i += 1
                return keepChecking(f'{justname}_({i}){dotExt}')
            else:
                return innerFilename
        return os.path.join(parent, keepChecking(fullname))

    @staticmethod 
    def tryContentDisposition(response, preferThis=None):
        '''returns Full Name with extension else None'''
        preferredName = response.headers.get('content-disposition')
        if preferredName is not None:
            # length of string 'attachment; filename=' is 21
            e = preferredName[21:]
            
            if not preferThis: 
                return e
            else:
                return preferThis + '.' + e.split('.')[-1]

        return None

    @staticmethod
    def hasExt(string):
        '''returns Full Name with extension else None'''
        if mimetypes.guess_type(string)[0] is not None: # then we know it has extension
            return string

        return None

    @staticmethod
    def tryContentType(response, string):
        '''returns Full Name with extension else None'''
        conType = response.headers.get('content-type')
        ext = mimetypes.guess_extension(conType)
        
        if ext is not None:
            print('appending extension', ext)
            return string + ext

        return None

    def mainDownloader(self):
        r = self.sess.send(self.prep, stream=True, verify=False)
        r.raise_for_status()
        # SO LINUX DOESNT NEED FILE EXTENSIONS JUST THE BINARY FILES????????
        totalSize = int(r.headers.get('content-length', 0))
        
        if not self.customName:
            # this may or may not have extension
            defaultName = r.url.split('/')[-1]

            fullname = self.tryContentDisposition(r, preferThis=None) or \
                        self.hasExt(defaultName) or \
                        self.tryContentType(r, defaultName) or \
                        None
        else:
            # this may or may not have extension
            givenName = self.customName

            fullname = self.hasExt(givenName) or \
                        self.tryContentDisposition(r, preferThis=givenName) or \
                        self.tryContentType(r, givenName) or \
                        None
        
        if fullname is None: return None
        ext = fullname.split('.')[-1]

        if self.customPath: # if customPath is provided dont categorize
            fullPath = os.path.join(self.customPath, fullname)# has extension
        else:
            fullPath = os.path.join(self.catgPath(ext), fullname)# has extension

        fullPath = self.fileAlreadyExists(fullPath)
        with open(fullPath, 'wb') as f:
            if totalSize is None:
                print('CANNOT DETERMINE TOTAL SIZE!! PROGRESS BAR WILL BE INCORRECT!!')
            # for c, chunk in enumerate(r.iter_content(chunk_size=self.chunkSize)):
            for chunk in tqdm(iterable=r.iter_content(chunk_size=self.chunkSize),
                                 total=totalSize//self.chunkSize,
                                 unit='KB'):
                f.write(chunk)
                # Downloader.progressBar(totalSize, self.chunkSize, c)

        print(f'Downloaded to: {fullPath}')
        return fullPath

    def catgPath(self, urlOrExt):
        # if the extension is present in dict, insert it in respective dirs.        
        for catg in self.groupExt.keys():
            if urlOrExt.endswith(self.groupExt[catg]):
                return os.path.join(self.dwnld, catg)
        
        # else file will be downloaded to Downloads directory
        else:
            print('cant categorize')
            return self.dwnld


    def makeDirIfNoDir(self, dwnldFolder):
        for folder in self.groupExt.keys():
            os.makedirs(os.path.join(dwnldFolder, folder), exist_ok=True)
        return 'All required folder are available.'


if __name__ == "__main__":
    dp = Downloader('https://i.imgur.com/zOx3E2a.jpg', customName='peepee1')
    print('\n\n')
    print(dp)

    # 1) customName without extension only
    # print(Downloader('https://i.imgur.com/zOx3E2a.jpg', customName='peepee1').downloadPath)
    
    # 2) customName without extension + customPath
    # print(Downloader('https://i.imgur.com/zOx3E2a.jpg', customName='peepee2', customPath='/home/nope/Downloads/haha1').downloadPath)
    
    # 3) customName with extension only
    # print(Downloader('https://i.imgur.com/zOx3E2a.jpg', customName='peepee3.png').downloadPath)
    
    # 4) customName with extension + customPath
    # print(Downloader('https://i.imgur.com/zOx3E2a.jpg', customName='peepee4.bmp', customPath='/home/nope/Downloads/haha2').downloadPath)

    # print(Downloader('https://subscene.com/subtitles/english-text/ZAZctvCCWJIxcWRKjnD5sZJQn2LB6PfGBivnDNWP9tMlTBW_-5_PmgISkGOvyjWQxyOENTM_Q8HTAVgZSd4NhwGwYgzMWjXBAM4yKcVdH0ND9BEyeYnRDZI8YOcEF49G0',
    #      customName='peepee5', customPath='/home/nope/Downloads/haha3').downloadPath)

    # print(Downloader('https://subscene.com/subtitles/english-text/ZAZctvCCWJIxcWRKjnD5sZJQn2LB6PfGBivnDNWP9tMlTBW_-5_PmgISkGOvyjWQxyOENTM_Q8HTAVgZSd4NhwGwYgzMWjXBAM4yKcVdH0ND9BEyeYnRDZI8YOcEF49G0',
    #          customPath='/home/nope/Downloads/SubTitles').downloadPath)


