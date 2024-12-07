import os
import nltk

# Define the path to store NLTK data
nltk_data_path = '/app/nltk_data'

# Download necessary NLTK data if not already present
if not os.path.exists(os.path.join(nltk_data_path, 'tokenizers/punkt')):
    nltk.download('punkt', download_dir=nltk_data_path)
if not os.path.exists(os.path.join(nltk_data_path, 'corpora/stopwords')):
    nltk.download('stopwords', download_dir=nltk_data_path)
if not os.path.exists(os.path.join(nltk_data_path, 'corpora/wordnet')):
    nltk.download('wordnet', download_dir=nltk_data_path)
if not os.path.exists(os.path.join(nltk_data_path, 'corpora/omw-1.4')):
    nltk.download('omw-1.4', download_dir=nltk_data_path)
if not os.path.exists(os.path.join(nltk_data_path, 'tokenizers/punkt_tab')):
    nltk.download('punkt_tab', download_dir=nltk_data_path) 

print("NLTK data downloaded successfully.")
