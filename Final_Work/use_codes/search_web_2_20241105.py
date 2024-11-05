# 关联疾病文献检索，就是找我们筛选出来的基因关联了HPO疾病表型后，有没有相关的文献

import os
import requests
import xml.etree.ElementTree as ET
import time
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Step 1: 使用esearch获取PMID列表
def get_pmids(keyword, retmax=50):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={keyword}&retmax={retmax}&retmode=json"
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    data = response.json()
    return data['esearchresult']['idlist']

# Step 2: 使用efetch获取摘要并保存为TSV文件
def fetch_and_save_abstracts(pmids, disease_keyword, output_file="abstracts_by_disease2.tsv"):
    # 设置重试机制
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:  # 使用追加模式
        writer = csv.writer(file, delimiter='\t')
        
        for pmid in pmids:
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
            
            try:
                response = session.get(url)
                response.raise_for_status()  # 检查请求是否成功
                root = ET.fromstring(response.content)
                
                # 提取摘要文本
                abstract_text = ""
                for abstract in root.findall(".//Abstract/AbstractText"):
                    abstract_text += abstract.text if abstract.text else ""
                
                # 将PMID和摘要写入TSV文件，标记疾病表型关键词
                writer.writerow([disease_keyword, pmid, abstract_text])
                
                # 休息5秒
                time.sleep(5)
                print(f"Downloaded PMID: {pmid} for keyword: {disease_keyword}")
            
            except requests.exceptions.RequestException as e:
                print(f"Error fetching PMID {pmid}: {e}")

    print(f"All abstracts for {disease_keyword} saved to {output_file}")

# Step 3: 读取疾病表型关键词
def get_disease_keywords_from_txt(folder_path):
    keywords = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, mode='r', encoding='utf-8') as f:
                for line in f:
                    # 假设每行都是一个名称，可以根据实际情况调整
                    keywords.append(line.strip())
    return keywords

# 主程序
if __name__ == "__main__":
    folder_path = r"D:\Workspace\work_code\Python_code\NLP_project\Final_Work\use_codes\6个关键基因HPO"
    disease_keywords = get_disease_keywords_from_txt(folder_path)

    # 构建基础搜索关键词
    base_keyword = '(Prostate Cancer[Title/Abstract] OR Prostatic Neoplasms[MeSH]) AND (Metastasis[Title/Abstract] OR Neoplasm Metastasis[MeSH]) AND (Mechanism OR Therapy OR Biomarkers)'
    
    # 清空输出文件并写入标题
    output_file = "abstracts_by_disease2.tsv"
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Disease Keyword', 'PMID', 'Abstract'])  # 写入TSV文件的标题行

    # 针对每个疾病表型关键词进行检索
    for disease_keyword in disease_keywords:
        keyword = f'({base_keyword}) AND ("{disease_keyword}")'
        pmids = get_pmids(keyword)
        
        if pmids:  # 检查是否获取到PMID
            fetch_and_save_abstracts(pmids, disease_keyword, output_file)
        else:
            print(f"No PMIDs found for keyword: {disease_keyword}. Skipping.")
