from flask import Flask, render_template
from pylogix import PLC
import time
from datetime import datetime
import csv
import pandas as pd
import os


##### initializing folders needed 

# Create the data folder if it does not exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('templates'):
    os.makedirs('templates')
if not os.path.exists('static'):
    os.makedirs('static')
 

# Create the devicestore.csv file if it does not exist
if not os.path.exists('data/devicestore.csv'):
    with open('data/devicestore.csv', 'w') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        fieldnames = ['IP Address', 'Product Name','Vendor','Revision','Serial Number', 'DeviceID']
        f.writerow(fieldnames)

# Create the programstore.csv file if it does not exist
if not os.path.exists('data/programstore.csv'):
    with open('data/programstore.csv', 'w') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        fieldnames = ['Program Name:', 'IP Address:']
        f.writerow(fieldnames)

# Create the tagstore.csv file if it does not exist
if not os.path.exists('data/tagstore.csv'):
    with open('data/tagstore.csv', 'w') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        fieldnames = ['Tag Name', 'IP Address']
        f.writerow(fieldnames)
# Create the devices.html file if it does not exist
if not os.path.exists('templates/devices.html'):
    with open('templates/devices.html', 'w') as f:
        f.write('<html>\n')
        f.write('    <head>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="../static/style.css">\n')
        f.write('        <title>Discovered Devices</title>\n')
        f.write('    </head>\n')
        f.write('    <body>\n')
        f.write('    <ul>\n')
        f.write('    <li><a href="/discover_devices">Discover Devices</a></li>\n')
        f.write('    <li><a href="/read_programs">Read Programs</a></li>\n')
        f.write('    <li><a href="/read_tags">Read Tags</a></li>\n')
        f.write('    </ul>\n')
        f.write('        <h1>Discovered Devices</h1>\n')
        f.write('        <pre>{{ devices }}</pre>\n')
        f.write('    </body>\n')
        f.write('</html>\n')

# Create the programs.html file if it does not exist
if not os.path.exists('templates/programs.html'):
    with open('templates/programs.html', 'w') as f:
        f.write('<html>\n')
        f.write('    <head>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="../static/style.css">\n')
        f.write('        <title>Programs</title>\n')
        f.write('    </head>\n')
        f.write('    <body>\n')
        f.write('    <ul>\n')
        f.write('    <li><a href="/discover_devices">Discover Devices</a></li>\n')
        f.write('    <li><a href="/read_programs">Read Programs</a></li>\n')
        f.write('    <li><a href="/read_tags">Read Tags</a></li>\n')
        f.write('    </ul>\n')
        f.write('        <h1>Programs</h1>\n')
        f.write('        <pre>{{ programs }}</pre>\n')
        f.write('    </body>\n')
        f.write('</html>\n')

# Create the tags.html file if it does not exist
if not os.path.exists('templates/tags.html'):
    with open('templates/tags.html', 'w') as f:
        f.write('<html>\n')
        f.write('    <head>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="../static/style.css">\n')
        f.write('        <title>Tags</title>\n')
        f.write('    </head>\n')
        f.write('    <body>\n')
        f.write('    <ul>\n')
        f.write('    <li><a href="/discover_devices">Discover Devices</a></li>\n')
        f.write('    <li><a href="/read_programs">Read Programs</a></li>\n')
        f.write('    <li><a href="/read_tags">Read Tags</a></li>\n')
        f.write('    </ul>\n')
        f.write('        <h1>Tags</h1>\n')
        f.write('        <pre>{{ tags }}</pre>\n')
        f.write('    </body>\n')
        f.write('</html>\n')
#flask app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/discover_devices', methods=['POST'])
def discover_devices():
    now = datetime.now()
    with PLC() as comm:
        devices = comm.Discover()
        dictionary = {}
        fieldnames = ['IP Address', 'Product Name','Vendor','Revision','Serial Number', 'DeviceID']
        read = True
        comm.Micro800 = False

        with open('devicestore.csv', 'w') as f:
            f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
            f.writerow(fieldnames)
            for device in devices.Value:
                f.writerow([device.IPAddress, device.ProductName, device.Vendor, device.Revision, device.SerialNumber,device.DeviceID]) 
              
           
            return dictionary
        
    # Read the CSV file
    df = pd.read_csv('devicestore.csv')

    # Create the HTML string to display the data
    html_string = ''
    for index, row in df.iterrows():
        html_string += 'IP Address: ' + row['IP Address'] + '\n'
        html_string += 'Product Name: ' + row['Product Name'] + '\n'
        html_string += 'Vendor: ' + row['Vendor'] + '\n'
        html_string += 'Revision: ' + row['Revision'] + '\n'
        html_string += 'Serial Number: ' + row['Serial Number'] + '\n'
        html_string += 'DeviceID: ' + row['DeviceID'] + '\n\n'

    # Pass the HTML string to the template
    return render_template('devices.html', devices=html_string)


@app.route('/read_programs', methods=['POST'])
def read_programs():
    df = pd.read_csv('devicestore.csv')
    programs = []

    for index, row in df.iterrows():
        comm.IPAddress = row['IP Address']
        program = comm.GetProgramsList()
        for p in program.Value:
            programs.append({'Program Name': p, 'IP Address': str(comm.IPAddress)})

    with open('programstore.csv', 'w') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        f.writerow(fieldnames)
        for program in programs:
            f.writerow([program['Program Name'], program['IP Address']]) 

    return 'Programs stored to CSV file.'
@app.route('/read_tags', methods=['POST'])
def read_tags():
    df = pd.read_csv('devicestore.csv')
    tags = []

    for index, row in df.iterrows():
        comm.IPAddress = row['IP Address']
        taglist = comm.Read('TagList', 1)
        for tag in taglist.Value:
            tags.append({'Tag Name': tag, 'IP Address': str(comm.IPAddress)})

    with open('tagstore.csv', 'w') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        f.writerow(fieldnames)
        for tag in tags:
            f.writerow([tag['Tag Name'], tag['IP Address']]) 

    return 'Tags stored to CSV file.'
    # Read the CSV file
df = pd.read_csv('tagstore.csv')

# Create the HTML string to display the data
html_string = '<table>'
html_string += '<tr>'
html_string += '<th>Tag Name</th>'
html_string += '<th>IP Address</th>'
html_string += '</tr>'
for index, row in df.iterrows():
    html_string += '<tr>'
    html_string += '<td>' + row['Tag Name'] + '</td>'
    html_string += '<td>' + row['IP Address'] + '</td>'
    html_string += '</tr>'
html_string += '</table>'

# Pass the HTML string to the template
return render_template('tags.html', tags=html_string)
if __name__ == '__main__':
    app.run(debug=True)
