from building_dic import configure
from building_dic import Dic
from Hash_Trie import Dic_Hash_Trie
from utils import process_line
Test_File = configure['Test_File']


class Matching_Optimize:
    def __init__(self):
        Dic_Hash_Trie.Words_List, max_len = Dic().generate_dic()  # 初始化词列表
        self.root1 = Dic_Hash_Trie.fmm_dic_root(dic_path='result_file/dic/dic.txt')  #创建FMM的Trie树
        self.root2 = Dic_Hash_Trie.bmm_dic_root(dic_path='result_file/dic/dic.txt')  #创建BMM的Trie树

    def fmm(self, input_path=Test_File, fmm_path='result_file/seg/seg_FMM.txt'):
        seg_result = ''
        with open(input_path, 'r', encoding='gbk') as file1: #读取测试文件
            for line in file1:
                seg_line = ''
                line = line[:len(line) - 1]  #去掉最后的换行符
                while len(line) > 0:      # 仍有单词待处理
                    count = 0
                    terminal_word = line[0]  #相当于最大长度等于该行的长度
                    node = self.root1.get_node(line[0]) #从第一个字符开始搜索Trie
                    while node is not None:   #node非空时，沿着trie匹配
                        count += 1
                        if node.ending_flag:   # 如果是终结符，得到该分词
                            terminal_word = line[:count]
                        if count == len(line):
                            break
                        node = node.get_node(line[count]) #搜索下一个字符的结点
                    line = line[len(terminal_word):]
                    seg_line += terminal_word + '/ '
                seg_result += process_line(seg_line) + '\n'
        with open(fmm_path, 'w', encoding='UTF-8') as file2:
            file2.write(seg_result)
        file1.close()
        file2.close()

    def bmm(self,input_path=Test_File, bmm_path='result_file/seg/seg_BMM.txt'):
        seg_result = ''
        with open(input_path, 'r', encoding='gbk') as file1:
            for line in file1:
                seg_list = []
                line = line[:len(line) - 1] #去掉最后的换行符
                while len(line) > 0:
                    count = len(line) - 1    #从最后一个字符开始匹配
                    terminal_word = line[count]
                    node = self.root2.get_node(line[count])
                    while node is not None:
                        if node.ending_flag:
                            terminal_word = line[count:]
                        count -= 1
                        if count < 0:
                            break
                        node = node.get_node(line[count])
                    line = line[:len(line) - len(terminal_word)]
                    seg_list.insert(0, terminal_word + '/ ')
                seg_result += process_line(''.join(seg_list)) + '\n'
        with open(bmm_path, 'w', encoding='UTF-8') as file2:
            file2.write(seg_result)
        file1.close()
        file2.close()

