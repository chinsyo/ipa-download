#! /usr/bin/env python3

import requests
import shutil
from lxml.etree import HTML
from base64 import b64decode
from sys import argv
import json

def main():
    apps = argv[1:]
    for app in apps:
        req = requests.get(app)
        sel = HTML(req.content)
        title = sel.xpath('//div[@class="h1"]/text()')[-1]
        encoded = sel.xpath('//a[contains(@class, "download_from_pc")]/@data-download')[-1]
        decoded = b64decode(encoded).decode('utf8')
        print("%s: %s" % (title, decoded))
        info = json.loads(decoded)
        path = info['path']
        print("info: ", info, path)

        resp = requests.get(path, stream=True)
        assert(resp.status_code == 200)
        with open('%s.ipa' % title, 'wb') as ipa:
            print('Downloading ipa %s...' % title)
            resp.raw.decode_content=True
            shutil.copyfileobj(resp.raw, ipa)
        print('%s downloaded' % title)

if __name__ == '__main__':
    main()