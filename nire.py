import sys
from pyspark import RDD
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pyspark.sql import SparkSession

# Initialize Spark context
spark = SparkSession.builder \
    .appName("Nire") \
    .getOrCreate()

sc = spark.sparkContext

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

if len(sys.argv) != 3:
    print("Usage: token.py <input filename> <output filename>")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

def tokenize(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    tokens = text.split()
    return [ps.stem(word) for word in tokens if word not in stop_words]

def create_invert_index(doc_rdd):
    return (
        doc_rdd
        .flatMap(lambda x: [(word, x[0]) for word in tokenize(x[1])]) \
        .groupByKey() \
        .mapValues(lambda ids: list(set(ids)))
    )

docs_rdd = sc.wholeTextFiles("corpus/*.txt") \
    .map(lambda x: (x[0].split('/')[-1], x[1]))

inverted_index = create_invert_index(docs_rdd).collect()
    
print("Inverted Index:")
for word, docs in inverted_index:
    print(f"{word}: {docs}")

# try:
#     with open(input_filename, "r", encoding='utf-8') as i, \
#         open(output_filename, "w", encoding='utf-8') as o:
#         for line in i:
#             tokens = tokenize(line)
#             o.write(' '.join(tokens) + '\n')
# except Exception as e:
#     print(e)
#     sys.exit(1)

spark.stop()