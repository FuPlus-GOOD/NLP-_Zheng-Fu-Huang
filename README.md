# NLP-基于自然语言处理对前列腺癌迁移的知识图谱挖掘
##### 作者： 符家豪 郑杰 黄家璇


## 编者有话说
这个项目库是用于存储在我们课程项目推进过程中，用来实现最终结果的**代码、结果**以及其他**小尝试**

不过说实话讲道理，这次的探索大概率是没有什么特别的发现了。**（虽然老师说文本挖掘就是得先把现有的常识性规律整理出来）**

## （一）代码存放说明
简单讲讲各个分析流程模块的代码吧：

### 模块一：前期文本收集预处理

### 模块二：


## （二）小组讨论记录归档
再来谈谈我们关于这个项目的一系列想法的变化
### 2024-09-03 CLASS I  计划的初步敲定

**【主题】：**
    前列腺癌文本挖掘和知识发现

**【目标】：**
    探索前列腺癌细胞迁移（发病阶段）的影响因素和分子机制，包括环境影响、基因影响、遗传因素、激素水平、年龄层次等

**【计划】：**
    1、对文本内容关键词筛选（包括雄性激素、饮食习惯、血压）找到关键基因，对这些gene做GO/KEGG的功能富集。
    2、对筛选出的基因、表型、分子机制等根据文本内容做关系表（方法有待学习）
    3、对关系进行分类，按照对性状促进或抑制，按照发病症状，再按照发病阶段，做分类。
    4、希望得到对不同阶段病情有抑制病情作用的基因，以及这一套基因之间的关系。此外，再挖掘出针对不同阶段的前列腺癌的症状以及治疗方式做关联。

---

### 2024-09-10 CLASS II  关于词汇计算

**【不同类型的算法思想】：**
    词袋模型的TFIDF算法：实现对关键词汇的向量化表示

**【是否可用】：**
根据目前我们所看到的提前收集好的963条文本数据，我们小组计划进行对前列腺癌细胞迁移的相关文献，尝试对此类文献文本进行文本挖掘，试图找到有关癌细胞迁移的词汇。

**【获取数据】：**
    1 直接的文本资料→关键文本内容：
由于疾病的文本数据已经被筛选出来了，所以我们直接就下载就行
    2 关键文本内容→关键词提取：
采用词汇向量化操作提炼，面向“Sentence”列
        (1) 前期人工查找有关癌细胞迁移的词汇。
        (2) 将收集到的文本数据利用Doc2Vec模型、或者TF-IDF的方法将文本段落进行分类，根据前期寻找的与癌细胞迁移有关的tokens进行比对，找到我们感兴趣的tokens。

**【观察数据】：**
对得到的关键词进行人工筛选（二次筛选），寻找更适用于标注的目标关键词

---

### 2024-09-24 CLASS III  论文标题内容初定

**【论文标题预选方案1】：**
《利用文本挖掘办法，探索现有关于调控前列腺癌迁移的多层次相关因素》

**【关于后续目标的确认与确定】：**（只是单纯列举出点可能的对象）
    1.分子层面（重点探索）:相关基因 基因表达 表达产物 表达产物功能
    2.细胞层面：细胞类型  细胞功能  细胞代谢
    3.组织层面：组织类型  组织功能  组织代谢
    4.不过目前由于能力时间有限，只能专注于分子层面的探索，希望通过多轮筛选得到的关键基因或者关键表型

前列腺癌细胞在分子水平的基因调控关系：需要提前确认因果关系（是否有实实在在的关系）
        【不过需要注意的是，因果关系还是比较困难的，所以结果困难更偏向于相关性】

**【后续流程的过程细节丰富】：**
    1.第一次检查（寻找文本表型与已有知识比对）找关联因素
    2.筛选（增加新词汇，或留下与主题相关的词）
    3.关键词与基因ID绑定——再找文章（不要陷入文本，与数据库结合）
    4.找基因表型与数据库配对（联系基因和表型）

**【工具采纳选择】：**
    1.python包：NLTK
    2.额外数据库：KEGG
    3.正则表达式
    4.语言大模型：GPT-4...

---

### 2024-10-08 CLASS IV  短文内容方向敲定

**【短文提交】：**
    我们需要在10月17日之前将我们的初期结果转化为短文打印上交

---

### 2024-10-15 CLASS V 短文摘要

**【研究背景】：**

前列腺癌是全球男性中最常见的恶性肿瘤之一，其高转移性是导致患者死亡的主要原因之一，同时也是导致患者预后不良的主要原因。但从分子、细胞、组织三个层面将前列腺癌转移联系起来，以期望给予精准医疗更多细节。

**【研究问题】：**

为了深入理解前列腺癌细胞迁移的复杂机制，本研究从分子、细胞和组织三个层面构建了全面的知识图谱。

**【研究方法】：**

1. 我们通过针对CancerAlterome研究整理的964组关键词为"Prostate Adenocarcinoma"的文献数据，筛选有关前列腺癌扩散的影响基因
2. 通过GO富集（不同层面的）有相同功能的基因、HPO同样也进行富集
3. 比对HPO和GO的富集结果，分别对这些富集方式的结果交集、并集进行KEGG Pathway通路富集
4. 再通过KEGG Pathway 得到的通路关系，从CC BP MF三个层面进行联系
5. 收集目前对前列腺癌的精准治疗手段，将其与针对的基因相关联添加到通路图谱中，构建现有精准治疗手段与基因通路的关联图谱

**【研究结果】：**

目前我们研究发现，分子层面23个、细胞层面9个、组织层面6个与前列腺癌转移相关的关键词，并发现PSMA、Bone metastasis、AR、PTEN、BRCA1、BRCA2、ATM、CHEK2、CDK12对于前列腺癌转移有重要影响。

**【研究反思】：**

1. 通过文献查阅以及分词筛选关键词，存在词汇不统一的情况，推测存在筛选到目标结果缺少的情况。
2. 查找现有文献中有关前列腺癌的治疗手段时，可能存在时效性问题，有的方法可能被优化取代过了

---

### 2024-10-22 CLASS VI 老师批语

**论文目的：**

目的是探索，不是结果

如何评价结果：

方法准确性

1. 抽取关键词与目标文献的关联性，我们需要准备一系列与癌细胞迁移有关的文献作为评价标准
2. HPO匹配数据作为评价标准，为我们预测出来的结果做精准度检验

---

### 2024-10-29 CLASS VII 关于知识图谱的构建方法探索

前辈介绍方法：

* AGAC语料库（到时候去看看能不能拉出来用，这样说不定就不用我们自己找关键词了）
