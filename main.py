#!/usr/bin/python3

import sys, piexif, re
from math import floor

def exif_set(dict, name, value):
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in piexif.TAGS[ifd]:
            this_name = piexif.TAGS[ifd][tag]["name"]
            if this_name == name:
                dict[ifd][tag] = value
                return
    raise(ValueError(f"Bad EXIF name {name}"))

def exif_list(dict):
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in dict[ifd]:
            name = piexif.TAGS[ifd][tag]["name"]
            value = dict[ifd][tag]
            print(f"{ifd}:{tag}:{name}:{value}")

def b(str):
    return bytes(str, 'utf-8')

image = piexif.load(sys.argv[1])

i = 2
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '-l':
        exif_list(image)
    if arg == '-g':
        i = i + 1
        lat_str = sys.argv[i]
        latitude = float(lat_str)
        lat_deg = int(floor(latitude))
        lat_min = int(floor((latitude - lat_deg) * 60))
        lat_sec = (latitude - lat_deg - lat_min / 60) * 3600
        lat_ref = 'N' if latitude >= 0 else 'S'
        i = i + 1
        lng_str = sys.argv[i]
        longitude = float(lng_str)
        lng_deg = int(floor(longitude))
        lng_min = int(floor((longitude - lng_deg) * 60))
        lng_sec = (longitude - lng_deg - lng_min / 60) * 3600
        lng_ref = 'E' if longitude >= 0 else 'W'
        print(f"Setting GPS position to {lat_deg}d {lat_min}m {lat_sec:0.2f}s {lat_ref}, {lng_deg}d {lng_min}m {lng_sec:0.2f}s {lng_ref}")
        exif_set(image, 'GPSVersionID', (2, 2, 0, 0))
        exif_set(image, 'GPSLatitudeRef', b(lat_ref))
        exif_set(image, 'GPSLatitude', ((lat_deg, 1), (lat_min, 1), (int(lat_sec * 100), 100)))
        exif_set(image, 'GPSLongitudeRef', b(lng_ref))
        exif_set(image, 'GPSLongitude', ((lng_deg, 1), (lng_min, 1), (int(lng_sec * 100), 100)))
    if arg == '-t':
        i = i + 1
        time_str = sys.argv[i].replace('-', ':')
        if re.match("[0-9]{4}:[0-9]{2}:[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", time_str):
            print(f"Setting time to {time_str}")
            exif_set(image, "DateTime", b(time_str))
            exif_set(image, "DateTimeOriginal", b(time_str))
            exif_set(image, "DateTimeDigitized", b(time_str))
        else:
            raise(ValueError("Bad date format"))
    if arg == '-s':
        print(f"Saving to file {sys.argv[1]}")
        piexif.insert(piexif.dump(image), sys.argv[1])
    
    i = i + 1

