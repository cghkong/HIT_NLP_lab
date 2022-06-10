# 1. 工程文件结构
### 1.1 building_dic.py
> 该部分使用了7/8的199801_seg&pos.txt和全部的199802.txt来构建词典，构建的词典不添加量词。
> 同时取出了1/8的199801_seg&pos.txt作为一个测试集test_k.txt
### 1.2 Max_matching.py
> FMM和BMM算法
> 输入测试文件为全部的199801_sent.txt
### 1.3 Optimize_Matching.py
> 优化后的FMM和BMM算法
### 1.4 Hash_Trie.py
> 用于优化的Trie树（数据结构）
### 1.5 score_analysis.py
> FMM和BMM的算法分析，主要计算准确率、召回率、F值，此外还计算优化后的运行时间，FMM和BMM的分析差异，以及FMM和BMM的错误词性统计
### 1.6 utils.py
> 工具包，为其它部分提供相应功能的函数

#2. 注意事项
### 2.1 文件格式
> 除老师给出的文件均为gbk编码外，程序生成的所有文件均为utf-8编码
### 2.2 测试集读入
> 如果需要使用新的测试文件，有两种方式
> 方式-：删除199801_sent.txt文件，将新的测试文件命名为199801_sent.txt,直接放在result_file文件夹中，务必确保编码格式gbk

> 方式二（不推荐）：修改building_dic.py文件中的configure配置信息，将'Test_File'对应的value修改为新测试文件的路径，文件编码依然为gbk

> 注意：修改测试文件之后，请不要再调用score_analysis.py程序分析,除非同时将199801_seg&pos.txt修改为标准分词答案文件，或修改程序中的标准文件路径
### 其它问题
> 请联系@我, email:2718458514@qq.com
