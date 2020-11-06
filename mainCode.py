# .... pending work ! add modularity
"""
#   Code Written By : Qazi Arsalan Shah
#   Language Used : Python
#   Tool/IDE/Text Editor : Jupyter and Vscode
#   Libraries used : pandas , jinja2 , weasyprint
#   Requirments : Python 3.6+ , pip or pip3 , Above mentioned libraries

"""
import pandas as pd

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Reading CSV file
filename = "logs_example.csv"
df = pd.read_csv(f"csvfiles/{filename}")

company_logo = "images/nam.png"
# Names of Columns Got 

header = df.columns 
print(f"Columns From CSV : {list(header)}")
# Got Servers Unique in np.array
# Unique servers Array

servers = df["Server"].unique()

# Check For a pattern
# For A particular server write 
# df.loc[df["Server"] == "Name"].loc[df["Notes:"].str.contains("Update|Expanded")]

#Looking for a particular word like update/install

df.loc[df["Notes:"].str.contains("Update|install")]
# print(type(df.loc[df["Server"] == serversList[0]]["Notes:"]))

# Getting List of Servers
serversList = list(servers)
# Minimun Date   .... df["Date"].min()

# Loop through all the list of servers in csv
print("Data Read... !!")
print("Started Generting .... !")
for server in serversList:
      
  # Server Name Got
  firstServer = server 

  # Get Minimun / Earliest Date
  edate = df.loc[df["Server"]== firstServer]["Date"].min()

  edate = edate.split(" ") #splited to get date only
  edate = str(edate[0])

  # Getting List for (update/install) Words
  install = df.loc[df["Server"] == firstServer].loc[df["Notes:"].str.contains("Update|install|update",na=False, case=False)]
  # Getting List form of installs/updates but unique()
  listInstall = list(install["Notes:"].unique())

  # Getting List for (Expanded) Words
  expan = df.loc[df["Server"] == firstServer].loc[df["Notes:"].str.contains("Expanded|expand",na=False, case=False)]
  # Getting List form of expand
  listExpand = list(expan["Notes:"])

# Jinja2 and Weasyprint Stuff For PDF Generation

  env=Environment(loader=FileSystemLoader('.'))

  # import the html template
  template = env.get_template("report.html")

  # Dictionary contains all data passed to pdf
  template_vars={
              'headers':list(serversList),
              'date' : edate,
              'server': firstServer,
              'installs' : listInstall,
              'expands' : listExpand,
              'image' : company_logo
  }

  html_out=template.render(template_vars)
  # Generating names as "servername_report.pdf"

  pdf_name=f'Reports/{firstServer}_report.pdf'
  

  # Conversion of HTML to PDF
  
  HTML(string=html_out, base_url='.').write_pdf(pdf_name,stylesheets = ["mystyle.css","bootstrap.css"])
  print(f"{firstServer} , Report Generated")
print("Work, Done ... !!")
