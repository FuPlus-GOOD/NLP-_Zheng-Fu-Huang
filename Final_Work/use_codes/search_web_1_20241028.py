# 这个是用来找前列腺癌迁移相关文献的爬虫代码，找到这些文献后用来筛选关键词

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
def fetch_and_save_abstracts(pmids, output_file="abstracts2.tsv"):
    # 设置重试机制
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['PMID', 'Abstract'])  # 写入TSV文件的标题行
        
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
                
                # 将PMID和摘要写入TSV文件
                writer.writerow([pmid, abstract_text])
                
                # 休息5秒
                time.sleep(5)
                print(f"Downloaded PMID: {pmid}")
            
            except requests.exceptions.RequestException as e:
                print(f"Error fetching PMID {pmid}: {e}")
    
    print(f"All abstracts saved to {output_file}")

# 使用示例 - 根据优化后的检索关键词组合
keyword = '(Prostate Cancer[Title/Abstract] OR Prostatic Neoplasms[MeSH]) AND (Metastasis[Title/Abstract] OR Neoplasm Metastasis[MeSH]) AND (Mechanism OR Therapy OR Biomarkers) AND ("2018/01/01"[Date - Publication] : "3000"[Date - Publication])'
pmids = get_pmids(keyword)
fetch_and_save_abstracts(pmids)

