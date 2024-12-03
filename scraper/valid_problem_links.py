import os

all_titles=[]
all_links=[]

valid_titles=[]
valid_links=[]
path=os.getcwd()

with open(f'{path}/data/problem_titles.txt','r',encoding='utf-8',errors='ignore') as f:
    for title in f:
        all_titles.append(title.strip())
with open(f'{path}/data/problem_links.txt','r',encoding='utf-8',errors='ignore') as f:
    for link in f:
        all_links.append(link.strip())
with open(f'{path}/valid_data/titles.txt','r',encoding='utf-8',errors='ignore') as f:
    for title in f:
        valid_titles.append(title.strip())

#save corresponding link to valid_titles in valid_links
cnt=0
for idx,title in enumerate(all_titles):    
    if(title==valid_titles[cnt]):
        valid_links.append(all_links[idx])
        cnt+=1

with open(f'{path}/valid_data/links.txt','w',encoding='utf-8',errors='ignore') as f:
    for link in valid_links:
        f.write(link+'\n')

