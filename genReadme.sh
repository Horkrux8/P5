#!/bin/bash
cd /home/lennart/backup/vscode/github/P5
rm README.html README.docx README.pdf
pandoc -s -o READMEs/README.pdf README.md
pandoc -s -o READMEs/README.html README.md
pandoc -s -o READMEs/README.docx README.md