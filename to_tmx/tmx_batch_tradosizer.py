#!/usr/bin/env python3
"""This script applies tmx_tradosizer.py to a folder with several tmx files.

It saves results in folder tmx-trados-style/.

The effect of running this script on a directory containing tmx files is that
the name of each tmx files becomes an attribute of each <tu> element so that
when I import such tmx files into Trados Studio's TM, each imported segment
has a property whose value is the name of the tmx file from which that
segment originated.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog

from to_tmx import tmx_tradosizer


class ProcessTMX:

    def __init__(self):
        """
            self.inputdir: path returned by dialog window
                        (and where TMX files to be processed are)
            self.outputpath: where output files will be written
            self.tmx_files: list of tmx files to be processes
        """
        self.inputdir = ''
        self.outputpath = ''
        self.tmx_files = []

        self.select_directory()
        if self.inputdir:
            print('Reading files in:', self.inputdir)
            self.make_output_dir()
        if self.tmx_files:
            print('# of tmx files identified:', len(self.tmx_files))
            self.process_tmx_files()

    def select_directory(self):
        """Select the directory where the TMX files to be processed are."""
        root = tk.Tk()
        root.withdraw()
        result = filedialog.askdirectory()
        if result:
            self.inputdir = result

    def make_output_dir(self):
        """Create a dir for output files."""
        file_names = os.listdir(self.inputdir)
        self.tmx_files = [f for f in file_names if f.endswith('.tmx')]
        if self.tmx_files:
            self.outputpath = os.path.join(self.inputdir, 'tmx-trados-style/')
            print('Created output dir:', self.outputpath)
            if not os.path.exists(self.outputpath):
                try:
                    os.mkdir(self.outputpath)
                except Exception as e:
                    print("The program can't create the directory")
                    print(e)
                    sys.exit()

    def process_tmx_files(self):
        """Process tmx files by applying Trados style fields."""
        for f in self.tmx_files:
            tmx_tradosizer.create_tmx(os.path.join(self.inputdir, f),
                                      os.path.join(self.outputpath, f)
                                      )


if __name__ == '__main__':
    ProcessTMX()
