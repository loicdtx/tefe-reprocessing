import requests
from pprint import pprint
import json
import urllib
import re
from datetime import datetime
import os

import argparse
import getpass

dir_out = '/data/landsat-tefe'

orders = ['loic.dutrieux@wur.nl-03102017-164024-729',
          'loic.dutrieux@wur.nl-03102017-164136-859',
          'loic.dutrieux@wur.nl-03102017-164211-903']

def parseSceneId(id):
    """Landsat sceneID parser
    Identifies a typical LandsatID sequence in a string and returns a
    dictionary with information on sensor, date, path and row. The function
    raises an error in case no Landsat scene ID pattern can be found
    Args:
        id (string) string containing a Landsat scene ID
    Returns:
        dictionary: Dictionary containing information on sensor, date, path and row
    """
    id_grep = re.compile(".*(LT4|LT5|LE7|LC8|LO8)(\d{3})(\d{3})(\d{7}).*", re.IGNORECASE)
    m = id_grep.search(id)
    if m is None:
        raise ValueError('Landsat ID pattern not found for %s' % id)
    id_meta = {'sensor': m.group(1).upper(),
               'date': datetime.strptime(m.group(4), "%Y%j").date(),
               'path': int(m.group(2)),
               'row': int(m.group(3))}
    return id_meta

class PwdAction(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         mypass = getpass.getpass()
         setattr(namespace, self.dest, mypass)


def main(username, password):
    for order in orders:
        r = requests.get('https://espa.cr.usgs.gov/api/v0/item-status/%s' % order, auth = (username, password))
        scene_list = json.loads(r.text)['orderid'][order]
        dl_list = [scene['product_dload_url'] for scene in scene_list if parseSceneId(scene['name'])['path'] == 1 and parseSceneId(scene['name'])['row'] == 62]
        for url in dl_list:
            file_name = url.split('/')[-1]
            pprint('Downloading %s' % url)
            urllib.urlretrieve(url, os.path.join(dir_out, file_name))


if __name__ == '__main__':

    epilog = ('Download ordered scenes from path/row 001/062\n'
              '\n ')

    parser = argparse.ArgumentParser(epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-u", "--username", help="ESPA username")
    parser.add_argument('-p', "--password", action=PwdAction, nargs=0)
    # parser.add_argument('-p', action=Password, nargs='?', dest='password', help='ESPA password:')

    parsed_args = parser.parse_args()

    main(**vars(parsed_args))