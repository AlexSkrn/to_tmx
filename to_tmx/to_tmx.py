#!/usr/bin/env python3
"""This script converts two text files into one tmx file, with
EN-US and RU-RU language codes.

The files must have equal number of lines, with one sentence per line.

The resulting tmx files have been checked for compatibility with Heartsome
and Olifant tmx editors.
"""

import os
import argparse
import xml.etree.ElementTree as ET


def build_tree(root, *args):
    """Build a tree structure."""
    body = ET.SubElement(root, "body")
    if len(args) == 2:
        file1, file2 = args
        with open(file1, 'r', encoding='utf8') as f1, open(file2, 'r', encoding='utf8') as f2:
            for src, trg in zip(f1, f2):
                src = src.strip()
                trg = trg.strip()
                if src != trg:
                    tu = ET.SubElement(body, "tu")

                    tuv = ET.SubElement(tu,
                                        "tuv",
                                        attrib={'xml:lang': 'EN-US'}
                                        )
                    seg = ET.SubElement(tuv, "seg")
                    seg.text = src

                    tuv = ET.SubElement(tu,
                                        "tuv",
                                        attrib={'xml:lang': 'RU-RU'}
                                        )
                    seg = ET.SubElement(tuv, "seg")
                    seg.text = trg
    elif len(args) == 1:
        file1 = args[0]
        with open(file1, 'r', encoding='utf8') as f1:
            for line in f1:
                src, trg = line.split('\t')
                src = src.strip()
                trg = trg.strip()
                if src != trg:
                    tu = ET.SubElement(body, "tu")

                    tuv = ET.SubElement(tu,
                                        "tuv",
                                        attrib={'xml:lang': 'EN-US'}
                                        )
                    seg = ET.SubElement(tuv, "seg")
                    seg.text = src

                    tuv = ET.SubElement(tu,
                                        "tuv",
                                        attrib={'xml:lang': 'RU-RU'}
                                        )
                    seg = ET.SubElement(tuv, "seg")
                    seg.text = trg

    # wrap it in an ElementTree instance
    tree = ET.ElementTree(root)
    return tree


def indent(elem, level=0):
    """Create indentation for tree elements."""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def build_trg_file_name(*args):
    """Return the target file name."""
    if len(args) == 2:
        file1, file2 = args
        head, tail1 = os.path.split(file1)
        _, tail2 = os.path.split(file2)
        target_file_name = '{}-{}.tmx'.format(os.path.splitext(tail1)[0],
                                              os.path.splitext(tail2)[0])
    elif len(args) == 1:
        file_name = args[0]  # You get a tuple without [0]
        head, tail = os.path.split(file_name)
        target_file_name = '{}.tmx'.format(os.path.splitext(tail)[0])

    return head, target_file_name


def create_tmx(*args):
    """Create the tmx file."""
    root = ET.Element('tmx', attrib={'version': '1.4'})
    ET.SubElement(root, 'header', attrib={'srclang': 'EN-US'})
    tree = build_tree(root, *args)
    indent(root)
    # Save as tmx
    head, target_file_name = build_trg_file_name(*args)
    dsn = os.path.join(head, target_file_name)
    tree.write(dsn, encoding='UTF-8', xml_declaration=True)


def main():
    """Run the script."""
    description = """Text-to-tmx converter. Accepts one tab-delim source file
    (format: 'english text \\t russian text')
    or two source files: English.txt, Russian.txt. Texts must be
    sentence tokenized before passing them to this script."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('source', nargs='*',
                        help='Provide one or two file names, english first')
    args = parser.parse_args()
    if len(args.source) == 2:
        create_tmx(*args.source)
    elif len(args.source) == 1:
        create_tmx(*args.source)
    else:
        print('Wrong number of arguments, use -h flag for help')


if __name__ == '__main__':
    main()
