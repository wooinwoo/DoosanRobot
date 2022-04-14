num=22
range=[-1,-2,-3,-4,-5,-6,-7,-8]
num=bin(num)#2진수로 변환
c=0
for i in reversed(num):
    if i=="b": break
    if i=="1": range[c]*=-1
    c+=1
