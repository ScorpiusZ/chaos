#! /usr/bin/env python
import os
import sys
import re
import subprocess

def main ():
    res=os.popen('ls -l').read()
    i=1
    for line in res.split('\n'):
        if i==1:
            i+=1
            continue
        else:
            print "line: %s"%line
            data=re.findall(' *([^ ]*) *',line)
            print data
        i+=1

def main(argv):
  git = subprocess.Popen(["git", "log", "--shortstat", "--reverse",
                        "--pretty=oneline"], stdout=subprocess.PIPE)
  out, err = git.communicate()
  total_files, total_insertions, total_deletions = 0, 0, 0
  for line in out.split('\n'):
    if not line: continue
    if line[0] != ' ':
      # This is a description line
      hash, desc = line.split(" ", 1)
    else:
      # This is a stat line
      data = re.findall(
        ' (\d+) files changed, (\d+) insertions\(\+\), (\d+) deletions\(-\)',
        line)
      if not data:
          continue
      if data[0]:
          print data
          files, insertions, deletions = ( int(x) for x in data[0] )
          total_files += files
          total_insertions += insertions
          total_deletions += deletions
  print "%s: %d files, %d lines" % (hash, total_files,
                                        total_insertions - total_deletions)


if __name__ == '__main__':
  sys.exit(main(sys.argv))


