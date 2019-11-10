#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""This program is used to prepare corpora extracted from TMX files.

It extracts  from a directory containing TMX files (and from all of its
subdirectories) all the segments of one language pair (except empty segments
and segments that are equal in both languages) and removes all other
information. It then creates 2 separate monolingual files, both of which
have strictly parallel (aligned) segments.

The original code is from the Moses For Mere Mortals project. See
https://github.com/agesmundo/MosesLabelFeats/tree/master/contrib/Extract_TMX_Corpus

I simplified the code for my use case.
The script no longer requires Pythoncard or wxPython or Python 2.
Language codes (namely, 'EN-US' and 'RU-RU') and output corpora basename are
now hard-coded.
When you run the code, just choose the directory that contains your tmx files.
"""

import os
import re
import sys
from time import strftime
import codecs

import tkinter as tk
from tkinter import filedialog


class Extract_TMX_Corpus:

    def __init__(self):
        """Initialize values

        @self.inputdir: directory whose files will be treated
        @self.outputfile: base name of the resulting corpora files
        @self.outputpath: root directory of the resulting corpora files
        @self.languages: list of languages whose segments can be processed
        @self.startinglanguage: something like 'EN-GB'
        @self.destinationlanguage: something like 'FR-FR'
        @self.numtus: number of translation units extracted so far
        @self.presentfile: TMX file being currently processed
        @self.errortypes: variable that stocks the types of errors detected
                        in the TMX file that is being processed
        @self.wroteactions: variable that indicates whether the actions
                        files has already been written to
        """

        self.inputdir = ''
        self.outputfile = ''
        self.outputpath = ''
        self.startinglanguage = ''
        self.destinationlanguage = ''
        self.tottus = 0
        self.numtus = 0
        self.numequaltus = 0
        self.presentfile = ''
        self.errortypes = ''
        self.wroteactions = False
        self.errors = ''
        if not self.SelectDirectory():  # User hits Cancel
            return
        self.ExtractCorpus()

    def extract_language_segments_tmx(self,text):
        """Extracts TMX language segments from TMX files

        @text: the text of the TMX file
        @pattern: compiled regular expression object
        @tus: list that collects the translation units of the text
        @segs: list that collects the segment units of the pair of languages
        @numtus: number of translation units extracted
        @present_tu: stocks  translation unit relevant segments being processed
        @self.errortypes: stocks errors detected in TMX file being processed
        """
        print('extract_language_segments: start at '+strftime('%H-%M-%S'))
        result = ('', '')
        try:
            if text:
                # Extract translation units
                pattern = re.compile('(?s)<tu.*?>(.*?)</tu>')
                tus = re.findall(pattern,text)
                ling1 = ''
                ling2 = ''
                #Extract relevant segments and store them in the @text variable
                if tus:
                    for tu in tus:
#                        print tu
                        pattern = re.compile('(?s)<tuv.*?lang="'+self.startinglanguage+'".*?>.*?<seg>(.*?)</seg>.*?<tuv.*?lang="'+self.destinationlanguage+'".*?>.*?<seg>(.*?)</seg>')
                        # pattern=re.compile('(?s)<tuv.*?lang="'+self.startinglanguage+'">.*?<seg>(.*?)</seg>.*?<tuv.*?lang="'+self.destinationlanguage+'">.*?<seg>(.*?)</seg>')
                        # pattern=re.compile('(?s)<tuv.*?<seg>(.*?)</seg>.*?<tuv.*?<seg>(.*?)</seg>')
                        present_tu = re.findall(pattern,tu)

                        self.tottus += 1
                        #reject empty segments
                        # print 'present_tu CASE 1', present_tu
                        if present_tu:  # and not present_tu[0][0].startswith("<")
                            present_tu1 = present_tu[0][0].strip()
                            present_tu2 = present_tu[0][1].strip()

                            # Convert character entities to "normal"  characters
                            pattern = re.compile('&gt;', re.U)
                            present_tu1 = re.sub(pattern, '>', present_tu1)
                            present_tu2 = re.sub(pattern, '>', present_tu2)
                            pattern = re.compile('&lt;', re.U)
                            present_tu1 = re.sub(pattern, '<', present_tu1)
                            present_tu2 = re.sub(pattern, '<', present_tu2)
                            pattern = re.compile('&amp;', re.U)
                            present_tu1 = re.sub(pattern, '&', present_tu1)
                            present_tu2 = re.sub(pattern, '&', present_tu2)
                            pattern = re.compile('&quot;', re.U)
                            present_tu1 = re.sub(pattern, '"', present_tu1)
                            present_tu2 = re.sub(pattern, '"', present_tu2)
                            pattern = re.compile('&apos;', re.U)
                            present_tu1 = re.sub(pattern, "'", present_tu1)
                            present_tu2 = re.sub(pattern, "'", present_tu2)

                            present_tu1 = re.sub(r'<ut.*?</ut>', '', present_tu1)
                            present_tu2 = re.sub(r'<ut.*?</ut>', '', present_tu2)
                            present_tu1 = re.sub('<bpt.*?</bpt>', '', present_tu1)
                            present_tu2 = re.sub('<bpt.*?</bpt>', '', present_tu2)
                            present_tu1 = re.sub(r'<ept.*?</ept>', '', present_tu1)
                            present_tu2 = re.sub(r'<ept.*?</ept>', '', present_tu2)
                            present_tu1 = re.sub(r'<ph.*?</ph>', '', present_tu1)
                            present_tu2 = re.sub(r'<ph.*?</ph>', '', present_tu2)
                            present_tu1 = re.sub('^[0-9\.() \t\-_]*$', '', present_tu1)
                            present_tu2 = re.sub('^[0-9\.() \t\-_]*$', '', present_tu2)
                            present_tu1 = re.sub(u"(?im)\u2028", " ", present_tu1)
                            present_tu2 = re.sub(u"(?im)\u2028", " ", present_tu2)
                            present_tu1 = re.sub(u"(?im)\u2029", " ", present_tu1)
                            present_tu2 = re.sub(u"(?im)\u2029", " ", present_tu2)

                            if present_tu1 != present_tu2:
##                                print present_tu1, present_tu2
                                x=len(present_tu1)
##                                print x
                                y=len(present_tu2)
##                                print y
                                if (x <= y*3) and (y <= x*3):
##                                    print "condition true"
                                    ling1=ling1+present_tu1+'\n'
                                    ling2=ling2+present_tu2+'\n'
                                    self.numtus+=1
                            else:
                                self.numequaltus+=1
                        pattern=re.compile('(?s)<tuv.*?lang="'+self.destinationlanguage+'".*?>.*?<seg>(.*?)</seg>.*?<tuv.*?lang="'+self.startinglanguage+'".*?>.*?<seg>(.*?)</seg>')
                        # pattern=re.compile('(?s)<tuv.*?lang="'+self.destinationlanguage+'">.*?<seg>(.*?)</seg>.*?<tuv.*?lang="'+self.startinglanguage+'">.*?<seg>(.*?)</seg>')
                        present_tu=re.findall(pattern,tu)
                        # print 'present_tu CASE 2:', present_tu
                        if present_tu:
                            # print present_tu
                            present_tu1=present_tu[0][1].strip()
                            present_tu2=present_tu[0][0].strip()
                            # Convert character entities to "normal"  characters
                            pattern=re.compile('&gt;',re.U)
                            present_tu1 = re.sub(pattern,'>',present_tu1)
                            present_tu2 = re.sub(pattern,'>',present_tu2)
                            pattern=re.compile('&lt;',re.U)
                            present_tu1=re.sub(pattern,'<',present_tu1)
                            present_tu2=re.sub(pattern,'<',present_tu2)
                            pattern=re.compile('&amp;',re.U)
                            present_tu1=re.sub(pattern,'&',present_tu1)
                            present_tu2=re.sub(pattern,'&',present_tu2)
                            pattern=re.compile('&quot;',re.U)
                            present_tu1=re.sub(pattern,'"',present_tu1)
                            present_tu2=re.sub(pattern,'"',present_tu2)
                            pattern=re.compile('&apos;',re.U)
                            present_tu1=re.sub(pattern,"'",present_tu1)
                            present_tu2=re.sub(pattern,"'",present_tu2)
                            present_tu1 = re.sub('<bpt.*</bpt>', '', present_tu1)
                            present_tu2 = re.sub('<bpt.*</bpt>', '', present_tu2)
                            present_tu1 = re.sub(r'<ept.*</ept>', '', present_tu1)
                            present_tu2 = re.sub(r'<ept.*</ept>', '', present_tu2)
                            present_tu1 = re.sub(r'<ut.*</ut>', '', present_tu1)
                            present_tu2 = re.sub(r'<ut.*</ut>', '', present_tu2)
                            present_tu1 = re.sub(r'<ph.*</ph>', '', present_tu1)
                            present_tu2 = re.sub(r'<ph.*</ph>', '', present_tu2)
                            #Thanks to Gary Daine
                            present_tu1 = re.sub('^[0-9\.() \t\-_]*$', '', present_tu1)
                            #Thanks to Gary Daine
                            present_tu2 = re.sub('^[0-9\.() \t\-_]*$', '', present_tu2)
                            if present_tu1 != present_tu2:
                                x=len(present_tu1)
                                y=len(present_tu2)
                                if (x <= y*3) and (y <= x*3):
                                    ling1=ling1+present_tu1+'\n'
                                    ling2=ling2+present_tu2+'\n'
                                    self.numtus+=1
                            else:
                                self.numequaltus+=1
                    result=(ling1,ling2)
        except:
            self.errortypes=self.errortypes+'   - Extract Language Segments error\n'
        return result

    def locate(self,pattern, basedir):
        """Locate all files matching supplied filename pattern in and below
        supplied root directory.

        @pattern: something like '*.tmx'
        @basedir:whole directory to be treated
        """
        import fnmatch
        for path, dirs, files in os.walk(os.path.abspath(basedir)):
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(path, filename)

    def getallsegments(self):
        """Get all language segments from the TMX files in the specified
        directory

        @self.startinglanguage: something like 'EN-GB'
        @self.destinationlanguage: something like 'FR-FR'
        @fileslist: list of files that should be processed
        @self.inputdir: directory whose files will be treated
        @startfile:output file containing all segments in the @startinglanguage; file
            will be created in @self.inputdir
        @destfile:output file containing all segments in the @destinationlanguage; file
            will be created in @self.inputdir
        @actions:output file indicating the names of all files that were processed without errors; file
            will be created in @self.inputdir
        @self.errortypes: variable that stocks the types of errors detected in the TMX file that is being processed
        @self.presentfile: TMX file being currently processed
        @preptext: parsed XML text with all tags extracted and in string format
        @tus: list that receives the extracted TMX language translation units just with segments of the relevant language pair
        @num: loop control variable between 0 and length of @tus - 1
        @self.numtus: number of translation units extracted so far
        """
        try:
            # Get a list of all TMX files that need to be processed
            fileslist=self.locate('*.tmx',self.inputdir)
            # print(fileslist)
            # Open output files for writing
            startfile=open(os.path.join(self.outputpath, self.startinglanguage+  ' ('+self.destinationlanguage+')_' +self.outputfile),'w+', encoding='utf8')
            destfile=open(os.path.join(self.outputpath, self.destinationlanguage+' ('+self.startinglanguage+')_'+self.outputfile),'w+', encoding='utf8')
            actions=open(os.path.join(self.outputpath, '_processing_info', self.startinglanguage+ '-'+self.destinationlanguage+'_'+'actions_'+self.outputfile+'.txt'),'w+', encoding='utf8')
        except:
            # if any error up to now, add the name of the TMX file to the output file @errors
            self.errortypes=self.errortypes+'   - Get All Segments: creation of output files error\n'
        if fileslist:
            # For each relevant TMX file ...
            for self.presentfile in fileslist:
                self.errortypes=''
                try:
                    print( self.presentfile)
                    fileObj = codecs.open(self.presentfile, "rb", "utf-8","replace",0 )
                    pos=0
                    while True:
                        # read a new chunk of text...
                        preptext = fileObj.read(692141)
                        if not preptext:
                            break
                        last5=''
                        y=''
                        #... and make it end at the end of a translation unit
                        while True:
                            y=fileObj.read(1)
                            if not y:
                                break
                            last5=last5+y
                            if '</tu>' in last5:
                                break
                        preptext=preptext+last5
                        # ... and extract its relevant segments ...
                        if not self.errortypes:
                            # print preptext
                            segs1,segs2=self.extract_language_segments_tmx(preptext)
                            # print 'segs1:', segs1
                            # print 'segs2:', segs2
                            preptext=''
                            #... and write those segments to the output files
                            if segs1 and segs2:
                                # print(segs2)
                                try:
                                    # startfile.write('%s' % (segs1.encode('utf-8','strict')))
                                    # destfile.write('%s' % (segs2.encode('utf-8','strict')))
                                    startfile.write(segs1)
                                    destfile.write(segs2)
                                    # print('%s' % (segs2.encode('utf-8', 'strict')))
                                except Exception as e:
                                    self.errortypes=self.errortypes+'   - Get All Segments: writing of output files error\n'
                                    # print( 'erro')
                                    print(e)
                    #if no errors up to now, insert the name of the TMX file in the @actions output file
                    # print('self.errortypes:', self.errortypes)
                    if self.errortypes=='':
                        try:
                            actions.write(self.presentfile +'\n')
                            self.wroteactions=True
                        except Exception as e:
                            self.errortypes=self.errortypes+'   - Get All Segments: writing of actions file error\n'
                            print(e)
                    fileObj.close()
                except Exception as e:
                    self.errortypes=self.errortypes+'   - Error reading input file\n'
                    print(e)
            try:
                if self.wroteactions:
                    actions.write('\n*************************************************\n\n')
                    actions.write('Total number of translation units: '+str(self.tottus)+'\n')
                    actions.write('Number of extracted translation units (source segment not equal to destination segment): '+str(self.numtus)+'\n')
                    actions.write('Number of removed translation units (source segment equal to destination segment): '+str(self.numequaltus)+'\n')
                    actions.write('Number of empty translation units (source segment and/or destination segment not present): '+str(self.tottus-self.numequaltus-self.numtus) + '\n')
                    actions.write('Value of self.tottus = ' + str(self.tottus) + '; Value of self.numequaltus = ' + str(self.numequaltus) + '; Value of self.numtus = ' + str(self.numtus))

            except Exception as e:
                self.errortypes=self.errortypes+'   - Get All Segments: writing of actions file error\n'
                print(e)
            # Close output files
            actions.close()
            destfile.close()
            startfile.close()

    def SelectDirectory(self):
        """Select the directory where the TMX files to be processed are.

        @result: path returned by dialog window
        @self.inputdir: directory where TMX files to be processed are
                       (and where output files will be written)
        """
        root = tk.Tk()
        root.withdraw()
        result = filedialog.askdirectory()
        if result:
            self.inputdir = result
            self.outputpath = result
            self.outputfile = 'Corpus'
            if not os.path.exists(os.path.join(self.outputpath, '_processing_info')):
                try:
                    os.mkdir(os.path.join(self.outputpath, '_processing_info'))
                except Exception as e:
                    print("The program can't create the directory")
                    print(e)
                    sys.exit()
            return True
        else:
            return False

    def ExtractCorpus(self):
        """Get the directory where TMX files to be processed are, get
        the choice of the pair of languages that will be treated and
        launch the extraction of the corpus

        @self.errortypes: stocks errors detected in TMX file being processed
        @self.presentfile: TMX file being currently processed
        @self.numtus: number of translation units extracted so far
        @self.startinglanguage: something like 'EN-GB'
        @self.destinationlanguage: something like 'FR-FR'
        @self.inputdir: directory whose files will be treated
        @self.outputfile: base name of the resulting corpora files
        @self.errors:output file indicating error in each processed TMX file
        @self.numtus: number of translation units extracted so far
        """

        print('Extract corpus: started at '+strftime('%H-%M-%S'))
        self.errortypes = ''
        self.presentfile = ''
        self.numtus = 0
        self.startinglanguage = 'EN-US'
        self.destinationlanguage = 'RU-RU'
        try:
            self.errors = open(os.path.join(self.outputpath, '_processing_info', self.startinglanguage+ '-'+self.destinationlanguage+'_'+'errors_'+self.outputfile+'.txt'), 'w+', encoding='utf8')
        except Exception as e:
            print(e)
            pass
        # Launch the segment extraction
        self.numtus = 0
        self.getallsegments()
        # if any error up to now, add the name of the TMX file to the output file @errors
        if self.errortypes:
            try:
                self.errors.write(self.presentfile + ':\n' + self.errortypes)
            except Exception as e:
                print(e)
                pass
        try:
            self.errors.close()
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    Extract_TMX_Corpus()
