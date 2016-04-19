#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main():
    try:
        app.run()
    except clip.ClipExit as e:
        sys.exit(e.status)

if __name__ == '__main__':
    main()
