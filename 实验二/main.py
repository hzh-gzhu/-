import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as plt
import heapq
merge=pd.read_csv('合并数据.csv',encoding='gbk')
x_values = merge['C1']
y_values = merge['Constitution']
plt.scatter(x_values, y_values, s=50)
plt.xlabel('C1', fontsize=14)
plt.ylabel('Constitution', fontsize=14)
plt.show()
plt.hist(x=merge['C1'],bins=8,edgecolor = 'black',range=[60,100])
plt.xlabel('C1 mark', fontsize=14)
plt.ylabel('time', fontsize=14)
plt.show()
for i in range(6,11):
    a = "C" + str(i)
    merge[a] = merge[a].apply(lambda x:x*10)
knowledge_mean = 0

pe_grade = merge['Constitution'].tolist()
pe_mean = sum(pe_grade) / len(pe_grade)
each_pe_mean=merge['Constitution'].apply(lambda x:x-pe_mean)
std_pr = pow(pow(each_pe_mean, 2).sum() / 105, 0.5)  # 体育成绩的方差
each_pe_mean = merge['Constitution'].apply(lambda x:(x-pe_mean)/std_pr)

each_mean = np.array([[0.0]*len(each_pe_mean)]*len(each_pe_mean))
for x in range(0,len(each_pe_mean)):
    each_mean[0][x] = round(each_pe_mean[x],3)


for i in range(1,10):
    a = "C" + str(i)
    knowledge_grade = merge[a].tolist()
    knowledge_mean = sum(knowledge_grade) / len(knowledge_grade)
    each_aca_mean=merge[a].apply(lambda x:x-knowledge_mean)
    std_aca = pow(pow(each_aca_mean, 2).sum() / 105, 0.5)
    each_aca_mean=merge[a].apply(lambda x:(x-knowledge_mean)/std_aca)
    for x in range(0, len(each_aca_mean)):
        each_mean[i][x] =  round(each_aca_mean[x],3)

# for i in range(0,10):
#     for j in range(0,len(each_pe_mean)):
#         print(each_mean[i][j],end=" ")
#     print()

correlation_matrix = np.array([[0.0]*len(each_pe_mean)]*len(each_pe_mean))

for i in range(0,len(each_pe_mean)):
    for j in range(0,len(each_pe_mean)):
        correlation = 0
        for x in range(0,10):
            correlation= correlation+each_mean[x][i]*each_mean[x][j]
        correlation_matrix[i][j] = round(correlation,3)


np.savetxt("correlation_matrix.txt",correlation_matrix,fmt="%d")


plt.matshow(correlation_matrix,cmap=plt.get_cmap('Greens'), alpha=10000)  # , alpha=0.3
plt.show()

correlation_sample = np.array([[0]*3]*len(each_pe_mean))

for i in range(0,len(each_pe_mean)):
    max1_index = np.argmax(correlation_matrix[i])
    max1_num = np.amax(correlation_matrix[i])
    correlation_matrix[i][max1_index] = -1e9
    max2_index = np.argmax(correlation_matrix[i])
    max2_num = np.amax(correlation_matrix[i])
    correlation_matrix[i][max2_index] = -1e9
    max3_index = np.argmax(correlation_matrix[i])
    max3num = np.amax(correlation_matrix[i])
    correlation_matrix[i][max2_index] = max2_num
    correlation_matrix[i][max1_index] = max1_num
    correlation_sample[i][0] = merge['ID'][max1_index]
    correlation_sample[i][1] = merge['ID'][max2_index]
    correlation_sample[i][2] = merge['ID'][max3_index]


np.savetxt("最近样本.txt",correlation_sample,fmt="%d")




