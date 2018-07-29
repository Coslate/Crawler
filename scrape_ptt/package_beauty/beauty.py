
import urllib.request
import urllib
import re
import os

def TestHello():
    print("Hello World!")


def AutoDisplayImage():
    pass

def IsRelativePath(folder):
    is_relative = True
    folder_spl = str.split('\/')

    if(folder_spl[0] == ''):
        is_relative = False

    return is_relative

def GetSaveImage(url, folder):
    file_name = re.match(r".*\/(\S+)\.jpg\s*", url).group(1)

    if((folder == '.') or folder == './'):
        pass
    else:
        if not os.path.isdir(folder):
            os.makedirs(folder)

    urllib.request.urlretrieve(url,'{}/{}.jpg'.format(folder,file_name))

