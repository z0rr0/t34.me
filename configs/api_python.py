#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, urllib2

def main():
    if len(sys.argv) < 2:
        print("Error, usage: {0} <your url>".format(sys.argv[0]))
        return 1
    url = sys.argv[1]
    print(urllib2.urlopen('http://t34.me/api/?u=' + url).read())
    return 0

if __name__ == '__main__':
    main()

