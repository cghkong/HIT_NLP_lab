configure={
    'Train_File' : 'result_file/data/train.txt',  # 生成的训练集文本文件路径
    'Test_File': 'result_file/199801_sent.txt',    #测试文件路径
    'test_file_k': 'result_file/data/test_k.txt',    #测试文件路径 1/k
    'Std_File': 'result_file/199801_seg&pos.txt',     #标准文件路径
    'std_file_k': 'result_file/data/std_k.txt',     #标准文件路径 1/k
    'seg&pos_path': 'result_file/199801_seg&pos.txt',
    '199802':'result_file/199802.txt',
    'sent_path': 'result_file/199801_sent.txt',
    'ratio1': 1,
}


class Dic:
    def __init__(self):
        self.train_path = configure['Train_File']
        self.test_path = configure['test_file_k']
        self.std_path = configure['std_file_k']
        self.seg_pos_path = configure['seg&pos_path']
        self.seg_199802 = configure['199802']
        self.sent_path = configure['sent_path']
        self.flag=True   #加入量词的标志位，True表示不加入
        self.k = configure['ratio1'] #抽取比例

    # 划分训练集和测试集
    def generate_train_test(self):
        #抽取训练集文件
        with open(self.seg_pos_path, 'r', encoding='gbk') as file1:
            std_seg_lines = file1.readlines()
        std_lines = []  # 用于输出标准分词答案
        with open(self.train_path, 'w', encoding='utf-8') as file2:
            for id, line in enumerate(std_seg_lines):
                if id % self.k != 0:
                    file2.write(line)  # 按照行数模K将该行作为训练行
                else:
                    std_lines.append(line)
        with open(self.std_path, 'w', encoding='utf-8') as file3:
            file3.write(''.join(std_lines))
        file2.close()
        file3.close()
        #抽取测试集文件
        with open(self.sent_path, 'r', encoding='gbk')as file4:
            std_sent_lines = file4.readlines()
        with open(self.test_path, 'w', encoding='utf-8') as file5:
            for id, line in enumerate(std_sent_lines):
                if id % self.k == 0:
                    file5.write(line)  # 按照行数模K将该行作为训练行
        file5.close()
        file4.close()

    # 生成词典
    def generate_dic(self, dic_path='result_file/dic/dic.txt'):
        max_len = 0  # 最大词长
        word_set = set()
        with open(self.train_path, 'r', encoding='utf-8') as file1:
            lines = file1.readlines()
        with open(dic_path, 'w', encoding='utf-8') as file2:
            for line in lines:
                for word in line.split():
                    if '/m' in word and self.flag:
                        continue
                    word = word[1 if word[0] == '[' else 0:word.index('/')]  # 去掉两个空格之间的非词字符
                    word_set.add(word)  # 将词加入词典
                    max_len = len(word) if len(word) > max_len else max_len  # 更新最大词长
            word_list = list(word_set)
            word_list.sort()  # 排序
            file2.write('\n'.join(word_list))
        file1.close()
        file2.close()
        return word_list, max_len

dic =Dic()
dic.generate_train_test()
dic.generate_dic()