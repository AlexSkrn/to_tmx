#!/usr/bin/env python3
"""This script tokenizes an input file into sentences.

The sentences are written one sentence per line to file name <orig>_sent_tok.
"""

# import os
import argparse
import re
from nltk.tokenize import sent_tokenize


def sent_tok(filename, language):
    """Return a list of sentencies."""
    with open(filename, 'r', encoding='utf8') as fromF:
        text = fromF.read()
        sentences = []
        # Split into paragraphs and tokenize
        for para in re.split('\ufeff|\n|\r', text):
            if para:
                sentences.extend(sent_tokenize(para, language=language))
    return sentences


def write_to_file(sentences, filename):
    """Write sentences to filename and return None."""
    with open(filename + '_sent_tok', 'w', encoding='utf8') as toF:
        for sent in sentences:
            toF.write('{}\n'.format(sent))
    return None


def main():
    """Run the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        help='Provide file name to tokenize into sentences')
    parser.add_argument('lang', nargs='?', default='english',
                        help='Specify language if not English')
    args = parser.parse_args()

    filename = args.path  # file name to process
    # head, tail = os.path.split(filename)
    lang = args.lang  # Tokenizer language

    sentence_list = sent_tok(filename, lang)
    write_to_file(sentence_list, filename)


if __name__ == '__main__':
    main()
