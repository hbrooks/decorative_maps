"""
Usage:
    make_map_of_DC.py API_KEY [--save]

Options:
    --save
"""


import time


from docopt import docopt
import requests
import urllib.parse
from PIL import Image
from io import BytesIO
import numpy as np


DC_LAT = 38.889931
DC_LONG = -77.009003


def params_to_URLs(params_list):
    BASE_URL = 'https://maps.googleapis.com/maps/api/staticmap?'
    return [''.join([BASE_URL, urllib.parse.urlencode(params)]) for params in params_list]


def assemble_params(API_KEY):
    params_list = []
    CHANGE_IN_LAT = 0.001
    CHANGE_IN_LONG = 0.001
    WIDTH = 1
    HEIGHT = 1
    for lat_index in range(0, WIDTH):
        lat = round(DC_LAT+lat_index*CHANGE_IN_LAT, 6)
        for long_index in range(0, HEIGHT):
            long = round(DC_LONG+long_index*CHANGE_IN_LONG, 6)
            params = {
                'key': API_KEY,
                'zoom': 17,
                'size': '999999999x999999999',
                'center': str(lat)+','+str(long),
            }
            params_list.append(params)
    return params_list
    

def make_request(URL):
    current_delay = 0.01
    while current_delay <= 2.0:
        request = requests.get(URL)
        if request.status_code == 200:
            return request
        else:
            time.sleep(current_delay)
            current_delay *= 2
    raise Exception('Issue connecting to Google Maps API.')
            

def main(args):
    API_KEY = args['API_KEY']
    params_list = assemble_params(API_KEY)
    URL_list = params_to_URLs(params_list)
    request_count = 0
    images = []
    for request_count in range(0, len(URL_list)):
        URL = URL_list[request_count]
        request = make_request(URL)
        image = Image.open(BytesIO(request.content))
        images.append(image)
        image
        
        
        
    # if args['--save']:
    #     OUTPUT_FILE_NAME = '{}.png'.format(request_count)
    #     image = Image.open(BytesIO(request.content))
    #     image.save(OUTPUT_FILE_NAME)

                        

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    main(arguments)