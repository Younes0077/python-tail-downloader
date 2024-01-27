#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import math
import os
import os.path
import urllib.request

import requests


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def download_url(zoom, xtile, ytile):
    # url = "https://tile.openstreetmap.de/%d/%d/%d.png" % (zoom, xtile, ytile) url =
    # "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%d/%d/%d.png" % (zoom,
    # xtile, ytile) url = "https://khms1.google.com/kh/v=966?x=%d&y=%d&z=%d" % (xtile, ytile,zoom) url =
    # "https://khms0.googleapis.com/kh?v=966&hl=en-US&x=%d&y=%d&z=%d" % (xtile, ytile,zoom)
    url = "https://api.maptiler.com/maps/satellite/256/%d/%d/%d.jpg?key=y9tbWYVWkwEbvCGIwH9N" % (zoom, xtile, ytile)
    dir_path = "tiles/%d/%d/" % (zoom, xtile)
    download_path = "tiles/%d/%d/%d.png" % (zoom, xtile, ytile)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if not os.path.isfile(download_path):
        # x = requests.get(url)
        # print(x.content)
        print(url)
        urllib.request.urlretrieve(url, download_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-x", type=float, help="Minimum longitude", default='52.657487')
    parser.add_argument("-X", type=float, help="Maximum longitude", default='52.723451')
    parser.add_argument("-y", type=float, help="Minimum latitude", default='35.272489')
    parser.add_argument("-Y", type=float, help="Maximum latitude", default='35.299514')
    parser.add_argument("-Z", type=int, help="Maximum zoom level (>=7)", default=20)
    args = parser.parse_args()

    # Zoom 0 to 6 download worldwide tiles
    for zoom in range(0, 7):
        for x in range(0, 2 ** zoom):
            for y in range(0, 2 ** zoom):
                download_url(zoom, x, y)

    # # Zoom 0 to 6 download worldwide tiles
    # for zoom in range(6, 7):
    #     for x in range(30, 45):
    #         for y in range(30, 45):
    #             download_url(zoom, x, y)

    for zoom in range(7, int(args.Z) + 1):
        xtile_min, ytile_min = deg2num(float(args.y), float(args.x), zoom)
        xtile_max, ytile_max = deg2num(float(args.Y), float(args.X), zoom)

        print(f"Z:{zoom}, X:{xtile_min}-{xtile_max}, Y:{ytile_max}-{ytile_min}")
        for x in range(xtile_min, xtile_max + 1):
            for y in range(ytile_min, ytile_max - 1, -1):
                result = download_url(zoom, x, y)

