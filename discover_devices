from pylogix import PLC
import time
from datetime import datetime
import csv
import pandas as pd

now = datetime.now()

with PLC() as comm:
    
    #comm.IPAddress = input('Enter Device Ip Address: ')
    devices = comm.Discover()
    dictionary = {}
    fieldnames = ['IP Address', 'Product Name','Vendor','Revision','Serial Number']
    read = True
    Micro800 = True
    
    with open('devicestore.csv', 'w') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        f.writerow(fieldnames)
        for device in devices.Value:
            
            f.writerow([device.IPAddress, device.ProductName, device.Vendor, device.Revision, device.SerialNumber]) 
          
       
        print('Done')
