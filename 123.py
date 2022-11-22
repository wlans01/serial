import os

dataPath =r'C:\Users\wlans\Documents\Bandicut'
resultpath =r'C:\Users\wlans\Desktop\gavideo'

# 데이터 파일 불러오기
file_list = [file for file in os.listdir(dataPath)]
totlal_file_len = len(file_list)

for i in range(totlal_file_len):
    a= f'{dataPath}\\{file_list[i]}'
    b= f'{resultpath}\\GA-{i+1}.png'
    os.rename(a,b)