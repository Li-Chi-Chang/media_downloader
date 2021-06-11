from .helper import log
from .sites import site_function_map
from threading import Thread

def download_control(urls):
    threads = []
    urlclassify = {}
    for site in site_function_map.keys():
        urlclassify[site] = []

    for url in urls:
        success = False
        for site in site_function_map.keys():
            if site in url:
                success = True
                urlclassify[site].append(url)
                break
        if not success:
            log(url+' site cannot found')

    
    for site in urlclassify.keys():
        if len(urlclassify[site]) > 0:
            threads.append(Thread(target = site_function_map[site]['function'], args=[urlclassify[site],]))
            log(site+' urls start')
            threads[-1].start()

    for i in threads:
        i.join()
    log('control All Done.')
    # log(url+' start download')
    # for site in site_function_map.keys():
    #     if site in url:
    #         log(url+' redirect to '+site+' fucntion')
    #         site_function_map[site]['function'](url)
    #         return
    # log(url+' unknown site')