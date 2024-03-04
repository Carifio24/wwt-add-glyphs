#!/bin/sh

# Stolen from https://www.imagemagick.org/Usage/text/#font_info
convert -debug annotate  xc: -font micross.ttf -pointsize ${1} -annotate 0 ${2} null
