from os import listdir
from os.path import join

from .video import download_video_by_youtube_dl, change_MP4_format
from .gallery import change_Jpg_format
from .helper import log, busy_wait, move_to_done,redirect_format

def youtubedl_thread(url):
    name = download_video_by_youtube_dl(url)
    files = listdir(name)
    for one_file in files:
        if(redirect_format(join(name,one_file)) == 'vdo'):
            change_MP4_format(one_file,name)
        elif(redirect_format(join(name,one_file)) == 'img'):
            change_Jpg_format(one_file,name)
    move_to_done(name)

def youtubedl(urls):
    threads = []
    for url in urls:
        thread = Thread(target = youtubedl_thread, args=[url,])
        threads.append(thread)
        busy_wait(threads)
        thread.start()
    
    for i in threads:
        i.join()
    log('youtubedl All Done.')

site_function_map = {
    'youtube.com':{'function':youtubedl, 'browser_need': False},
}