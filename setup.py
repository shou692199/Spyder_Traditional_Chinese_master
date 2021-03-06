# -*- coding: utf-8 -*-
"""
@contect:shou692199@gmail.com

@author: 蕭澧邦
"""

import os,shutil,sys,subprocess
import platform

thissys = platform.system()
FLAG = r'\\' if thissys == 'Windows' else '/'
pyver = sys.version_info[0] + sys.version_info[1]/10
MODICT = {'spyder':'spyder.mo',
          'spyder_pylint':'pylint.mo',
          'spyder_profiler':'profiler.mo',
		  'spyder_breakpoints':'breakpoints.mo'}
def checkpath(path):
    '''Checking...
    param path<str>: link:
    return <str>:Done!
    '''
    try:
        tmp = path.split(FLAG)
        if '.' in tmp[-1] and len(tmp)>1:
            path = FLAG.join(tmp[:-1])
    except:
        pass
    if os.path.exists(path):
        if os.path.isfile(path)==False:
            return path
        else:
            raise ValueError('Failed. files existed.')
    else:
        os.makedirs(path)
        return path


def search_packages_path(pyflag='1'):
    '''Finding site-packages...
    return <str>: path.
    '''
    sitepath="."
    for x in sys.path:
        if pyflag == '1' and 'anaconda' not in x.lower():
            continue
        if 'AppData' in x:
            continue
        ix1 = x.find('site-packages')
        ix2 = x.find('dist-packages')
        if( (ix1>=0 and x[ix1:]=='site-packages') or (ix2>=0 and x[ix2:]=='dist-packages') ):
          sitepath = x
          break
    
    return sitepath


def creat_language_folder(sitepath, modulename='spyder'):
    # creat zh_TW language folder
    try:
        zh_TW = sitepath + '{sep}{modulename}{sep}locale{sep}zh_TW{sep}LC_MESSAGES'.format(sep=FLAG, modulename=modulename)
        checkpath(zh_TW)
        
        return 1
    except:
        return 0
    
def shutil_file(sitepath, modulename='spyder'):
    mo_file_name = MODICT[modulename]
    zh_TW = sitepath + '{sep}{modulename}{sep}locale{sep}zh_TW{sep}LC_MESSAGES'.format(sep=FLAG, modulename=modulename)
    shutil.copyfile(mo_file_name,zh_TW + r'{0}{1}'.format(FLAG, mo_file_name))
    
def chinesize(sitepath):
    '''run pack'''
    configpath = sitepath + '{0}spyder{1}config{2}base.py'.format(FLAG,FLAG,FLAG)
    print(configpath)
    newpath = sitepath + '{0}base.py'.format(FLAG)
    if thissys == 'Windows':
        if pyver > 2.7:
            newf = open(newpath, 'w', encoding='utf-8')
            with open(configpath, 'r',encoding='utf-8') as f:
                lines = f.readlines()
        else:
            import io
            newf = io.open(newpath, 'w', encoding='utf-8')
            with io.open(configpath, 'r',encoding='utf-8') as f:
                lines = f.readlines()
    
        islanguage = 0
        for i in range(len(lines)):
            line = lines[i]
            newf.writelines(line)
            if "LANGUAGE_CODES = {'en': u'English'," in line:
                islanguage = 1
                mystr = "                  'zh_TW': u'繁體中文',\n" if pyver >2.7 else u"                  'zh_TW': u'繁體中文',\n"
                
                newf.writelines(mystr)
    
    else:
        newf = open(newpath, 'w')
        with open(configpath, 'r') as f:
            lines = f.readlines()
            islanguage = 0
        for i in range(len(lines)):
            line = lines[i]
            newf.writelines(line)
            if "LANGUAGE_CODES = {'en': u'English'," in line:
                #print(line)
                islanguage = 1
                mystr = "                  'zh_TW': u'繁體中文',\n"
                newf.writelines(mystr)
    newf.close()

    # rename old base.py
    if os.path.exists(sitepath + r'{0}spyder{1}config{2}base_bak.py'.format(FLAG, FLAG, FLAG)):
        os.remove(sitepath + r'{0}spyder{1}config{2}base_bak.py'.format(FLAG, FLAG, FLAG))
    os.rename(configpath,sitepath + r'{0}spyder{1}config{2}base_bak.py'.format(FLAG, FLAG, FLAG)) 
    # remove new base.py
    shutil.move(newpath,configpath) 
    mystr = u'Successful! Restart and Setting. \n\n Press ENTER and wait Spyder IDE start to \n set link: Tools–>Perferences–>Advanced Setting–>Language–>繁體中文.'
    pyinput(mystr)
    return

def pyinput(mystr):
    try:
        input_content = raw_input(mystr.encode('gbk'))
    except:
        input_content = input(mystr)
    return input_content

if __name__ == '__main__':
    mystr = u'This is the CHTlang tranlate pack.\nSelect a selection \n1、Insert Python link（for example: D:\Anaconda3\Lib\dist-packages or D:\Anaconda3\Lib\site-packages）。\n2、automatic load\nPlease enter 1 or 2:  '
    install_flag = pyinput(mystr)
    if install_flag == '1':
        mystr = u'Python was install at（for example:D:\python or D:\anaconda）：  '
        sitepath = pyinput(mystr)
    else:
        mystr = '''
        =======================================================
        Because the environment variables of different users are too complicated to be completely balanced,
        Join some manual configuration items.
        In general, only Windows systems can be cumbersome. Also, if you
        Is the windows system, please make sure your python is not installed in the system disk
        In the user folder under the AppData path, in order to take care of
        Most people have filtered AppData.
        
        
        note! ! ! If your Anaconda not install in defualt link, just choose 2 or 3 not 1.
	When installation exit Spyder IDE will be launch.
        ======================================================='''
        
        print(mystr)
        
        #==============================================================================
        mystr = u'What kind of your python? \n     1.Anaconda \n     2.Original \n     3.Other\nYou choosed（Number：'
        pyflag = pyinput(mystr)
   
        sitepath = search_packages_path(pyflag)
    
    print(sitepath)
    creat_language_folder(sitepath, 'spyder')
    shutil_file(sitepath, 'spyder')
    chinesize(sitepath)
    for m in MODICT.keys():
        if m =='spyder':
            continue
        creat_language_folder(sitepath, m)
        shutil_file(sitepath, m)
