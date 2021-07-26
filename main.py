#! /usr/bin/env python

# -*- coding: utf-8 -*-

import os
import json
from flask import Flask
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

app = Flask(__name__)


def ler(filename):
    data = {}
    i = -1
    for page_layout in extract_pages(filename):
        i += 1
        data[i] = []
        for container in page_layout:
            if isinstance(container, LTTextContainer):
                for el in container:
                    item = {}
                    # item['x0'] = el.x0
                    # item['x1'] = el.x1
                    # item['y0'] = el.y0
                    # item['y1'] = el.y1
                    item['x'] = el.x0
                    item['y'] = el.y0
                    item['w'] = el.width
                    item['h'] = el.height
                    item['text'] = el.get_text().strip().upper()
                    data[i].append(item)
                    # print(data)
    jsondata = json.dumps(data, ensure_ascii=False)
    return jsondata


@app.route("/<filename>")
def get_pdf(filename):
    print("lendo", filename)
    path = os.environ['PDF_FILES_PATH']
    jsondata = ler(path + filename)
    return jsondata
    return filename


if __name__ == '__main__':
    app.run(threaded=True)
