"""
This code accepts the query string entered by user as input, preprocesses it and returns top 20 documents based on decreasing order of cosine similarity (which is also calculated in this code)
"""
import numpy as np
from tfidf_generator import preprocess #user defined module and function
import time
import sys
import json
import os

import zlib
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

def zlib_matrix_loader(file_path):
    # Read and decompress the zlib file
    with open(file_path, 'rb') as f:
        compressed_data = f.read()
        decompressed_data = zlib.decompress(compressed_data)

    # Decode the decompressed data into a string
    decompressed_text = decompressed_data.decode('utf-8')

    # Process each line, stripping trailing commas and converting to float
    matrix = []
    for line in decompressed_text.splitlines():
        # Clean the line by removing any trailing commas
        clean_line = line.rstrip(',').strip()
        # Convert the cleaned line to a list of floats
        matrix.append(list(map(float, clean_line.split(','))))

    return matrix


if __name__=="__main__":
    start_time=time.time()
    # query=" Maximum Area of Longest Diagonal Rectangle. "
    query=sys.argv[1] #get the query from command line (for integration with node backend)

    # for debugging commenting from here ...
    preprocessed_query=preprocess(query)

    # print(os.getcwd())

    keywords=[]
    idf_list=[]
    # tfidf_matrix=[]

    titles=[]
    links=[]

    with open(f'{os.getcwd()}/tf-idf/keywords.txt','r') as f:
        for line in f:
            keywords.append(line.strip())

    with open(f'{os.getcwd()}/tf-idf/idf.txt','r') as f:
        for idf in f:
            idf_list.append(float(idf.strip()))

    # with open(f'{os.getcwd()}/tf-idf/tfidf_matrix.txt','r') as f:
    #     for line in f:
    #         tfidf_matrix.append(list(map(float,line.split(','))))

    tfidf_matrix=zlib_matrix_loader(f'{os.getcwd()}/tf-idf/tfidf_compressed.zlib') #this is the line causing deployment failure on heroku due to large memory usage

    with open(f'{os.getcwd()}/scraper/valid_data/titles.txt') as f:
        for title in f:
            titles.append(title.strip())

    with open(f'{os.getcwd()}/scraper/valid_data/links.txt') as f:
        for link in f:
            links.append(link.strip())

    keyword_indices={keyword:idx for idx,keyword in enumerate(keywords)}
    query_vector=generate_query_vector(preprocessed_query,keyword_indices)
    query_tfidf_vector=generate_tfidf_vector(query_vector,idf_list)

    # top_5_docs=calculate_cosine_similarity(tfidf_matrix,query_tfidf_vector)[:5]
    
    # results=[]
    # for item in top_5_docs:
    #     idx=item[0]
    #     score=item[1]
    #     title=titles[idx-1]
    #     link=links[idx-1]
    #     body=""
    #     with open(f'{os.getcwd()}/scraper/valid_data/problem_{idx}/problem_{idx}.txt') as f:
    #         fileContent=f.read()
    #         body+=fileContent
    #     results.append({'title':title,'link':link,'body':fileContent,'link':link})

    # end_time=time.time()

    #to here 
    temp_res=[{"title": "Sum of Two Integers", "link": "https://leetcode.com/problems/sum-of-two-integers", "body": "Given two integers a and b, return the sum of the two integers without using the operators + and -.\nExample 1:\nInput: a = 1, b = 2\nOutput: 3\nExample 2:\nInput: a = 2, b = 3\nOutput: 5\nConstraints:\n-1000 <= a, b <= 1000\nTopics\nMath\nBit Manipulation\n"}, {"title": "Add Two Integers", "link": "https://leetcode.com/problems/add-two-integers", "body": "Given two integers num1 and num2, return the sum of the two integers.\nExample 1:\nInput: num1 = 12, num2 = 5\nOutput: 17\nExplanation: num1 is 12, num2 is 5, and their sum is 12 + 5 = 17, so 17 is returned.\nExample 2:\nInput: num1 = -10, num2 = 4\nOutput: -6\nExplanation: num1 + num2 = -6, so -6 is returned.\nConstraints:\n-100 <= num1, num2 <= 100\nTopics\nMath\n"}, {"title": "Binary Gap", "link": "https://leetcode.com/problems/binary-gap", "body": "Given a positive integer n, find and return the longest distance between any two adjacent 1's in the binary representation of n. If there are no two adjacent 1's, return 0.\nTwo 1's are adjacent if there are only 0's separating them (possibly no 0's). The distance between two 1's is the absolute difference between their bit positions. For example, the two 1's in \"1001\" have a distance of 3.\nExample 1:\nInput: n = 22\nOutput: 2\nExplanation: 22 in binary is \"10110\".\nThe first adjacent pair of 1's is \"10110\" with a distance of 2.\nThe second adjacent pair of 1's is \"10110\" with a distance of 1.\nThe answer is the largest of these two distances, which is 2.\nNote that \"10110\" is not a valid pair since there is a 1 separating the two 1's underlined.\nExample 2:\nInput: n = 8\nOutput: 0\nExplanation: 8 in binary is \"1000\".\nThere are not any adjacent pairs of 1's in the binary representation of 8, so we return 0.\nExample 3:\nInput: n = 5\nOutput: 2\nExplanation: 5 in binary is \"101\".\nConstraints:\n1 <= n <= 109\nTopics\nBit Manipulation\n"}, {"title": "Add Two Numbers", "link": "https://leetcode.com/problems/add-two-numbers", "body": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum\u00a0as a linked list.\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.\nExample 1:\nInput: l1 = [2,4,3], l2 = [5,6,4]\nOutput: [7,0,8]\nExplanation: 342 + 465 = 807.\nExample 2:\nInput: l1 = [0], l2 = [0]\nOutput: [0]\nExample 3:\nInput: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]\nOutput: [8,9,9,9,0,0,0,1]\nConstraints:\nThe number of nodes in each linked list is in the range [1, 100].\n0 <= Node.val <= 9\nIt is guaranteed that the list represents a number that does not have leading zeros.\nTopics\nLinked List\nMath\nRecursion\n"}, {"title": "Add Two Numbers II", "link": "https://leetcode.com/problems/add-two-numbers-ii", "body": "You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.\nExample 1:\nInput: l1 = [7,2,4,3], l2 = [5,6,4]\nOutput: [7,8,0,7]\nExample 2:\nInput: l1 = [2,4,3], l2 = [5,6,4]\nOutput: [8,0,7]\nExample 3:\nInput: l1 = [0], l2 = [0]\nOutput: [0]\nConstraints:\nThe number of nodes in each linked list is in the range [1, 100].\n0 <= Node.val <= 9\nIt is guaranteed that the list represents a number that does not have leading zeros.\nFollow up:\u00a0Could you solve it without reversing the input lists?\nTopics\nLinked List\nMath\nStack\n"}]

    # print("Time Taken:",end_time-start_time)

    # print(json.dumps(results))
    print(json.dumps(temp_res))