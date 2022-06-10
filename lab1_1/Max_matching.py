from utils import process_line
from building_dic import configure
Test_File = configure['Test_File']


#最小代码的最大长度匹配（优化前）
class Matching:
    def __init__(self):
        self.Max_length = 0
        self.dic_words = []
        self.dic_path='result_file/dic/dic.txt'
        with open(self.dic_path, 'r', encoding='utf-8') as dic_file:
            lines = dic_file.readlines()  # 读取词典中的词
        for line in lines:
            self.dic_words.append(line[0:len(line) - 1])  # 将该词加入词典列表中
            self.Max_length = len(line) - 1 if len(line) - 1 > self.Max_length else self.Max_length  # 更新最大词长

    # 正向最大匹配分词,要求最小代码
    def FMM(self,input_path=Test_File, FMM_path='result_file/seg/seg_FMM.txt'):
        with open(input_path, 'r', encoding='gbk') as input_file:    # 读取文件
            input_lines = input_file.readlines()
        input_file.close()          # 关闭文件
        FMM_file = open(FMM_path, 'w', encoding='utf-8')  #打开写入文件
        for id,line in enumerate(input_lines):
            single_line=''        #存储一行的结果
            line = line[:len(line) - 1]   #去掉最后一个换行符
            while len(line) > 0:
                search_word = line[0:len(line) if len(line) < self.Max_length else self.Max_length]  #以最大长度开始搜索匹配
                while search_word not in self.dic_words:
                    if len(search_word) == 1:  # 字串长度为1，跳出循环
                        break
                    search_word = search_word[0:len(search_word) - 1]  # 减小词长
                line = line[len(search_word):]  # 更新剩余的待分词
                single_line += search_word + '/ '  # 得到一个分词结果
            FMM_file.write(process_line(single_line) + '\n')  # 写入文件
        FMM_file.close()

    # 逆向最大匹配分词，要求最小代码
    def BMM(self,input_path=Test_File, BMM_path='result_file/seg/seg_BMM.txt'):
        with open(input_path, 'r', encoding='gbk') as input_file:
            input_lines = input_file.readlines()
        input_file.close()
        BMM_file = open(BMM_path, 'w', encoding='utf-8')
        for id,line in enumerate(input_lines):
            line = line[:len(line) - 1]  # 去掉最后一个换行符
            seg_list = []  # 保存后向匹配得到的一个词
            while len(line) > 0:
                if len(line) < self.Max_length:           #从最大长度开始匹配
                    search_word=line
                else:
                    search_word=line[len(line) - self.Max_length:]
                while search_word not in self.dic_words:
                    if len(search_word) == 1:  # 字串长度为1，跳出循环
                        break
                    search_word = search_word[1:]  # 长度减一
                seg_list.insert(0, search_word + '/ ')  # 将该分词的结果保存
                line = line[:len(line) - len(search_word)]  # 更新剩余的待分词
            BMM_file.write(process_line(''.join(seg_list)) + '\n')  # 写入一行分词结果
        BMM_file.close()
