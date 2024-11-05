#使用powershell代码爬取文本内容

# 设置查询关键词
$search_term = "Metastatic Prostate Cancer"

# 定义API Key（可选），如果没有API Key，可以留空
$api_key = "" 

# 定义PMID列表文件和保存文献摘要的文件
$input_file = "pmid_list.txt"
$output_file = "pubmed_articles.txt"

# 清空/初始化输出文件
Clear-Content $output_file

# 1. 获取PMID列表，使用usehistory保存查询结果
Write-Host "Fetching PMIDs for '$search_term'..." 

# 使用esearch获取PMID，检索所有相关文献，并按日期排序（从最早到最新）
if ($api_key -eq "") {
    $esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed`&term=$search_term`&usehistory=y`&retmax=2000`&retmode=json`&sort=pubdate"
} else {
    $esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed`&term=$search_term`&usehistory=y`&retmax=2000`&retmode=json`&sort=pubdate`&api_key=$api_key"
}

# 发起请求并解析响应
$query_info = Invoke-RestMethod -Uri $esearch_url
$web_env = $query_info.esearchresult.webenv
$query_key = $query_info.esearchresult.querykey
$count = $query_info.esearchresult.count

# 保存PMID到文件
$query_info.esearchresult.idlist | Out-File -FilePath $input_file
Write-Host "PMID list saved to $input_file."

# 2. 根据PMID下载文献摘要，并合并保存到一个文件
Write-Host "Starting to download abstracts and save to $output_file..."

# 设置每次检索返回的文献数量
$retstart = 0
$retmax = 1

# 循环获取文献摘要，直到检索到所有文献
while ($retstart -lt $count) {
    # 使用efetch获取文献摘要
    if ($api_key -eq "") {
        $efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed`&query_key=$query_key`&WebEnv=$web_env`&retstart=$retstart`&retmax=$retmax`&retmode=text`&rettype=abstract"
    } else {
        $efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed`&query_key=$query_key`&WebEnv=$web_env`&retstart=$retstart`&retmax=$retmax`&retmode=text`&rettype=abstract`&api_key=$api_key"
    }

    # 下载文献摘要并追加到输出文件
    $abstracts = Invoke-RestMethod -Uri $efetch_url
    Add-Content -Path $output_file -Value $abstracts

    # 更新retstart，准备获取下一篇文献摘要
    $retstart += $retmax

    # 防止频繁请求导致限流
    Start-Sleep -Seconds 5.8
}

Write-Host "All abstracts have been downloaded and saved to $output_file."
