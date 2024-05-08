import os
import random
from typing import Set
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import time
import json
import copy
import re
import operator

start = time.time()
with open('/home/wang888/gaSNN0417/chromosomes.json') as fp:    #存放json檔案的路徑
    new_parameter_values = {k: v for k, v in json.load(fp).items() if len(v) > 0}
with open('/home/wang888/gaSNN0417/parameters.py') as fp:       #存放參數py檔案的路徑
    original_code = fp.readlines()
docker1 = "docker run -i -v /home/wang888/gaSNN0417/data/"      
#docker run指令-v後是本機檔案的路徑
docker2 = ":/app/data snn0417 python3 /app/learning.py"
#/app/data為容器路徑接著為image名稱和執行檔案
#世代數量
generation = 10
#chromosome數量
chrNum = 10 #需要2的倍數兩兩交配才不會出錯
croPro = 85 #crossoverprobability交配機率
mutPro = 5  #mutationprobability突變機率
path = "/home/wang888/gaSNN0417/data/" #存放資料的路徑
#probabilityCutoff = [0,30,55,75,90,100]   #機率數量為chrNum+1個
#[0,30,55,75,90,100]前面的機率應該要比較高比較容易選到[0,10,20,30,40,50,60,70,80,90,100] 
#print(len(probabilityCutoff))
listgeneSet = list(new_parameter_values.keys()) 
#=========================================================
probabilityCutoff = []
x= 0
for i in range (0, chrNum+1):
    probabilityCutoff.append(x)
    x +=(chrNum-i)*(chrNum-i+1)
print (probabilityCutoff)

def population (chrNum):
    generation =  []
    for i in range(0,chrNum):
        chri = []
        for j in range (0, len(new_parameter_values)):
            new_value=new_parameter_values.get(listgeneSet[j])
            get_num = np.random.randint(0,len(new_parameter_values[listgeneSet[j]]))
            new_chrom = new_value[get_num]
            chri.append(new_chrom)
        print ("染色體",i+1,":",chri)
        generation.append (chri)

    return generation
# tournament selection
def selection (l: list,probabilityCutoff):  # l是染色體的list
    def rand():
        n = np.random.randint(0, probabilityCutoff[len(probabilityCutoff)-1])
        for i in range (0, len(probabilityCutoff)-1):
            if probabilityCutoff[i] <= n < probabilityCutoff[i+1]:
                return i       

    v = []
    while len(v) < chrNum:
        x = rand()
        if x not in v:
            v.append(x)
    g = []
    while len(v)>0:
       v_x = v.pop(0) 
       v_y = l[v_x]
       g.append(v_y)
    
    return g 
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct
# mutation operator
def mutation(c1, c2):
        # check for a mutation
    if np.random.randint(0,100) < mutPro:
        z = np.random.randint(0,len(new_parameter_values))
        print ("突變的位數為第",z+1,"位")
        for i in range (0,len(new_parameter_values)):
            new_value=new_parameter_values.get(listgeneSet[i])
            if z==i:
                get_num = np.random.randint(0,len(new_parameter_values[listgeneSet[i]]))
                new_chrom = new_value[get_num]
                print ("突變後的數字為",new_chrom)         
                c1[i] = c2[i] = new_chrom
                return [c1, c2]
    else:
        print ("沒有發生突變")
        return [c1, c2]
# genetic algorithm
print ("選擇",len(new_parameter_values),"個基因組成一個染色體，總共會有",chrNum,"個染色體以下為其基因參數")
for i in range(0, len(new_parameter_values)):
    print (i+1,".",listgeneSet[i],new_parameter_values[listgeneSet[i]])
first_generation = population (chrNum)
print ("population=",first_generation)
# with open('/home/ccllab/gaSNN/SNN_50/parameters.py') as fp:
#     original_code = fp.readlines()
#     for i in original_code:
#         print(i)
parameter_transfer = []
first_generation_backup = []
first_generation_backup = copy.deepcopy(first_generation)
init = []
TempAcc = []
Save_All_Acc = []
#for i in range(chrNum):
   #first_generation_backup.extend(first_generation) 
for i in range (1, chrNum+1):
    new_code = []
    parameter_transfer = first_generation_backup.pop(0)
    print (first_generation)
    #i = 0
    for line in original_code:
        new = False
        for k, v in new_parameter_values.items():
            if line.split('=')[0].strip() == k:            
                new_value = parameter_transfer.pop(0)
                print (new_value)
                new_code.append(f'    {k} = {new_value}\n')        
                new = True
                #i += 1
        if not new:
            new_code.append(line)
#for i in new_code:
    #print(i)
#    path = "/home/ccllab/gaSNN/data50/"
    file_name = path + str(i)
    os.mkdir(file_name) 
    #new_file_name = input("請輸入新檔名:") or "parameters"
    new_file_name = "parameters"
    with open(f'{path}/{i}/{new_file_name}.py', 'w') as fp:
        fp.writelines(new_code) 
    with open(f'{path}/{i}/__init__.py', 'w') as fp:
        fp.writelines('# -*- coding: utf-8 -*-') 
    #with open(f'{new_file_name}.py', 'w') as fp:
        #fp.writelines(new_code) 
    # p1 = "docker run -i -v /home/ccllab/gaSNN/data50/"
    # p2 = ":/app/data onlysnn python3 /app/learning.py"
    docker =  docker1 + str(i) + docker2
    os.system(docker)
    new_path = path + str(i)+'/Accuracy_v2.txt'
    isExist = os.path.exists(new_path)
    if not isExist: 
        with open(f'{path}/{i}/Accuracy_v2.txt', 'a') as fp:
            fp.write("0")     

for i in range (1 , chrNum+1):
    with open(f'{path}/{i}/Accuracy_v2.txt', 'r') as fp:
        TemAcc = fp.readline() 
        NumAcc = re.sub(u"([^\u0030-\u0039\u002e])", "", TemAcc)   #去掉除了小數點和數字以外的符號
        Save_All_Acc.append(i)
        Save_All_Acc.append(NumAcc)
        TempAcc.append(i-1)
        TempAcc.append(NumAcc)
AllAcc = Convert(TempAcc)   #改成dict形式
Sorted_AllAcc = sorted(AllAcc.items(), key=operator.itemgetter(1),reverse=True) #進行排序
#Save_All_Acc = Sorted_AllAcc
print ("染色體當前順序=",Sorted_AllAcc)
LastAcc = []                    #存取排序後前面的數字也就是第幾個染色體
for i in range (0 , chrNum):
    a = Sorted_AllAcc[i]
    LastAcc.append(a[0])        
Generationn_Accuracy = []
for i in range (0 , chrNum):
    Generationn_Accuracy.append(first_generation[LastAcc[i]])


# tournament selection
print ("==================================================================================================================")
for j in range(2,generation+1):
    print ("第",j,"世代:")
    print ("染色體排名=",Generationn_Accuracy)
#    p1, p2, p3, p4 = selection (Generationn_Accuracy,probabilityCutoff)
 #   New_Pop = [p1, p2, p3, p4]
    New_Pop = selection (Generationn_Accuracy,probabilityCutoff)
    All_pop = []
    for i in range (0, chrNum//2):
        p1 = New_Pop.pop(0)
        p2 = New_Pop.pop(0)
        if np.random.randint(0,100) < croPro:
            print ("父親=",p1)
            print ("母親=",p2)
            pt = np.random.randint(1, len(new_parameter_values))
            print ("交換的位置:",pt)
            c1 = list()
            c2 = list()
            c1.extend(p1[0:pt])
            c1.extend(p2[pt:])
            c2.extend(p2[0:pt])
            c2.extend(p1[pt:])
            print ("c1=",c1)
            print ("c2=",c2)

            print ("==================================================================================================================")
        else:
            print ("沒有發生交配")
            c1 = list()
            c2 = list()
            c1.extend(p1)
            c2.extend(p2)
        print ("==================================================================================================================")
        m1 = list(c1)
        m2 = list(c2)
        m1, m2 = mutation(m1, m2)
        print ("新的子代:",m1,m2)
        All_pop.append(m1) 
        All_pop.append(m2) 
    print ("==================================================================================================================")
#    with open('/home/ccllab/gaSNN/SNN_50/parameters.py') as fp:
#        original_code = fp.readlines()
    #for i in original_code:
        #print(i)
    parameter_transfer = []
    second_generation_backup = []
    second_generation_backup = copy.deepcopy(All_pop)
    init = []
    TempAcc = []
    c = j-1
    for i in range (chrNum*c+1, chrNum*j+1):
        new_code = []
        parameter_transfer = second_generation_backup.pop(0)
        for line in original_code:
            new = False
            for k, v in new_parameter_values.items():
                if line.split('=')[0].strip() == k:            
                    new_value = parameter_transfer.pop(0)
                    print (new_value)
                    new_code.append(f'    {k} = {new_value}\n')        
                    new = True
                #i += 1
            if not new:
                new_code.append(line)
#        path = "/home/ccllab/gaSNN/data50/"
        file_name = path + str(i)
        os.mkdir(file_name) 
        #new_file_name = input("請輸入新檔名:") or "parameters"
        new_file_name = "parameters"
        with open(f'{path}/{i}/{new_file_name}.py', 'w') as fp:
            fp.writelines(new_code) 
        with open(f'{path}/{i}/__init__.py', 'w') as fp:
            fp.writelines('# -*- coding: utf-8 -*-') 
    #with open(f'{new_file_name}.py', 'w') as fp:
        #fp.writelines(new_code) 
        # p1 = "docker run -i -v /home/ccllab/gaSNN/data50/"
        # p2 = ":/app/data onlysnn python3 /app/learning.py"
        docker =  docker1 + str(i) + docker2
        os.system(docker)
        new_path = path + str(i)+'/Accuracy_v2.txt'
        isExist = os.path.exists(new_path)
        if not isExist: 
            with open(f'{path}/{i}/Accuracy_v2.txt', 'a') as fp:
                fp.write("0")     
    for i in range (chrNum*c+1, chrNum*j+1):
        with open(f'{path}/{i}/Accuracy_v2.txt', 'r') as fp:
            TemAcc = fp.readline() 
            NumAcc = re.sub(u"([^\u0030-\u0039\u002e])", "", TemAcc)   #去掉除了小數點和數字以外的符號
            Save_All_Acc.append(i)
            Save_All_Acc.append(NumAcc)
            TempAcc.append(i-chrNum*c-1)
            TempAcc.append(NumAcc)
    AllAcc = Convert(TempAcc)   #改成dict形式
    Sorted_AllAcc = sorted(AllAcc.items(), key=operator.itemgetter(1),reverse=True) #進行排序
    #Save_All_Acc.append(Sorted_AllAcc) 
    print ("染色體當前順序=",Sorted_AllAcc)
    LastAcc = []                    #存取排序後前面的數字也就是第幾個染色體
    for i in range (0 , chrNum):
        a = Sorted_AllAcc[i]
        LastAcc.append(a[0])        
    Generationn_Accuracy = []
    for i in range (0 , chrNum):
        Generationn_Accuracy.append(All_pop[LastAcc[i]])

#print("最終結果:", not_picked) 
#Sorted_Saved = sorted(Save_All_Acc.items(), key=operator.itemgetter(1),reverse=True) #進行排序
Convert_All_Acc = Convert(Save_All_Acc) 
Last_Sorted_Acc = sorted(Convert_All_Acc.items(), key=operator.itemgetter(1),reverse=True)
print("最終全體準確度:", Last_Sorted_Acc)
end = time.time()
print("The time of execution of above program is :",
      (end-start)/3600, "h")
with open(f'{path}/ALL.txt', 'w') as fp:
        fp.writelines(str(Last_Sorted_Acc)+'\n') 
        fp.writelines("The time of execution of above program is :") 
        fp.writelines(str((end-start)/3600)) 
        fp.writelines("h") 
        