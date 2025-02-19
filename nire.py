import sys
import codecs
import re
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pyspark.sql import SparkSession
import nltk

# Initialize NLTK data (add this once)
nltk.download('stopwords')

# Fix Windows console encoding
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Initialize Spark context
spark = SparkSession.builder \
    .appName("Nire") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.python.worker.memory", "512m") \
    .getOrCreate()

sc = spark.sparkContext

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def tokenize(text):
    try:
        # Preserve unicode characters in regex
        text = re.sub(r'[^\w\s]', '', text.lower(), flags=re.UNICODE)
        tokens = text.split()
        return [ps.stem(word) for word in tokens if word not in stop_words]
    except Exception as e:
        print(f"Error tokenizing: {str(e)}")
        return []

def create_invert_index(doc_rdd):
    return (
        doc_rdd
        # Create sets from the start for efficient union
        .flatMap(lambda x: [(word, {x[0]}) for word in tokenize(x[1])])
        .reduceByKey(lambda a, b: a.union(b))
        .mapValues(lambda ids: list(ids))  # Convert set to list for serialization
    )

# Use raw string for Windows paths
docs_rdd = sc.wholeTextFiles(r"C:\Users\valor\Desktop\nire\corpus\*.txt") \
    .map(lambda x: (x[0].split('/')[-1], x[1]))

try:
    output_path = r"file:///C:/Users/valor/Desktop/nire/output"
    
    # Remove existing output directory
    if 'output' in os.listdir('C:/Users/valor/Desktop/nire'):
        import shutil
        shutil.rmtree('C:/Users/valor/Desktop/nire/output')
    
    inverted_index_rdd = create_invert_index(docs_rdd)
    inverted_index_rdd.saveAsTextFile(output_path)
    
    # Optional: Print sample results
    sample = inverted_index_rdd.take(10)
    print("\nSample entries:")
    for word, docs in sample:
        print(f"{word}: {docs}")
        
except Exception as e:
    print(f"Critical error: {str(e)}")
    import traceback
    traceback.print_exc()
    spark.stop()
    sys.exit(1)

spark.stop()