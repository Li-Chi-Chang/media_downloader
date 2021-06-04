from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from os.path import join, dirname, abspath

adblock_path = join(dirname(__file__),'files','adblock','4.27.0_1')
driver_path = join(dirname(__file__),'files','msedgedriver.exe')

def create_web_driver():
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    '''edge_options.add_argument('headless')'''
    path_to_extension = abspath(adblock_path)
    edge_options.add_argument('load-extension=' + path_to_extension)
    edge_options.add_argument('--mute-audio')
    edge_options.add_experimental_option('excludeSwitches',['disable-popup-blocking'])
    browser = Edge(executable_path=driver_path, options=edge_options)
    return browser