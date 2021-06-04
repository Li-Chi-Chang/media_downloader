# media_downloader

* before using, pls add adblock package and webdriver in /downloader/files.
* or change the path in downloader/webdriver.py
* or apply your webdriver in downloader/webdriver.py
* or just use it without webdriver (cannot use JS render)

## add a website

1. add function in site.py, the input will be links=['url1','url2',...]
2. connect website name and function in site_function_map

## usage

1. use generaldownload.txt to record all links
2. run python generaldownload.py in this folder

## support type

### video

1. youtube-dl website (https://ytdl-org.github.io/youtube-dl/supportedsites.html)
2. m3u8 http2 encrypt video
3. m3u8 http2 video
4. m3u8 http1 encrypt video
5. m3u8 http1 video
6. original html5 video src

### image

1. html5 img
2. img lists

### javascript

1. with JS -> use webdriver
2. without JS -> use requests package only