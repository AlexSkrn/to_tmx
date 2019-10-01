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


def build_tree(root, file1, file2):
    """Build a tree structure."""
    body = ET.SubElement(root, "body")

    with open(file1, 'r', encoding='utf8') as f1, open(file2, 'r', encoding='utf8') as f2:
        for src, trg in zip(f1, f2):
            src = src.strip()
            trg = trg.strip()
            if src != trg:
                tu = ET.SubElement(body, "tu")

                tuv = ET.SubElement(tu,
                                    "tuv",
                                    attrib={'lang': 'EN-US'}
                                    )
                seg = ET.SubElement(tuv, "seg")
                seg.text = src

                tuv = ET.SubElement(tu,
                                    "tuv",
                                    attrib={'lang': 'RU-RU'}
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


def main():
    """Run the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path1',
                        help='Provide first file name')
    parser.add_argument('path2',
                        help='Provide second file name')
    args = parser.parse_args()

    file1 = args.path1
    file2 = args.path2

    root = ET.Element('tmx', attrib={'version': '1.4'})
    ET.SubElement(root, 'header', attrib={'srclang': 'EN-US'})
    tree = build_tree(root, file1, file2)
    indent(root)
    # Save as tmx
    head, tail1 = os.path.split(file1)
    _, tail2 = os.path.split(file2)
    target_file_name = '{}-{}.tmx'.format(os.path.splitext(tail1)[0],
                                          os.path.splitext(tail2)[0])
    dsn = os.path.join(head, target_file_name)
    tree.write(dsn, encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    main()
