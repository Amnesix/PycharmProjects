#!/usr/bin/env python3
import sys
import base64


def get_base64_img(name: str) -> str:
    with open(name, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def convert_to_b64(name: str):
    with open(name.split('.')[0]+'.b64', 'wt') as f:
        f.write(get_base64_img(name))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: convert_to_b64 image.ext", file=sys.stderr)
    else:
        convert_to_b64(sys.argv[1])

