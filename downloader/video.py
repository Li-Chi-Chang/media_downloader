import requests
from time import sleep
from urllib.parse import urljoin,urlsplit
from hyper import HTTP20Connection

from os import system, remove, makedirs, rename
from os.path import join, splitext

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from youtube_dl import YoutubeDL

from .helper import log,get_a_http20_headers,clearify,get_a_headers,move_to_done

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'}

def change_MP4_format(filename,dirpath=''):
    realfilename,ext=splitext(filename)
    print(realfilename)
    if(ext == 'mp4'):
        return realfilename+'.mp4'
    system('ffmpeg -i "' + join(dirpath,filename) + '" -c copy -movflags +faststart "' + join(dirpath,'DEBUG'+realfilename+'.mp4')+'"')
    remove(join(dirpath,filename))
    rename(join(dirpath,'DEBUG'+realfilename+'.mp4'),join(dirpath,realfilename+'.mp4'))
    log(realfilename+'.mp4'+' finish change_MP4_format',dirpath)
    return realfilename+'.mp4'

def decrypt_video(Key,IV,video):
    decryptObj = AES.new(Key, AES.MODE_CBC, IV)
    rawout = decryptObj.decrypt(pad(video,16))
    return rawout

def download_video_by_m3u8_http2(origin, m3u8url, video_name, serial = 0, sleeptime = 1):
    myheader = get_a_http20_headers()
    m3u8 = urlsplit(m3u8url)
    myheader[':authority'] = m3u8.netloc
    myheader[':path'] = m3u8.path
    myheader['origin'] = origin
    
    with HTTP20Connection(host='vvip.vvvcdn.live',secure=True) as conn:
        # m3u8 layer
        req = conn.request("GET",'',headers=myheader)
        rsp = conn.get_response(req)
        rsp_content = rsp.read()
        rsp_text = rsp_content.decode().split('\n')

        totalsegs = 0
        for line in rsp_text:
            if '#' in line:
                continue
            totalsegs += 1

        count = 0
        with open(join(video_name,'video' + str(serial) + '.ts'),'wb') as f:
            for line in rsp_text[3:]:
                if '#' in line:
                    continue
                log(str(count/totalsegs*100)+'% ' + urljoin(m3u8url,line.strip()),video_name)
                myheader[':path'] = urlsplit(urljoin(m3u8url,line.strip())).path
                req = conn.request("GET",'',headers=myheader)
                rsp = conn.get_response(req)
                rsp_content = rsp.read()
                f.write(rsp_content)
                sleep(sleeptime)
                log('sleeptime ' + str(sleeptime),video_name)
                count+=1
    system('ffmpeg -i "' + join(video_name,'video' + str(serial) + '.ts') + '" -c copy -movflags +faststart "' + join(video_name,'video' + str(serial) + '.mp4')+'"')
    remove(join(video_name,'video' + str(serial) + '.ts'))
    log('done ' + str(serial),video_name)
    log(video_name + ' ' + str(serial) + ' done')

def download_video_by_m3u8(m3u8url, video_name, sleeptime=1, session=None, serial = 0, myheader=None):
    try:
        makedirs(video_name, exist_ok=True)
    except:
        log(video_name + ' mkdir error')
    
    if(session is None):
        session = requests.session()
    if myheader is None:
        myheader = get_a_headers()

    key = None
    iv = None
    res = session.get(m3u8url,headers=myheader)
    if res.status_code in [404,403]:
        log('err resquest' + m3u8url,video_name)
        log(res.text,video_name)
        return
    
    totalsegs = 0
    lines = res.text.split('\n')
    for line in lines:
        if len(line) == 0:
            continue
        if '#' not in line[0]:
            totalsegs += 1
        else:
            if 'AES-128' in line:
                KeyFile = line.split('"')[1]
                key = session.get(urljoin(m3u8url,KeyFile),headers=myheader).content
                iv = (int('0x0',16)).to_bytes(16, byteorder='big')
            elif (len(line.split('IV=')) > 1):
                IVvalue = line.split('IV=')[1]
                iv = (int(IVvalue,16)).to_bytes(16, byteorder='big')
                KeyFile = line.split('"')[1]
                key = session.get(urljoin(m3u8url,KeyFile),headers=myheader).content

    count = 0
    with open(join(video_name,'video' + str(serial) + '.ts'),'wb') as f:
        for line in lines[3:]:
            if '#' in line:
                continue
            log(str(count/totalsegs*100)+'% ' + urljoin(m3u8url,line.strip()),video_name)
            #line without strip may have error like \r 
            res = session.get(urljoin(m3u8url,line.strip()),headers=myheader)
            if res.status_code in [404,403]:
                log('err resquest' + urljoin(m3u8url,line.strip()),video_name)
                return
            if(key is not None and iv is not None):
                f.write(decrypt_video(key,iv,res.content))
            elif(key == None and iv == None):
                f.write(res.content)
            sleep(sleeptime)
            log('sleeptime ' + str(sleeptime),video_name)
            count+=1
    system('ffmpeg -i "' + join(video_name,'video' + str(serial) + '.ts') + '" -c copy -movflags +faststart "' + join(video_name,'video' + str(serial) + '.mp4')+'"')
    remove(join(video_name,'video' + str(serial) + '.ts'))
    log('done ' + str(serial),video_name)
    log(video_name + ' ' + str(serial) + ' done')
    move_to_done(video_name)

def download_video_by_original_src(url,video_name,serial=0):
    try:
        with requests.get(url, stream=True) as r:
            total_length = int(r.headers.get('content-length'))
            if total_length is None or r.status_code == '404': # no content length header
                log(name = video_name,string = 'ERR No file ending or 404')
                total_length = 0
                log(name = video_name,string = url)
                return
            conter = 0
            with open(join(video_name,'video'+str(serial)+'.mp4'), 'wb') as f:
                chunk_size=8*1024*1024
                for chunk in r.iter_content(chunk_size=chunk_size):
                    log(name = video_name,string = str(round(conter*chunk_size/total_length*100,3))+'%')
                    f.write(chunk)
                    conter+=1
            change_MP4_format('video'+str(serial)+'.mp4',video_name)
            log(name = video_name,string = 'video '+str(serial)+' done')
            log(string = video_name+str(serial)+' done')
    except:
        log(name = video_name,string = 'some error here, check it')
        log(string = 'some error here, check it: ' + video_name)
    return

def download_video_by_youtube_dl(url):
    log('download_video_by_youtube_dl: '+url+' start')
    
    ytdl_format_options = {
        'outtmpl': '%(title)s.%(ext)s',
    }
    info_dict = None
    with YoutubeDL(ytdl_format_options) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    
    name = clearify(info_dict.get('title', None))
    makedirs(name,exist_ok=True)
    ytdl_format_options = {
        'outtmpl': name+'/video.%(ext)s',
        'writethumbnail': True,
    }
    with YoutubeDL(ytdl_format_options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
    log('download_video_by_youtube_dl: '+name+' downloaded')
    return name