from downloader import download_control

with open('generaldownload.txt','r') as fp:
    lines = fp.readlines()
    links = []
    for line in lines:
        if len(line.strip()) == 0:
            continue
        if '#' in line[0]:
            continue

        links.append(line.strip())
    download_control(links)