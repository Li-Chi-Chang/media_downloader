from os.path import splitext,join
from os import makedirs
from shutil import move
from time import sleep

imgext = ['.jpg','.webp','.png']
vdoext = ['.mkv','.mp4']

def clearify(string, with_space=True):
    signs = ['?','“','”','/','\\','<','>','*','|',':','&', '+','\'','.','!','"','#',]
    for sign in signs:
        string = string.replace(sign,'')
    if not with_space:
        string = string.replace(' ','')
    return string

def log(string,name='',end='\n'):
    with open(join(name,'download.log'), 'a', encoding='utf-16') as f:
        f.write(string+end)

def busy_wait(thread, limit_thread_num=15):
    while True:
        for th in thread:
            if not th.is_alive():
                thread.remove(th)
        if len(thread) < limit_thread_num:
            return
        else:
            sleep(5)
            log('wait...')

def redirect_format(filename):
    __,ext = splitext(filename)
    print(ext)
    if ext in imgext:
        return 'img'
    elif ext in vdoext:
        return 'vdo'
    else:
        return 'unknown'

def page_to_html(text, pagename='test.html'):
    f = open(pagename, 'w')
    f.write(text)
    f.close()

def get_a_headers():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49'}
    return headers

def get_a_http20_headers():
    myheader = {}
    myheader[':authority'] = ''
    myheader[':method'] = 'GET'
    myheader[':path'] = ''
    myheader[':scheme'] = 'https'
    myheader['accept'] = '*/*'
    myheader['accept-encoding'] = 'gzip, deflate, br'
    myheader['accept-language'] = 'zh-TW,zh;q=0.9'
    myheader['cache-control'] = 'no-cache'
    myheader['dnt'] = '1'
    myheader['origin'] = ''
    myheader['sec-ch-ua'] = 'Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"'
    myheader['sec-ch-ua-mobile'] = '?0'
    myheader['sec-fetch-dest'] = 'empty'
    myheader['sec-fetch-mode'] = 'cors'
    myheader['sec-fetch-site'] = 'cross-site'
    myheader['pragma'] = 'no-cache'
    myheader['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56'
    return myheader

def move_to_done(name):
    done_dir = 'done'
    makedirs(done_dir, exist_ok=True)
    move(name,join(done_dir))
    log('move '+name+' to done DONE')