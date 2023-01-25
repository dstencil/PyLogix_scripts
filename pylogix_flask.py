from flask import Flask, render_template
from pylogix import PLC
import time
from datetime import datetime
import csv
import pandas as pd

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


if __name__ == '__main__':
    app.run(debug=True)
