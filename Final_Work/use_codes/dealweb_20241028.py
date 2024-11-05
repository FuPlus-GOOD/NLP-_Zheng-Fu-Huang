import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: 读取摘要和相关文本
def load_texts(file_path, column_name):
    df = pd.read_csv(file_path, delimiter='\t', usecols=[column_name])
    return df[column_name].fillna('').tolist()  # 返回文本列表

# Step 2: 加载摘要和句子
abstracts = load_texts("D:/Workspace/work_code/Python_code/NLP_project/Final_Work/use_codes/abstracts2.tsv", "Abstract")
sentences = load_texts("D:/Workspace/work_code/Python_code/NLP_project/Final_Work/use_codes/前列腺癌基因性状相关文本.tsv", "Sentence")

# Step 3: 创建TF-IDF向量化器并计算TF-IDF值
corpus = abstracts + sentences  # 将摘要和句子组合成一个语料库
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)  # 停用词和特征数量可以根据需求调整
tfidf_matrix = vectorizer.fit_transform(corpus)

# Step 4: 提取每个文本的关键词
feature_names = vectorizer.get_feature_names_out()
abstract_keywords = tfidf_matrix[:len(abstracts)].mean(axis=0).A1  # 计算摘要中每个词的平均TF-IDF值
sentence_keywords = tfidf_matrix[len(abstracts):].mean(axis=0).A1  # 计算句子中每个词的平均TF-IDF值

# Step 5: 选取TF-IDF值较高的关键词
top_n = 10  # 可以调整需要的关键词数量
abstract_top_keywords = [(feature_names[i], abstract_keywords[i]) for i in abstract_keywords.argsort()[-top_n:][::-1]]
sentence_top_keywords = [(feature_names[i], sentence_keywords[i]) for i in sentence_keywords.argsort()[-top_n:][::-1]]

# 显示结果
print("摘要的关键词:")
for word, score in abstract_top_keywords:
    print(f"{word}: {score}")

print("\n句子的关键词:")
for word, score in sentence_top_keywords:
    print(f"{word}: {score}")

