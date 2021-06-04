import requests
from PIL import Image

from os import makedirs,remove
from os.path import join,splitext

from .helper import log, get_a_headers

def download_one_pic(url, name, session=None):
    browser = requests.session()
    if session:
        browser = session
    with open(name,'wb') as f:
        pic = browser.get(url,headers=get_a_headers(),verify=False)
        f.write(pic.content)
    

def download_all_pics(urls, name, session=None):
    try:
        makedirs(name, exist_ok=True)
    except:
        log(name + ' mkdir error')
    try:
        browser = requests.session()
        if session:
            browser = session
        for counter, oneurl in enumerate(urls):
            storeloc = join(name, str(counter).zfill(3)+'.jpg')
            download_one_pic(oneurl, storeloc, browser)
            log('download_one_pic ' + storeloc+' done', name=name)
    except:
        log('downloading pics err', name=name)
    log(name + ' done')

def change_Jpg_format(filename,dirpath=''):
    realfilename,__=splitext(filename)
    im = Image.open(join(dirpath,filename)).convert('RGB')
    remove(join(dirpath,filename))
    im.save(join(dirpath,realfilename+'.jpg'),'jpeg')
    log(realfilename+'.jpg'+' finish change_Jpg_format')
    return realfilename+'.jpg'