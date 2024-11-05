import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader

# 1. 读取数据
abstracts_df = pd.read_csv("D:/Workspace/work_code/Python_code/NLP_project/Final_Work/use_codes/abstracts2.tsv", sep="\t")
sentences_df = pd.read_csv("D:/Workspace/work_code/Python_code/NLP_project/Final_Work/use_codes/前列腺癌基因性状相关文本.tsv", sep="\t")

# 2. 数据预处理，确保无 NaN 值
abstracts = abstracts_df["Abstract"].fillna('').tolist()  # 将 NaN 替换为空字符串
sentences = sentences_df["Sentence"].fillna('').tolist()

# 假设每个 Abstract 与 Sentence 配对
data = list(zip(abstracts, sentences))

# 3. 定义数据集类
class TextDataset(Dataset):
    def __init__(self, data, tokenizer, max_len):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # 确保数据无 NaN，且格式为字符串
        abstract, sentence = self.data[idx]
        abstract = str(abstract) if pd.notna(abstract) else ""
        sentence = str(sentence) if pd.notna(sentence) else ""

        # 进行编码
        encoding = self.tokenizer.encode_plus(
            abstract,
            sentence,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True,
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'token_type_ids': encoding['token_type_ids'].flatten(),
            # 如果有标签，可以在此处添加
            # 'labels': torch.tensor(label, dtype=torch.long)
        }

# 4. 初始化模型和 tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)  # 假设有两个类别

# 5. 拆分数据集
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
train_dataset = TextDataset(train_data, tokenizer, max_len=128)
test_dataset = TextDataset(test_data, tokenizer, max_len=128)

# 6. 创建数据加载器
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16)

# 7. 训练模型
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
model.train()

for epoch in range(3):  # 简单训练3个epoch
    for batch in train_loader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(model.device)
       
