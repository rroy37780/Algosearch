"""
This code accepts the query string entered by user as input, preprocesses it and returns top 20 documents based on decreasing order of cosine similarity (which is also calculated in this code)
"""
import numpy as np
from tfidf_generator import preprocess #user defined module and function
import time
import sys
import json
import os
"""
This function calculates cosine similarity score of query string with all document vectors
"""
# def similarity_score(query):
def generate_query_vector(preprocessed_query,keyword_indices):
    doc_vector=[0 for _ in  range(len(keyword_indices))]
    for word in preprocessed_query:
        if(word in keyword_indices.keys()):
            index=keyword_indices[word]
            doc_vector[index]+=1
    return doc_vector

def generate_tfidf_vector(query_vector,idf_list):
    freq_sum=sum(query_vector)
    query_tf_vector=[]
    query_tfidf_vector=[]

    for v in query_vector:
        query_tf_vector.append(v/freq_sum)
    for i in range(len(keywords)):
        query_tfidf_vector.append(round(query_tf_vector[i]*idf_list[i],5))

    return query_tfidf_vector

def calculate_cosine_similarity(tfidf_matrix,query_tfidf_vector):
    doc_score=[]
    for idx,doc_vector in enumerate(tfidf_matrix):
        cosine_similarity=np.dot(np.array(doc_vector),np.array(query_tfidf_vector))/(np.linalg.norm(np.array(doc_vector))*np.linalg.norm(np.array(query_tfidf_vector)))
        doc_score.append([idx+1,cosine_similarity])

    ordered_doc_score=sorted(doc_score,key=lambda x:-x[1])

    return ordered_doc_score

if __name__=="__main__":
    start_time=time.time()
    # query=" Maximum Area of Longest Diagonal Rectangle. "
    query=sys.argv[1] #get the query from command line (for integration with node backend)

    preprocessed_query=preprocess(query)

    # print(os.getcwd())

    keywords=[]
    idf_list=[]
    tfidf_matrix=[]

    titles=[]
    links=[]

    with open(f'{os.getcwd()}/tf-idf/keywords.txt','r') as f:
        for line in f:
            keywords.append(line.strip())

    with open(f'{os.getcwd()}/tf-idf/idf.txt','r') as f:
        for idf in f:
            idf_list.append(float(idf.strip()))

    with open(f'{os.getcwd()}/tf-idf/tfidf_matrix.txt','r') as f:
        for line in f:
            tfidf_matrix.append(list(map(float,line.split(','))))

    with open(f'{os.getcwd()}/scraper/valid_data/titles.txt') as f:
        for title in f:
            titles.append(title.strip())

    with open(f'{os.getcwd()}/scraper/valid_data/links.txt') as f:
        for link in f:
            links.append(link.strip())

    keyword_indices={keyword:idx for idx,keyword in enumerate(keywords)}
    query_vector=generate_query_vector(preprocessed_query,keyword_indices)
    query_tfidf_vector=generate_tfidf_vector(query_vector,idf_list)

    top_5_docs=calculate_cosine_similarity(tfidf_matrix,query_tfidf_vector)[:5]
    
    results=[]
    for item in top_5_docs:
        idx=item[0]
        score=item[1]
        title=titles[idx-1]
        link=links[idx-1]
        body=""
        with open(f'{os.getcwd()}/scraper/valid_data/problem_{idx}/problem_{idx}.txt') as f:
            fileContent=f.read()
            body+=fileContent
        results.append({'title':title,'link':link,'body':fileContent,'link':link})

    end_time=time.time()

    # print("Time Taken:",end_time-start_time)

    print(json.dumps(results))
