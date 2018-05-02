import pandas as pd
import itertools
import numpy as np

#function to get rank
def genRank(A):
    R = [0 for x in range(len(A))]
    for i in range(len(A)):
        (r, s) = (1, 1)
        for j in range(len(A)):
            if j != i and A[j] < A[i]:
                r += 1
            if j != i and A[j] == A[i]:
                s += 1
        R[i] = r + (s - 1) / 2
    return R

#Get Sign
def genSign(a):
    x=[]
    for each in a:
        if(each>0):
            x.append(1)
        else:
            x.append(-1)
    return x

#Function to implement Solution for Question_1
def generateWSRT(dframe,dfkey):
    for column in dframe:
        diff=dframe[column]-dfkey
        diff=diff[diff!=0]
        absdiff=abs(diff).tolist()
        diff_rank=genRank(absdiff)
        t=genSign(diff.tolist())
        signed_rank=[a*b for a,b in zip(diff_rank,t)]
        l1=[i for i in signed_rank if i > 0.0]
        l2=[i for i in signed_rank if i < 0.0]
        rank_pos=sum(l1)
        rank_neg=abs(sum(l2))
        if(rank_pos<rank_neg):
            print (str(column), "Test statistic: "+str(rank_pos),"Positive")
        else:
            print (str(column), "Test statistic: "+str(rank_pos), "Negative")

#Get Combinations
def get_combinations(a):
    l=[]
    for i in range(2,len(a)+1):
        l.append(list(itertools.combinations(a, i)))
    return l

#Generate the new Dataframe for the combination and permutation of the column
def generate_newdf(comb,orgdf):
    newDf=pd.DataFrame()
    for i in range(len(comb)):
        #print(comb[i])
        for j in range(len(comb[i])):
            t=i+2
            colName="W"
            sumc = pd.DataFrame(0, index=np.arange(len(orgdf)), columns={"A"})
            for k in range(t):
                colName=colName+"_"+comb[i][j][k]
                sumc['A']+=orgdf[comb[i][j][k]]
            sumc['A']=sumc['A']/t
            newDf[colName]=sumc
    return newDf


#Load the Data from the excel file.
xl = pd.ExcelFile("E:\coding_challneges\Algomus\Python_Exam.xlsx")
df = xl.parse("Data")
#formatting for dropping the
if 'Customer' in df.columns:
    df=df.drop('Customer', axis=1)

# Key Column
key=df[df.columns[0]]
df=df.drop(df.columns[0],axis=1)

# Execution for solution 1
print("Solution for Question 1")
generateWSRT(df,key)
colList=df.columns

# Question 2 Solution / Execution
print("Solution for Question 2")
comb=get_combinations(colList)
fed=generate_newdf(comb,df)
generateWSRT(fed,key)

