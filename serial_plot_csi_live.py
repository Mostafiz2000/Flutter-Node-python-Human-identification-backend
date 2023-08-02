import sys
import matplotlib.pyplot as plt
import math
import numpy as np
import os 
import pandas as pd
import collections
from wait_timer import WaitTimer
import randomforest
from read_stdin import readline, print_until_first_csi_line
import requests as rs
import csv
# Set subcarrier to plot
subcarrier = 44
start ="-1"
Option="0"
inputstr="A"
chek="0"
prev_opn="0"
# Wait Timers. Change these values to increase or decrease the rate of `print_stats` and `render_plot`.
print_stats_wait_timer = WaitTimer(0.5)
render_plot_wait_timer = WaitTimer(0.5)

# Deque definition
perm_amp = collections.deque(maxlen=100)
perm_temp=collections.deque(maxlen=100)

perm_phase = collections.deque(maxlen=100)
perm_time = collections.deque(maxlen=100)

# Variables to store CSI statistics
packet_count = 0
total_packet_counts = 0
time_stam = collections.deque(maxlen=100)

# Create figure for plotting
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
fig.canvas.draw()
plt.show(block=False)

mylist = []
mylist1 = []
mylist2 = []
mylist3 = []
mylist4 = []
temp=[]
tf=[]
prev_sum=0

mid_peopple=0
large_people=0
small_people=0
neutral_count=1
normal_count=0

def clear():
 

    df = pd.read_csv("experiment.csv")
    df.drop(df.index[0:], inplace=True)
    df.to_csv("experiment.csv", index=False)
def setdata(a,b):
    
    a.append(b)
    
    # print([a])
    data = [a]
    with open("experiment.csv", "a", newline="") as f:
        writer = csv.writer(f)
    # Write the new row of values to the CSV file
        writer.writerow([a])
def getdata(a,b):
    a.append(b)
    result = randomforest.fun([a])
    newdata ={"foo": "", "kaa":str(result),"max": ""}

    post = rs.post('http://192.168.0.103:4000/postdata', json=newdata)
 
  
def process1(X1,X2,option):
    global prev_opn,temp

    print("Processing.....")
 
    if option == "2":
        clear()
        return
    tempset=[]
    tempset.extend(X2[:,6][0:20].tolist())
    tempset.extend(X2[:,15][0:20].tolist())
    tempset.extend(X2[:,30][0:20].tolist())
    tempset.extend(X2[:,20][0:20].tolist())
    tempset.extend(X2[:,40][0:20].tolist())
    if option == "1":
        setdata(tempset,X1)
    if option == "3":
        getdata(tempset,X1)
        # temp.clear()
    
def carrier_plot(amp,ti,phas,cnt):
    plt.clf()
    
    global p1,p2,p3,p4 , p5, p6 , p7,neutral_count,mid_peopple,large_people,small_people,normal_count,temp
    global mylist , prevlist, perm_temp, mylist2, mylist1, mylist4, mylist3,tf,prev_sum
    myres=[]
    string1=""
    df = np.asarray(amp, dtype=np.int32)
    
    
    normal_count =normal_count+1
    vector = np.vectorize(np.int_)
    df1 = np.asarray(phas, dtype=np.int32)
    # Can be changed to df[x] to plot sub-carrier x only (set color='r' also)
    # for sub in range(6,40):
    plt.plot(range( 100-len(amp), 100), df[:, 6], color='b')
    plt.plot(range( 100-len(amp), 100), df[:, 30], color='r')
    plt.plot(range( 100-len(amp), 100), df[:, 40], color='yellow')
    plt.plot(range( 100-len(amp), 100), df[:, 15], color='black')
    plt.plot(range( 100-len(amp), 100), df[:, 20], color='green')
    result=""

        
         # the POST request 
     
        # normal_count =0
    



    
   
    
    if len(df[:,6])==100:
        # print(vector(mylist))
        print('')

        
        print(mylist)
        if len(mylist)==0:
            if normal_count >= 10:
                mylist=df[:,6]
        else:
            res1= vector(df[:,6]-mylist)

            myres.append(sum(abs(res1)))
            # print(vector(res1), sum(abs(res1)))
            print('')


        if len(mylist1 )==0 :
        
            if normal_count >= 10:
                mylist1=df[:,30]
        else:
            res2= vector(df[:,30]-mylist1)
            myres.append(sum(abs(res2)))
            # print(res2, sum(abs(res2)))
            print('')
        if len(mylist2 )==0:
            if normal_count >= 10:
                mylist2=df[:,15]            
        else:
            res3= vector(df[:,15]-mylist2)
            myres.append(sum(abs(res3)))
            # print(res3, sum(abs(res3)))
            print('')
        if len(mylist3)==0:
            if normal_count >= 10:
                mylist3=df[:,20]
        else:
            res4= vector(df[:,20]-mylist3)
            myres.append(sum(abs(res4)))
           
            print('')
        if len(mylist4 )==0:
            if normal_count >= 10:
                mylist4=df[:,40]
        else:
            res5= vector(df[:,40]-mylist4)
            myres.append(sum(abs(res5)))
            # print(res5, int(sum(abs(res5))))
            print('')

    if(normal_count>=10):

        if(ti[0]<="30.0"):

    
            mylist=(df[:, 6]+mylist*neutral_count)/(neutral_count+1)
            mylist1=(df[:, 30]+mylist1*neutral_count)/(neutral_count+1)
            mylist2=(df[:, 15]+mylist2*neutral_count)/(neutral_count+1)
            mylist3=(df[:, 20]+mylist3*neutral_count)/(neutral_count+1)
            mylist4=(df[:, 40]+mylist4*neutral_count)/(neutral_count+1)
            neutral_count=neutral_count+1       

    if len(myres)>0:
            print(myres)

            if(sum(myres)>prev_sum and Option=="1"):
                prev_sum=sum(myres)
                tf = np.asarray(df, dtype=np.int32)
                print('Observing...')
            if(normal_count%5==0 and Option=="1"):

                process1(inputstr,tf,Option) 
            elif (Option=="3"):
                process1(inputstr,df,Option)
            

    print(ti[0])




    
  


 

            
       
           
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    # plt.xlim(0, 1000)
    plt.ylim(-10,75)
    plt.title(f"Amplitude plot of Subcarrier {subcarrier}")
    # TODO use blit instead of flush_events for more fastness
    # to flush the GUI events
    fig.canvas.flush_events()
    plt.show()
   
   
    


def process(res):
    # 
    global prev_opn,Option,inputstr,chek,prev_sum

    get = rs.get('http://192.168.0.103:4000/getsdata' ) 
    data = get.json()
    # print (data['data1'])
    start=data['data1']
    Option=data['option']
    inputstr=data['str']
    
    chek=data['op']
  
    if(Option!="1"):
        prev_sum=0
    
    if(Option=="2" and prev_opn!=Option):
        process1(inputstr,[1],Option)
        prev_opn=Option
        return
    prev_opn=Option
    if start=="-1":
        return
    all_data = res.split(',')
    csi_data = all_data[25].split(" ")
    time_stam = all_data[23]
    csi_data[0] = csi_data[0].replace("[", "")
    csi_data[-1] = csi_data[-1].replace("]", "")
   
    csi_data.pop()
    csi_data = [int(c) for c in csi_data if c]
    imaginary = []
    real = []
    for i, val in enumerate(csi_data):
        if i % 2 == 0:
            imaginary.append(val)
        else:
            real.append(val)

    csi_size = len(csi_data)
    amplitudes = []
    phases = []
    if len(imaginary) > 0 and len(real) > 0:
        for j in range(int(csi_size / 2)):
            amplitude_calc = math.sqrt(imaginary[j] ** 2 + real[j] ** 2)
            phase_calc = math.atan2(imaginary[j], real[j])
            amplitudes.append(amplitude_calc)
            phases.append(phase_calc)

        perm_phase.append(phases)
        perm_amp.append(amplitudes)
        perm_time.append(time_stam)


print_until_first_csi_line()
prev_time=0
while True:
 
    line = readline()
    if "CSI_DATA" in line:

        process(line)
        packet_count += 1
        total_packet_counts += 1
        
        
        if print_stats_wait_timer.check():
            print_stats_wait_timer.update()
            # print("Packet Count:", packet_count, "per second.", "Total Count:", total_packet_counts)
            packet_count = 0

        if render_plot_wait_timer.check() and len(perm_amp) > 2 and perm_time[0]!=prev_time:
            render_plot_wait_timer.update()
            prev_time=perm_time[0]

            
            
            print("")
            

            carrier_plot(perm_amp,perm_time,perm_phase,0)