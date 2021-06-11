from downloader import download_control
from os.path import isfile

download_list = 'download_demo.list'
if isfile('download.list'):
    download_list = 'download.list'

with open(download_list,'r') as fp:
    lines = fp.readlines()
    links = []
    for line in lines:
        if len(line.strip()) == 0:
            continue
        if '#' in line[0]:
            continue

        links.append(line.strip())
    download_control(links)