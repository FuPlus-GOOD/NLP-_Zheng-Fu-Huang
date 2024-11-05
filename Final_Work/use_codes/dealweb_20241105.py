# 从HPO数据库筛选出与Entrez ID相关联的疾病信息

import requests
import os

# 读取文件中的Entrez IDs
file_path = "D:\\Workspace\\work_code\\Python_code\\NLP_project\\Final_Work\\use_codes\\list2.txt"
with open(file_path, 'r') as file:
    entrez_ids = file.read().splitlines()

# 基础URL模板
base_url = "https://ontology.jax.org/api/network/annotation/NCBIGene:{}/download/disease"

# 存储获取到的疾病信息
disease_info = {}

# 下载文件的保存路径
save_dir = "D:\\Workspace\\work_code\\Python_code\\NLP_project\\Final_Work\\use_codes"

# 确保保存目录存在
os.makedirs(save_dir, exist_ok=True)

# 遍历每个Entrez ID，构建URL并发送请求
for entrez_id in entrez_ids:
    url = base_url.format(entrez_id)
    response = requests.get(url)
    
    if response.status_code == 200:
        # 构建保存文件的路径
        save_path = os.path.join(save_dir, f"{entrez_id}_disease.txt")
        
        # 将响应内容写入文件
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"成功下载并保存 {entrez_id} 的疾病信息到 {save_path}")
    else:
        print(f"下载 {entrez_id} 的疾病信息失败，状态码: {response.status_code}")