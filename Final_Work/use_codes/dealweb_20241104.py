# 做词云图
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取 TXT 文件中的 ID
with open('D:/Workspace/work_code/Python_code/NLP_project/Final_Work/use_codes/gene_list.txt', 'r') as file:
    ids = file.read().splitlines()  # 按行读取，去掉换行符

# 读取 TSV 文件
tsv_data = pd.read_csv('D:/Workspace/work_code/Python_code/NLP_project/Final_Work/use_codes/前列腺癌基因性状相关文本.tsv', sep='\t')  # 读取 TSV 文件，指定分隔符为制表符

# 筛选出匹配的行
matched_rows = tsv_data[tsv_data['Gene'].isin(ids)]  # 假设 TSV 文件中有一列名为 'id'

# 提取 'sentence' 列
sentences = matched_rows['Sentence'].tolist()  # 将提取的句子转换为列表

# 将句子连接为一个字符串
text = ' '.join(sentences)

# 创建词云对象
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    max_words=200,
    colormap='viridis'
).generate(text)  # 生成词云

# 显示词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')  # 使用双线性插值显示图像
plt.axis('off')  # 关闭坐标轴
plt.show()  # 显示图形
