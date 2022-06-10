from math import log
Test_File = 'result_file/data/test.txt'
Train_File1 = 'result_file/data/train.txt'
from HMM import HMM

Word_Freq = {}  # 用于保存词典中的词和词频
Word_Num_Count = 0  # 记录总词数

#一元文法
class Dic_one_gram:

    # 构建词典
    @staticmethod
    def generate_uni_dic(train_path=Train_File1, dic_path='result_file/dic/uni_gram_dic.txt'):
        global Word_Freq  # 保存到全局变量中
        with open(train_path,'r',encoding='utf-8') as seg_file:
            lines = seg_file.readlines()
        for line in lines:
            for word in line.split():
                word = word[1 if word[0] == '[' else 0:word.index('/')]
                Word_Freq[word] = Word_Freq.get(word, 0) + 1
        Word_Freq = {k: Word_Freq[k] for k in sorted(Word_Freq.keys())}  # 对词典排序
        with open(dic_path, 'w', encoding='utf-8') as dic_file:
            for word in Word_Freq.keys():
                dic_file.write(word + ' ' + str(Word_Freq[word]) + '\n')
        Word_Freq = {}
        Dic_one_gram.get_uni_dic(dic_path)

    # 获取词典
    @staticmethod
    def get_uni_dic(dic_path='result_file/dic/uni_gram_dic.txt'):
        global Word_Num_Count
        with open(dic_path, encoding='utf-8') as dic_file:
            lines = dic_file.readlines()
        for line in lines:
            word, freq = line.split()[0:2]
            Word_Freq[word] = int(freq)
            Word_Num_Count += int(freq)
            for count in range(1, len(word)):
                prefix_word = word[:count]
                if prefix_word not in Word_Freq:
                    Word_Freq[prefix_word] = 0

    # 通过词典构建无向图DAG
    @staticmethod
    def generate_dag(line):
        dag = {}
        n = len(line)
        for k in range(n):
            i = k
            dag[k] = []
            word_fragment = line[k]
            while i < n and word_fragment in Word_Freq:
                if Word_Freq[word_fragment] > 0:
                    dag[k].append(i)
                i += 1
                word_fragment = line[k:i + 1]
            dag[k].append(k) if not dag[k] else dag[k]
        return dag

    # 最大概率分词，用于概率最大路径计算
    @staticmethod
    def compute_maxprob_route(line, dag):
        n = len(line)
        route = {n: (0, 0)}
        log_total = log(Word_Num_Count)
        for idx in range(n - 1, -1, -1):  # 动态规划求最大路径
            route[idx] = max((log(Word_Freq.get(line[idx:x + 1], 0) or 1) - log_total +
                              route[x + 1][0], x) for x in dag[idx])
        return route

    # 对输入文本文件进行最大概率分词
    @staticmethod
    def unigram(input_path=Test_File, uni_path='result_file/seg/uni_gram.txt'):
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(uni_path, 'w', encoding='utf-8') as mwf_file:
            for line in lines:
                line = line[:len(line) - 1]
                line_route = Dic_one_gram.compute_maxprob_route(line, Dic_one_gram.generate_dag(line))
                old_start = 0
                seg_line = ''
                while old_start < len(line):
                    new_start = line_route[old_start][1] + 1
                    seg_line += line[old_start:new_start] + '/ '
                    old_start = new_start
                mwf_file.write(seg_line + '\n')


# 二元文法
class Dic_two_gram:
    words_dic = {}
    pun = ['？','。','，','：','；','“']

    @staticmethod
    def generate_bi_dic(train_path=Train_File1, dic_path='result_file/dic/bi_gram_dic.txt'):
        with open(train_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            if line == '\n':
                continue
            words = line.split()
            words.append('EOS/ ')
            words.insert(0, 'BOS')
            for idx in range(1, len(words)):
                words[idx] = words[idx][1 if words[idx][0] == '[' else 0:words[idx].index('/')]
                if words[idx] not in Dic_two_gram.words_dic.keys():
                    Dic_two_gram.words_dic[words[idx]] = {}
                if words[idx - 1] not in Dic_two_gram.words_dic[words[idx]].keys():
                    Dic_two_gram.words_dic[words[idx]][words[idx - 1]] = 0
                Dic_two_gram.words_dic[words[idx]][words[idx - 1]] += 1  # 更新词频
        Dic_two_gram.words_dic = {k: Dic_two_gram.words_dic[k] for k in
                               sorted(Dic_two_gram.words_dic.keys())}
        with open(dic_path, 'w', encoding='utf-8') as f:
            for word in Dic_two_gram.words_dic:
                Dic_two_gram.words_dic[word] = {k: Dic_two_gram.words_dic[word][k] for k in
                                             sorted(Dic_two_gram.words_dic[word].keys())}
                for pre in Dic_two_gram.words_dic[word]:
                    if pre=='BOS':
                        continue
                    if word=='BOS':
                        continue
                    if pre in Dic_two_gram.pun or word in Dic_two_gram.pun:
                        continue
                    f.write(word + ' ' + pre + ' ' + str(Dic_two_gram.words_dic[word][pre]) + '\n')

    @staticmethod
    def get_bi_dic(dic_path='result_file/dic/bi_gram_dic.txt'):
        with open(dic_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            word, pre_word, freq = line.split()[0:3]
            if word not in Dic_two_gram.words_dic.keys():
                Dic_two_gram.words_dic[word] = {pre_word: int(freq)}
            else:
                Dic_two_gram.words_dic[word][pre_word] = int(freq)

    @staticmethod
    #经过平滑处理
    def get_log_pos(pre_word, word, r=0.5):
        pre_word_freq = Word_Freq.get(pre_word, 0)  # 前词词频
        cur_word_freq = Word_Freq.get(word, 0)
        condition_word_freq = Dic_two_gram.words_dic.get(word, {}).get(pre_word, 0)  # 组合词频
        return r * (log(condition_word_freq + 1) - log(pre_word_freq + Word_Num_Count)) + (1 - r) * (log(cur_word_freq + 1) - log(Word_Num_Count))


    # 最大概率分词，用于概率最大路径计算
    @staticmethod
    def compute_maxprob_route(line, dag):
        n = len(line) - 3
        start = 3
        pre_graph = {'BOS': {}}
        word_graph = {}
        for x in dag[3]:
            pre_graph['BOS'][(3, x + 1)] = Dic_two_gram.get_log_pos('BOS', line[3:x + 1])
        while start < n:
            for idx in dag[start]:
                pre_word = line[start:idx + 1]
                temp = {}
                for next_end in dag[idx + 1]:
                    last_word = line[idx + 1:next_end + 1]
                    if line[idx + 1:next_end + 3] == 'EOS':
                        temp['EOS'] = Dic_two_gram.get_log_pos(pre_word, 'EOS')
                    else:
                        temp[(idx + 1, next_end + 1)] = Dic_two_gram.get_log_pos(pre_word, last_word)
                pre_graph[(start, idx + 1)] = temp
            start += 1
        pre_words = list(pre_graph.keys())
        for pre_word in pre_words:
            for word in pre_graph[pre_word].keys():
                word_graph[word] = word_graph.get(word, list())
                word_graph[word].append(pre_word)
        pre_words.append('EOS')
        route = {}
        for word in pre_words:
            if word == 'BOS':
                route[word] = (0.0, 'BOS')
            else:
                pre_list = word_graph.get(word, list())  # 取得该词对应的前词列表
                route[word] = (-65507, 'BOS') if not pre_list else max(
                    (pre_graph[pre][word] + route[pre][0], pre) for pre in pre_list)
        return route

    @staticmethod
    def bigram(input_path=Test_File, bigram_path='result_file/seg/bi_gram.txt'):
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(bigram_path, 'w', encoding='utf-8') as bigram_file:
            for line in lines:
                line = 'BOS' + line[:len(line) - 1] + 'EOS'
                dag = Dic_one_gram.generate_dag(line)
                line_route = Dic_two_gram.compute_maxprob_route(line, dag)
                seg_line = ''
                position = 'EOS'
                while True:
                    position = line_route[position][1]
                    if position == 'BOS':
                        break
                    seg_line = line[position[0]:position[1]] + '/ ' + seg_line
                seg_line = HMM.process_line(seg_line) if seg_line else ''  # 未登录词处理
                bigram_file.write(seg_line + '\n')  # 写入分词文件中

    @staticmethod
    def bigram_newdata(input_path='result_file/test.txt', bigram_path='result_file/seg/seg_LM.txt'):
        with open(input_path, 'r', encoding='gbk') as f:
            lines = f.readlines()
        with open(bigram_path, 'w', encoding='utf-8') as bigram_file:
            for line in lines:
                line = 'BOS' + line[:len(line) - 1] + 'EOS'
                dag = Dic_one_gram.generate_dag(line)
                line_route = Dic_two_gram.compute_maxprob_route(line, dag)
                seg_line = ''
                position = 'EOS'
                while True:
                    position = line_route[position][1]
                    if position == 'BOS':
                        break
                    seg_line = line[position[0]:position[1]] + '/ ' + seg_line
                seg_line = HMM.process_line(seg_line) if seg_line else ''  # 未登录词处理
                bigram_file.write(seg_line + '\n')  # 写入分词文件中
