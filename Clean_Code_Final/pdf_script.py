# This Scripts Simply Scans HTMLS directory and gets list of all files here
# Don't place anyother file in HTMLS directory

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pathlib
from pathlib import Path
import os
# Getting files from HTMLS directory
os.listdir(path='.')
def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
                
    return listOfFile


outpath = Path.cwd()
# outpath == current working directory 
outpath = str(outpath)
outpath = outpath + "/HTMLS"
# Now output is /HTMLS/

listOfFiles = getListOfFiles(outpath)
#print(listOfFiles)
for server in listOfFiles:
    pdf_name = f"Reports/{server}_report.pdf"
    HTML(f"HTMLS/{server}", base_url='.').write_pdf(pdf_name,stylesheets = ["mystyle.css","bootstrap.css"])
    print(f"{server} PDF Report Generated .. !")
