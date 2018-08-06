
import urllib.request
import urllib
import re
import os
import shutil

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

def GetSaveImage(url, folder, folder_check):
    file_name = re.match(r".*\/(\S+)\.jpg\s*", url).group(1)

    if(folder_check):
        if((folder == '.') or folder == './'):
            pass
        else:
            if not os.path.isdir(folder):
                os.makedirs(folder)
            else:
                shutil.rmtree(folder, ignore_errors=True)
                os.makedirs(folder)

    urllib.request.urlretrieve(url,'{}/{}.jpg'.format(folder,file_name))

def GetAllImgURL(content_info):
    str_line_arr = content_info.split('\n')
    img_url_list = [CheckImgLineURL(line) for line in str_line_arr]
    img_url_list = [x for x in img_url_list if x is not None]

    return img_url_list

def CheckImgLineURL(context_line):
    ret_context_line = None
    match_line = re.match(r'.*\/\S+\.jpg\s*', context_line)
    if(match_line is not None):
        match_push  = re.match(r'.*\:\s*(http.*\/\S+\.jpg)\s*', context_line)
        match_push2 = re.match(r'.*(http.*\/\S+\.jpg)\s*', context_line)
        if(match_push is not None):
            ret_context_line = match_push.group(1)
        elif(match_push2 is not None):
            ret_context_line = match_push2.group(1)
        else:
            ret_context_line = context_line

    print(f'ret_context_line = {ret_context_line}')
    return ret_context_line


