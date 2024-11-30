import time
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import random

driver=webdriver.Chrome(executable_path='/home/rishabh/algozenith_2024/chromedriver-linux64/chromedriver')

"""
Create a folder named valid_data
Go through all the links in /data/problem_titles.txt, save their content in valid_data ,in folder named problem_i, with the file name problem_i.txt.
Save the difficulty in a separate file named difficulty.txt
Save the titles (can use problem_titles.txt file) and links in ordered way.
In case of any error, do not update the index. Verify all once done
"""
desc_class='elfjS'
difficulty_class='bg-fill-secondary'
topics_class='mt-2'

def make_list(filename):
    ls=[]
    with open(filename,'r') as f:
        for line in f:
            ls.append(line)
    return ls

def get_difficulty(soup):
    difficulty=soup.find('div',class_=difficulty_class)
    return difficulty.text
    # return difficulty.stripped_string

def get_topics_list(soup):
    parent_tag=soup.find('div',class_=topics_class)
    topics=[]
    for child in parent_tag.children:
        if child.name:
            topics.append(child.text)
            # topics.append(child.stripped_string)
    return topics


def make_dir_of_problem(index):
    path=os.getcwd()+'/valid_data/'+'problem_'+str(index)
    os.mkdir(path)
    return path


def explore_problems(all_problem_links,all_titles):
    all_link_cnt=0
    index=1
    folder_path=os.getcwd()+'/valid_data'
    difficulty_arr=[]
    title_arr=[]
    # classes_to_wait_for=[desc_class,difficulty_class,topics_class]
    # css_selector = ",".join(f".{cls}" for cls in classes_to_wait_for)
    # print(css_selector)
    os.mkdir(folder_path)
    for link in all_problem_links:
        try:
            driver.get(link)
            time.sleep(random.uniform(3, 6))  # Wait for 3 to 6 seconds randomly
            # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, f".{desc_class}")))
            html=driver.page_source
            soup=BeautifulSoup(html,'html.parser')
            desc_html=soup.find('div',class_=desc_class)
            # Split the text into lines, remove blank lines, and reassemble the text
            description = "\n".join(line for line in desc_html.text.splitlines() if line.strip())
            # description=desc_html.text
            # description=desc_html.stripped_strings
            title=all_titles[all_link_cnt]
            difficulty=get_difficulty(soup)
            topics_list=get_topics_list(soup)
            description+='\n'
            description+='Topics\n'
            for topic in topics_list:
                description+=topic
                description+='\n'
            folder=make_dir_of_problem(index)
            filepath=folder+'/problem_'+str(index)+'.txt'
            with open(filepath,"a",encoding="utf-8",errors="ignore") as f:
                f.write(description)
            difficulty_arr.append(difficulty)
            title_arr.append(title)
            index+=1
        except Exception as e:
            print(e)
            pass
        all_link_cnt+=1
    driver.quit()
    with open(folder_path+'/difficulty.txt',"a",encoding="utf-8",errors="ignore") as f:
        for item in difficulty_arr:
            f.write(item+'\n')
    with open(folder_path+'/titles.txt',"a",encoding="utf-8",errors="ignore") as f:
        for item in title_arr:
            f.write(item)

if __name__=="__main__":
    links_path=os.getcwd()+'/data/'+'problem_links.txt'
    titles_path=os.getcwd()+'/data/'+'problem_titles.txt'
    all_problem_links=make_list(links_path)
    all_titles=make_list(titles_path)
    explore_problems(all_problem_links,all_titles)

