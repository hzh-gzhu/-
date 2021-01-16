import pandas as pd
import xlrd
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
one=pd.read_csv('学生数据1.txt',encoding='gbk')
one['C10']=one['C10'].fillna(0) #将c0为空的属性全部添加为0
Gender=one['Gender'].tolist()
for i in range(len(Gender)):  #将female变为girl male变为boy
    if Gender[i]=='female':
        Gender[i] = 'girl';
    if Gender[i]=='male':
        Gender[i] = 'boy';
one['Gender'] = Gender
one['Height'] = one['Height'].apply(lambda x: float(x * 100)) #将Height的单位换算成cm
one['ID']=one['ID'].apply(lambda x:str(x))  #将id属性变为字符串类型
two=pd.read_excel('学生数据2.xlsx')
two['C10']=two['C10'].fillna(0)
ID=two['ID'].tolist()
for i in range(len(ID)):  #转换ID为正确形式
        ID[i] = 202000 + ID[i]
two['ID'] = ID
two['ID'] = two['ID'].apply(lambda x: str(x))  #将ID转换为str
three=pd.merge(one,two,how='outer').drop_duplicates(subset=['ID']).sort_values('ID') #删除重复ID的
three['Constitution']=three['Constitution'].fillna('bad')  #填充体育成绩
#填充C1-C10所有空值的数据
for i in range(1,11):
    a = "C"+ str(i)
    three[a].fillna(three[a].mean(),inplace=True)
pe_grade = three['Constitution'].tolist()
for i in range(len(pe_grade)):  #将标准改成百分制
    if pe_grade[i] == 'excellent':
        pe_grade[i] = 95
    elif pe_grade[i] == 'good':
        pe_grade[i] = 85
    elif pe_grade[i] == 'general':
        pe_grade[i]=75
    elif pe_grade[i] == 'bad':
        pe_grade[i] = 55
three['Constitution']= pe_grade
three.to_csv('合并数据.csv')  #合并数据在csv文件中


#第一问
beijing = three[three['City']=='Beijing']
for i in range(1,11):
    a = "C"+ str(i)
    mean = sum(beijing[a])/len(beijing[a])
    print('北京学生%s课程平均成绩 % .3f'% (a,mean))

#第二问
stu_num = three[(three['City']=='Guangzhou')&(three['C1']>=80)&(three['Gender']=='boy')&(three['C10']>=9)].shape[0]
print('学生中家乡在广州，课程1在八十分以上，课程10在9分以上的男同学的数量为%d'%int(stu_num))

#第三问
Gz=three[(three['City']=='Guangzhou')&(three['Gender']=='girl')]
Sh=three[(three['City']=='Shanghai')&(three['Gender']=='girl')]
Gz_grade=Gz['Constitution'].tolist()
Sh_grade=Sh['Constitution'].tolist()
GZ_mean = sum(Gz_grade)/len(Gz_grade)
Sh_mean = sum(Sh_grade)/len(Sh_grade)
if GZ_mean>Sh_mean:
    print('广州女生平均体能测试成绩比上海女生好\r\n平均体能测试成绩分别为%.3f、%.3f\r\n'% (GZ_mean,Sh_mean))
elif GZ_mean==Sh_mean:
    print('广州女生平均体能成绩与上海女生实力相当\r\n平均体能测试成绩分别为%.3f、%.3f\r\n'% (GZ_mean,Sh_mean))
else:
    print('广州女生平均体能成绩比上海女生差\r\n平均体能测试成绩分别为%.3f、%.3f\r\n'% (GZ_mean,Sh_mean))

#第四问
for i in range(6,11):
    a = "C" + str(i)
    three[a] = three[a].apply(lambda x:x*10)
knowledge_mean = 0

pe_grade = three['Constitution'].tolist()
pe_mean = sum(pe_grade) / len(pe_grade)
each_pe_mean=three['Constitution'].apply(lambda x:x-pe_mean)
print(each_pe_mean)
std_pr = pow(pow(each_pe_mean, 2).sum() / 105, 0.5)  # 体育成绩的方差
print(std_pr)
each_pe_mean = three['Constitution'].apply(lambda x:(x-pe_mean)/std_pr)
print(each_pe_mean)


for i in range(1,11):
    a = "C" + str(i)
    knowledge_grade = three[a].tolist()
    knowledge_mean = sum(knowledge_grade) / len(knowledge_grade)
    each_aca_mean=three[a].apply(lambda x:x-knowledge_mean)
    std_aca = pow(pow(each_aca_mean, 2).sum() / 105, 0.5)
    each_aca_mean=three[a].apply(lambda x:(x-knowledge_mean)/std_aca)
    correlation=(each_aca_mean*each_pe_mean).sum()
    print("课程%d和体能测试成绩的相关系数：%s" % (i,correlation))
    if correlation<0.3:
        print("得出结论：课程%d与体能成绩不相关"% i)
    elif correlation>=0.3 and correlation<=0.8:
        print("得出结论：课程%d与体能成绩弱相关"% i)
    else:
        print("得出结论：课程%d与体能成绩相关"% i)
