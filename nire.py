from pyspark import SparkContext
import re
import os

# Initialize Spark Context
sc = SparkContext("local", "Nire")

def tokenize(text):
    """Convert text to lowercase, remove punctuation, and split into unique words"""
    text = re.sub(r'\W+', ' ', text.lower())
    words = text.split()
    return list(set(words))  # Return unique words

# 1. Load and prepare documents
def load_documents(path):
    """Load documents with (filename, content) pairs"""
    return sc.wholeTextFiles(path) \
             .map(lambda x: (os.path.basename(x[0]), x[1]))

# 2. Create inverted index
def create_inverted_index(docs_rdd):
    """Build inverted index: (word -> list of documents)"""
    return docs_rdd.flatMap(lambda x: [(word, x[0]) for word in tokenize(x[1])]) \
                   .groupByKey() \
                   .map(lambda x: (x[0], list(x[1]))) \
                   .collectAsMap()

# 3. Search function
def search(query, inverted_index):
    """Return documents containing all query words"""
    query_words = tokenize(query)
    if not query_words:
        return []
    
    # Get document lists for each query word
    doc_sets = [set(inverted_index.get(word, [])) for word in query_words]
    
    # Find common documents across all query words
    return list(set.intersection(*doc_sets)) if doc_sets else []

# Main execution
if __name__ == "__main__":
    # Load documents (update path to your files)
    docs_rdd = load_documents("corpus/*.txt")
    
    # Build inverted index
    inverted_index = create_inverted_index(docs_rdd)
    
    # Example queries
    print("Documents containing 'hello world':", search("hello world", inverted_index))
    print("Documents containing 'speaking':", search("spark", inverted_index))
    
    # Keep context alive for exploration (optional)
    # input("Press Enter to stop...")
    sc.stop()