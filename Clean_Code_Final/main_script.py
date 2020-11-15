"""
#   Code Written By : Qazi Arsalan Shah
#   Language Used : Python
#   Tool/IDE/Text Editor : Jupyter and Vscode
#   Libraries used : pandas , jinja2 , weasyprint
#   Requirments : Python 3.6+ , pip or pip3 , Above mentioned libraries
#   Main Script that Reads CSV File using pandas, 
#   Does all strings searching etc stuff and Regex matching stuff
#   Then Places all HTML reports for each server in HTMLS/ directory

"""
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


# Reading CSV file
# Write CSV file name here and place your csv file in (csvfiles/) Directory

filename = "logs_example.csv"
df = pd.read_csv(f"csvfiles/{filename}")
# Place company's logo in images/ directory and write its name in company_logo
company_logo = "nam.png"
company_logo = f"images/{company_logo}"

headers = df.columns 

# Got Servers Unique in np.array
# Unique servers Array
servers = df["Server"].unique()
# Getting List of Servers
serversList = list(servers)


print("Data Read... !!")
print("Started Generting HTML .... !")

# Place anyother string here for matching ...
matching = ["Security Update for Adobe Flash Player",
            "Security Update for Microsoft .NET Framework 3.5 on Windows Server 2012 R2",
            "Security Update for Windows Server 2012 R2",
            "Windows Malicious Software Removal Tool",
            "Cylance updated",
            "Security and Quality Rollup for .NET Framework",
            "Servicing Stack Update for Windows Server 2012 R2"
           ]

matching_lowered = [x.lower() for x in matching]
# Loop through servers list
# Generate Report For each server
# Main loop over servers
for server in serversList:
      
  # Got our server from server list
  firstServer = server 
  
  # These two lists are passed to our html
  summary = []
  os_patch = []

  # Get Minimun / Earliest Date
  edate = df.loc[df["Server"]== firstServer]["Date"].min()
  edate = edate.split(" ") #splited to get date only
  edate = str(edate[0])

  # Main logic for string matching
  # Loop through the matching list, look for each bullet , if it exists in notes, then add
  # Summarized list in list(summary) and detailed Notes: in list(os_patch) 
  # Regex is created : 
  for bullet in matching:
    res = df.loc[df["Server"] == firstServer].loc[df["Notes:"].str.contains(f"^.*{bullet}.*",na=False, case=False)==True]
    if not res.empty:
      summary.append(bullet)
      os_patch.extend(list(res["Notes:"]))
  
 
# Jinja2 and Weasyprint Stuff For HTML Generation
  env=Environment(loader=FileSystemLoader('.'))

  # import the html template
  template = env.get_template("main_template.html")

  # Dictionary contains all data passed to pdf
  # Mr Salar you can simply place anything that you want to pass to HTML 
  template_vars={
              'headers':list(serversList),
              'date' : edate,
              'server': firstServer,
              'summary' : list(summary),
              'os_patch' : list(os_patch),
              'image' : company_logo
  }

  html_out=template.render(template_vars)
  
  # Save HTML in HTMLS/ 
  file_name=f'HTMLS/{firstServer}_html.html'
  with open(file_name, 'w') as fh:
    fh.write(html_out)
  print(f"{firstServer} ,HTML Generated")

  # Commented out PDF Generation code
  # pdf_name=f'Reports/{firstServer}_report.pdf'
  

  # # Conversion of HTML to PDF
  
  # HTML(string=html_out, base_url='.').write_pdf(pdf_name,stylesheets = ["mystyle.css","bootstrap.css"])
  # print(f"{firstServer} , Report Generated")

print("HTMLS generated For each server report....!!")
print("Now Run PDF generation script to generate PDF in Reports/")
print("Bootstrap.css and mycustom.css files are dynamically linked for Styling")
print("When you will run pdf script, it will automatically add styling")

