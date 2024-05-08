from typing import Set
import numpy as np
import re
import operator

#=========================================================

path = "/home/wang888/gaSNN0417/FromSlurm/gaSNN/experiment/800/5/" #存放資料的路徑

#=========================================================  
TempAcc = []
Save_All_Acc = []
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct
for i in range (1, 801):
    with open(f'{path}/{i}/Accuracy_v2.txt', 'r') as fp:
        TemAcc = fp.readline() 
        NumAcc = re.sub(u"([^\u0030-\u0039\u002e])", "", TemAcc)   #去掉除了小數點和數字以外的符號
        Save_All_Acc.append(i)
        Save_All_Acc.append(NumAcc)
#print("最終結果:", not_picked) 
#Sorted_Saved = sorted(Save_All_Acc.items(), key=operator.itemgetter(1),reverse=True) #進行排序
Convert_All_Acc = Convert(Save_All_Acc) 
Last_Sorted_Acc = sorted(Convert_All_Acc.items(), key=operator.itemgetter(1),reverse=True)
print("最終全體準確度:", Last_Sorted_Acc)
with open(f'{path}/ALL.txt', 'w') as fp:
        fp.writelines(str(Last_Sorted_Acc)+'\n') 
