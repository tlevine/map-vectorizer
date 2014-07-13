#!/usr/bin/env python
'''
i would like to add a command-line parameter where you could opt to not                                 
execute the opencv part of the script (eg. vectorize input.tif                                          
--without-opencv)                                                                                       
                                                                                                        
i also want to add a command-line parameter to *not* delete temporary files                             
(they are very useful for debugging)... right now i comment out lines                                   
477-485 every time i want to keep them:                                                                 
                                                                                                        
https://github.com/NYPL/map-vectorizer/blob/9b9129b9d135c89b350700549794e7d0f2348af2/vectorize_map.py#L4
+77                    
'''

import argparse
parser = argparse.ArgumentParser('Map polygon and feature extractor')
parser.add_argument('--without-opencv', dest = 'opencv', action = 'store_false')
parser.add_argument('--keep-temporary-files', '-k', action = 'store_true')
result = parser.parse_args()
print('OpenCV: %s' % result.opencv)
print('Temporary Files: %s' % result.keep_temporary_files)
