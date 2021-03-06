#!/usr/local/bin/python

"""
Translate a batch of files.

Usage:
    python gtrans ru en -i inputDir -o outputDir -x py 
"""

import concurrent.futures
import os
import errno
import argparse
import goslate

# instantiate a Goslate object for the entire script
GS = goslate.Goslate()


def make_dir(path):
    """ Try to create the output directory."""
    try:
        os.makedirs(path)
    except OSError as exception:
        # if directory already exists do nothing
        if exception.errno != errno.EEXIST:
            raise


def translate_file(from_lang, to_lang, base_dir, in_file, out_dir, verbose):
    """
    Translate a file and write the translation to a directory.

    base_dir: The directory entered by the user if given a input dir.
              If given an input file, it is simply the file path.
              Used to create proper directory structure under output dir.
    """
    if verbose:
        print "Translating %s... " % in_file,

    translated_lines = GS.translate(open(in_file), to_lang, from_lang)
    translation = '\n'.join(translated_lines)

    # determine output file name and directory
    # recreate dir structure of input directory under output directory
    in_file_name, ext = os.path.splitext(in_file)
    # relative path gets rid of '..' in path
    rel_file_name = os.path.relpath(in_file_name, base_dir)
    out_file = os.path.join(out_dir, rel_file_name+'.'+to_lang)

    if verbose:
        print "Output in %s... " % out_file,

    make_dir(os.path.dirname(out_file))
    
    with open(out_file, 'w') as output:
        # encode translation as utf-8 else write will try to encode as ascii
        # and get UnicodeEncodeError
        encoded_translation = translation.encode('utf-8')
        output.write(encoded_translation)

    if verbose:
        print "Done."

def translate_dir(from_lang, to_lang, in_dir, out_dir, ext, verbose):
    #print "in_dir = %s" % in_dir
    for root, dirs, files in os.walk(in_dir):
        #print "root = {}, dirs = {}, files = {}".format(root, dirs, files)
        for f in files:
            file_name, file_ext = os.path.splitext(f)
            # check file type
            if ext is None or file_ext == '.'+ext:
                in_file = os.path.join(root, f)
                translate_file(from_lang, to_lang, in_dir, in_file, out_dir, 
                               verbose)
            else:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Translate a batch of files.")
    parser.add_argument("from_lang", help="input language")
    parser.add_argument("to_lang", help="output language")
    parser.add_argument("-i", help="input directory")
    parser.add_argument("-o", help="output directory")
    parser.add_argument("-x", help="file extension. Default all types.")
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="verbose", default=False)
    args = parser.parse_args()
    #print args

    if not (args.i and args.o):
        print "Please indicate input and output directories."
    else:
        if not args.verbose:
            print "Translating files in {} from {} to {}... ".format(args.i,
                                                                args.from_lang,
                                                                args.to_lang),
        translate_dir(args.from_lang, args.to_lang, args.i, args.o, args.x,
                      args.verbose)
        if not args.verbose:
            print "Done."

