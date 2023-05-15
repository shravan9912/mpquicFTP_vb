import os
import subprocess
import csv
import pandas as pd
path1_bw=1
path2_bw=1
path1_delay=1
path2_delay=1
path1_loss=1
path2_loss=1
scheduler_name="rr"
itfc1='h1-eth0'
itfc2='h1-eth1'
no_of_itr=1
file_adrr=""
file_size=''
gc=-1
results = pd.read_csv('inputfile.csv')
count=len(results)-1


def get_config_csv(file_adrr):
    global gc
    gc=gc+1
    global path1_bw
    global path1_bw
    global path2_bw  
    global path1_delay
    global path2_delay
    global path1_loss
    global path2_loss
    global scheduler_name
    global no_of_itr
    global file_size
    with open('inputfile.csv', mode='r') as csv_file:
         csv_reader = csv.DictReader(csv_file)
         rows = list(csv_reader)
         print(rows[gc]['path1_bw'])
         path1_bw=rows[gc]['path1_bw']
         path2_bw=rows[gc]['path2_bw']
         path1_delay=rows[gc]['path1_delay']
         path2_delay=rows[gc]['path2_delay']
         path1_loss=rows[gc]['path1_loss']
         path2_loss=rows[gc]['path2_loss']
         scheduler_name=rows[gc]['scheduler_name']
         no_of_itr=rows[gc]['no_of_itr']
         file_size=rows[gc]['file_size']



def apply_nw_conditions():#path1_bw,path2_bw,path1_delay,path2_delay,path1_loss,path2_loss):
  print("applying netem conditions-------Starts.....")
  os.system('tc qdisc change dev '+ itfc1 + " root netem delay " +path1_delay+" loss " +path1_loss+" rate "+path1_bw) #add netem code for itfr1
  os.system('tc qdisc change dev '+ itfc2 + " root netem delay " +path2_delay+" loss " +path2_loss+" rate "+path2_bw) #add netem code for itfr2
  print("netem comndtitions applied------Done...")
 
def parsedatatocsv():
         seco=''
         mylines = []
         sindex=0;                                # Declare an empty list.
         with open ('raw.txt', 'rt') as myfile:    # Open lorem.txt for reading text.
              for myline in myfile:                   # For each line in the file,
                  mylines.append(myline.rstrip('\n')) # strip newline and add to list.
              for element in mylines:                     # For each element in the list,
               if element.find("Time Taken To Download File:")>1:
                    sindex=element.find("Time Taken To Download File:")
                    #print(sindex)  
                    #print(element[sindex+29:sindex+36])
                    seco=element[sindex+29:sindex+36]
         rows = [ [path1_bw,path1_bw,path2_bw, path1_delay,path2_delay,path1_loss,path2_loss, scheduler_name,no_of_itr,file_size,seco]] 
         with open('outputfile.csv', 'a') as csvfile:
              csvwriter = csv.writer(csvfile)
              csvwriter.writerows(rows)
  
'''def getIntfc():
    #am,os.system("ifconfig -a | sed 's/[ \t].*//;/^\(lo\|\)$/d'")
    am=subprocess.check_output("ifconfig -a | sed 's/[ \t].*//;/^\(lo\|\)$/d'",shell=True)
    print("Itfc")
    am=str(am)
    am=am.replace(':','')
    print(am)
    amm=list(map(str.strip,am.split('\\')))
    print(amm[0])'''

def do_client_action():
    print("do_client_action----starts....")
    os.system('client/./client --scheduler='+scheduler_name+' --action=2 --file_name='+file_size+'.txt')
    parsedatatocsv()
    print("client_action----done....")

while(gc<count):
  print("row value "+str(gc))
  get_config_csv("inputfile.csv")
  apply_nw_conditions()
  print(path1_bw)
  print(path2_bw)
  print(path1_delay)
  print(path2_delay)
  print(path1_loss)
  print(path1_loss)
  print(scheduler_name)  
  print(no_of_itr)
  print(count)
  n=1
  while(n<=int(no_of_itr)):
    do_client_action()
    n=n+1
