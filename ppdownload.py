#! /usr/bin/env python3

import requests
import shutil
from lxml.etree import HTML
from base64 import b64decode
from sys import argv

def main():
    apps = argv[1:]
    for app in apps:
        req = requests.get(app)
        sel = HTML(req.content)
        title = sel.xpath('//h2[contains(@class, "app-title")]/text()')[-1]
        encoded = sel.xpath('//a[@class="btn-install-x"]/@appdownurl')[-1]
        decoded = b64decode(encoded).decode('utf8')
        print("%s: %s" % (title, decoded))
        
        resp = requests.get(decoded, stream=True)
        assert(resp.status_code == 200)
        with open('%s.ipa' % title, 'wb') as ipa:
            print('Downloading ipa %s...' % title)
            resp.raw.decode_content=True
            shutil.copyfileobj(resp.raw, ipa)
        print('%s downloaded' % title)

if __name__ == '__main__':
    main()
