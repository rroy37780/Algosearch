import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,WordNetLemmatizer
from word2number import w2n
import math
from scipy.sparse import csr_matrix, save_npz, load_npz
import numpy as np
# nltk.data.path.append('./nltk_data')

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt_tab')

def preprocess(text):
    text=re.sub(r'[^\w\s]','',text) #patten, replacement, string
    words=word_tokenize(text.lower())

    stop_words=set(stopwords.words('english'))
    filtered_words=[word for word in words if word not in stop_words]

    stemmer=PorterStemmer()
    lemmatizer=WordNetLemmatizer()

    stemmed_words=[stemmer.stem(word) for word in filtered_words]
    lemmatized_words=[lemmatizer.lemmatize(word) for word in stemmed_words]

    normalized_words=[]
    for word in lemmatized_words:
        try:
            normalized_words.append(str(w2n.word_to_num(word)))
            normalized_words.append(word)
        except ValueError:
            normalized_words.append(word)

    # Remove numeric words and long words
    filtered_words = [
        word for word in normalized_words
        if not word.isdigit() and len(word) <= 15
    ]

    sorted_words=sorted(filtered_words)
    return sorted_words

def generate_keywords_and_document_matrix(path):
    all_keywords=[]
    document_matrix=[]
    all_titles=[]
    with open(path+'/titles.txt','r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            all_titles.append(line[1:])
    for i in range(1,N+1):
        with open(f'{path}/problem_{i}/problem_{i}.txt','r',encoding='utf-8',errors='ignore') as f:
            filecontent=f.read()
            #include title
            title=all_titles[i-1]
            filecontent=title+filecontent
            #remove example content till topic
            example_index=filecontent.find("Example 1:")
            topic_index=filecontent.rfind("Topics")
            filecontent=filecontent[:example_index]+filecontent[topic_index:]
            preprocessed_file_content=preprocess(filecontent)
            document_matrix.append(preprocessed_file_content)
            all_keywords.extend(preprocessed_file_content)

    keywords=set(all_keywords)
    keywords=sorted(keywords)

    with open('./keywords.txt','w',encoding='utf-8',errors='ignore') as f:
        for word in keywords:
            f.write(word+'\n')
    return keywords,document_matrix

def generate_doc_freq_matrix(document_matrix,keyword_indixes):
    doc_freq_matrix=[[0 for _ in range(len(keywords))] for _ in range(N)]
    doc_num=0
    for document in document_matrix:
        for word in document:
            try:
                index=keyword_indices[word]
                doc_freq_matrix[doc_num][index]+=1
            except:
                pass
        doc_num+=1
    return doc_freq_matrix

def generate_idf_vector(doc_freq_matrix,keywords):
    idf_list=[]
    for keyword in keywords:
        index=keyword_indices[keyword]
        cnt=0
        for row in doc_freq_matrix:
            if(row[index]>0):
                cnt+=1
        idf=round(math.log10(N/cnt),4)
        idf_list.append(idf)
    with open('idf.txt','w',encoding='utf-8',errors='ignore') as f:
        for idf in idf_list:
            f.write(str(idf)+'\n')
    return idf_list

def generate_tf_matrix(doc_freq_matrix):
    tf_matrix=[[0 for _ in range(len(doc_freq_matrix[0])) ] for _ in range(N)]
    doc_num=0
    for doc in doc_freq_matrix:
        freq_sum=sum(doc)
        for col in range(len(doc)):
            tf_matrix[doc_num][col]=doc_freq_matrix[doc_num][col]/freq_sum
        doc_num+=1
    return tf_matrix

# Precompute and save the TF-IDF matrix
def generate_and_save_tfidf_matrix(tf_matrix, idf_list, output_file='tfidf_matrix.npz'):
    """
    Generate the TF-IDF matrix and save it as a sparse matrix.
    """
    tf_matrix = np.array(tf_matrix, dtype=np.float64)
    idf_array = np.array(idf_list, dtype=np.float64)
    tfidf_matrix = tf_matrix * idf_array  # Element-wise multiplication
    sparse_tfidf = csr_matrix(tfidf_matrix)
    save_npz(output_file, sparse_tfidf)
    return sparse_tfidf

if __name__=="__main__":

    path='/home/rishabh/algozenith_2024/dsa_search_engine/search_engine/scraper/valid_data'
    N=2368 # total number of documents

    keywords,document_matrix=generate_keywords_and_document_matrix(path)
    print("Keywords and document matrix generated")

    keyword_indices = {keyword: idx for idx, keyword in enumerate(keywords)}

    doc_freq_matrix=generate_doc_freq_matrix(document_matrix,keyword_indices)
    print("doc_freq_matrix generated")

    idf_list=generate_idf_vector(doc_freq_matrix,keywords)
    print("idf vector generated")

    tf_matrix=generate_tf_matrix(doc_freq_matrix)
    print("tf_matrix generated")

    tfidf_matrix=generate_and_save_tfidf_matrix(tf_matrix,idf_list)
    print("tfidf_matrix generated and saved")

