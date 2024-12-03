"""
This code accepts the query string entered by user as input, preprocesses it and returns top 20 documents based on decreasing order of cosine similarity (which is also calculated in this code)
"""
import numpy as np
from tfidf_generator import preprocess #user defined module and function
import time
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
    query=" Maximum Area of Longest Diagonal Rectangle. "

    preprocessed_query=preprocess(query)

    keywords=[]
    idf_list=[]
    tfidf_matrix=[]
    with open('keywords.txt','r') as f:
        for line in f:
            keywords.append(line.strip())
    with open('idf.txt','r') as f:
        for idf in f:
            idf_list.append(float(idf.strip()))
    with open('tfidf_matrix.txt','r') as f:
        for line in f:
            tfidf_matrix.append(list(map(float,line.split(','))))

    keyword_indices={keyword:idx for idx,keyword in enumerate(keywords)}
    query_vector=generate_query_vector(preprocessed_query,keyword_indices)
    query_tfidf_vector=generate_tfidf_vector(query_vector,idf_list)

    top_5_docs=calculate_cosine_similarity(tfidf_matrix,query_tfidf_vector)[:5]

    end_time=time.time()

    print("Time Taken:",end_time-start_time)

    print(top_5_docs)
