import time
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.91/linux64/chromedriver-linux64.zip- to download appropriate chromedriver version

driver = webdriver.Chrome(executable_path='/home/rishabh/algozenith_2024/chromedriver-linux64/chromedriver')
# driver.get("https://google.com")

# The base URL for the pages to scrape
page_URL = "https://leetcode.com/problemset/all/?page="

# cur_url=page_URL

problem_links=[]
problem_titles=[]
for i in range(1,61):
    cur_url=page_URL+str(i)
    driver.get(cur_url)
    time.sleep(5)
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    all_a_tags=soup.findAll('a')
    problem_a_tags=[]
    
    for a_tag in all_a_tags:
        if(((a_tag.get('href')) and (a_tag['href'].startswith('/problems/')))and(a_tag.get('class')and (a_tag['class'][0]!='hover:text-label-3')and (a_tag['class'][0]!='flex'))and (not(a_tag['href'].endswith('/solution')))and (not 'envType' in a_tag['href'])):
            #last condition of if is to exclude the first daily question and rest are tp exclude other a tags
            problem_a_tags.append(a_tag)
            problem_links.append("https://leetcode.com"+a_tag['href'])

            #to remove the number of the question at the beginning
            whitespace_index=a_tag.text.find(' ')# find the first occurence of whitespace in the string
            title=a_tag.text[whitespace_index:]
            problem_titles.append(title)

print(len(problem_links))
print(len(problem_titles))
# saving the problem links and titles
with open('./data/problem_titles.txt',"a") as f:
    for title in problem_titles:
        f.write(title+'\n')

with open('./data/problem_links.txt',"a") as f:
    for link in problem_links:
        f.write(link+'\n')

driver.quit()