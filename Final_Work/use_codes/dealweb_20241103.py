# 前期关键词筛选（失败路线）
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import stanza
import numpy as np

# 读取数据
file1 = 'D:\\Workspace\\work_code\\Python_code\\NLP_project\\Final_Work\\use_data\\abstracts2.tsv'
file2 = 'D:\\Workspace\\work_code\\Python_code\\NLP_project\\Final_Work\\use_data\\前列腺癌基因性状相关文本.tsv'

data1 = pd.read_csv(file1, sep='\t')
data2 = pd.read_csv(file2, sep='\t')

# 初始化Stanza
stanza.download('en')  # 只需运行一次
nlp = stanza.Pipeline('en')

# 用于存储主谓宾，按文件来源分类
subjects = {'file1': [], 'file2': []}
predicates = {'file1': [], 'file2': []}
objects = {'file1': [], 'file2': []}

# 提取主谓宾
for sentence in data1['Abstract'].dropna().tolist():
    doc = nlp(sentence)
    for sent in doc.sentences:
        subject = []
        predicate = []
        obj = []
        for word in sent.words:
            if word.deprel == 'nsubj':
                subject.append(word.text)
            elif word.deprel == 'root':
                predicate.append(word.text)
            elif word.deprel == 'dobj':
                obj.append(word.text)
        if subject and predicate:
            subjects['file1'].append(' '.join(subject))
            predicates['file1'].append(' '.join(predicate))
            objects['file1'].append(' '.join(obj) if obj else "无")

for sentence in data2['Abstract'].dropna().tolist():
    doc = nlp(sentence)
    for sent in doc.sentences:
        subject = []
        predicate = []
        obj = []
        for word in sent.words:
            if word.deprel == 'nsubj':
                subject.append(word.text)
            elif word.deprel == 'root':
                predicate.append(word.text)
            elif word.deprel == 'dobj':
                obj.append(word.text)
        if subject and predicate:
            subjects['file2'].append(' '.join(subject))
            predicates['file2'].append(' '.join(predicate))
            objects['file2'].append(' '.join(obj) if obj else "无")

# 自定义计算TF-IDF
def custom_tfidf(entities, alpha=0.5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(entities)
    
    # 获取TF和IDF
    tfidf_array = tfidf_matrix.toarray()
    idf = vectorizer.idf_
    
    # 调整TF-IDF，增强IDF权重
    adjusted_tfidf = (1 - alpha) * tfidf_array + alpha * (tfidf_array * idf.reshape(1, -1))
    
    return pd.DataFrame(adjusted_tfidf, columns=vectorizer.get_feature_names_out())

# 使用自定义的函数替代原有的计算TF-IDF部分
subjects_tfidf = {key: custom_tfidf(value) for key, value in subjects.items()}
predicates_tfidf = {key: custom_tfidf(value) for key, value in predicates.items()}
objects_tfidf = {key: custom_tfidf(value) for key, value in objects.items()}

# 保存结果到文件
for key in subjects_tfidf.keys():
    subjects_tfidf[key].to_csv(f'subjects_tfidf_{key}.csv', index=False)
    predicates_tfidf[key].to_csv(f'predicates_tfidf_{key}.csv', index=False)
    objects_tfidf[key].to_csv(f'objects_tfidf_{key}.csv', index=False)

# 输出TF-IDF值最高的前十个词汇
def print_top_tfidf(tfidf_df, category):
    if not tfidf_df.empty:
        tfidf_sums = tfidf_df.sum(axis=0)
        top_tfidf = tfidf_sums.nlargest(10)
        print(f"Top 10 TF-IDF values for {category}:")
        print(top_tfidf)
    else:
        print(f"No data for {category}.")

# 输出每个文件的TF-IDF最高词汇
for key in subjects_tfidf.keys():
    print_top_tfidf(subjects_tfidf[key], f'Subjects from {key}')
    print_top_tfidf(predicates_tfidf[key], f'Predicates from {key}')
    print_top_tfidf(objects_tfidf[key], f'Objects from {key}')

