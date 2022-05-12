from pylogix import PLC
import time
from datetime import datetime
import csv
import pandas as pd

now = datetime.now()
isMicro = input('Is this a Micro800?')
with PLC() as comm:
    
    comm.IPAddress = input('Enter Device Ip Address: ')
    programs = comm.GetProgramsList()   
    comm.Micro800 = isMicro
    fieldnames = ['Program Name:', 'IP Address:']
    with open('programstore.csv', 'w') as f:
        f = csv.writer(f, delimiter=',', lineterminator = '\n', quotechar='/',quoting=csv.QUOTE_MINIMAL)
        f.writerow(fieldnames)
        for p in programs.Value:
            
            f.writerow([p, str(comm.IPAddress)]) 
          
       
        print("success your list of programs have saved")
