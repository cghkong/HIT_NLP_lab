from math import log

Test_File = 'result_file/data/test.txt'
Train_File = 'result_file/data/train.txt'
Min = -1.0e+100  # 表示最小值
Pre_State = {'B': 'ES', 'M': 'MB', 'S': 'SE', 'E': 'BM'}  # 表示一个标记的前一个可能的标记
Pi = {}  # 初始状态集Π
A = {}  # 计算状态转移概率
B = {}  # 计算观测概率
States = ['B', 'M', 'E', 'S']  # 状态列表
State_Count = {}  # 保存状态出现次数
Word_Count = 0  # 用于计算总的词数
Word_Dic = set()  # 保存所有的词


#训练HMM的参数a（状态转移矩阵），b(观测概率举证），pi（初始概率）
class Train_Args:
    @staticmethod  # 初始化待统计的参数λ并配置所有的词
    def init():
        global Word_Count, Word_Dic
        Word_Count = 0
        Word_Dic = set()
        for state in States:
            Pi[state] = 0.0
            State_Count[state] = 0
            B[state], A[state] = {}, {}
            for state_1 in States:
                A[state][state_1] = 0.0  # 由state转换为state_1概率初始化

    @staticmethod  # 将训练得到的参数写入文本文件中，便于以后分析
    def generate_args(pi_path='result_file/hmm/pi.txt', a_path='result_file/hmm/a.txt',
                     b_path='result_file/hmm/b.txt'):
        pi_file = open(pi_path, 'w', encoding='utf-8')
        a_file = open(a_path, 'w', encoding='utf-8')
        b_file = open(b_path, 'w', encoding='utf-8')
        for state in States:  # 将参数写入文本文件中
            pi_file.write(state + ' ' + str(Pi[state]) + '\n')
            a_file.write(state + '\n')
            b_file.write(state + '\n')
            for state_1 in States:
                a_file.write(' ' + state_1 + ' ' + str(A[state][state_1]) + '\n')
            for word in B[state].keys():
                b_file.write(' ' + word + ' ' + str(B[state][word]) + '\n')

    @staticmethod
    def tag_line(line):
        global Word_Count
        line_word, line_tag = [], []
        for word in line.split():
            word = word[1 if word[0] == '[' else 0:word.index('/')]  # 取出一个词
            line_word.extend(list(word))
            Word_Dic.add(word)
            Word_Count += 1
            if len(word) == 1:
                line_tag.append('S')
                Pi['S'] += 1
            else:
                line_tag.append('B')
                line_tag.extend(['M'] * (len(word) - 2))
                line_tag.append('E')
                Pi['B'] += 1
        return line_word, line_tag

    @staticmethod
    # 标注文件中分词的词位，并计算各个参数
    def tag_doc(train_txt=Train_File):
        Train_Args.init()  # 初始化参数
        with open(train_txt, 'r', encoding='utf-8') as txt_f:
            lines = txt_f.readlines()
        for line in lines:
            if line == '\n':
                continue
            line_word, line_tag = Train_Args.tag_line(line)
            for i in range(len(line_tag)):
                State_Count[line_tag[i]] += 1
                B[line_tag[i]][line_word[i]] = B[line_tag[i]].get(line_word[i], 0) + 1
                if i > 0:
                    A[line_tag[i - 1]][line_tag[i]] += 1
        for state in States:
            Pi[state] = Min if Pi[state] == 0 else log(Pi[state] / Word_Count)
            for state_1 in States:
                A[state][state_1] = Min if A[state][state_1] == 0 else log(
                    A[state][state_1] / State_Count[state])
            for word in B[state].keys():
                B[state][word] = log(B[state][word] / State_Count[state])
        Train_Args.generate_args()

    @staticmethod
    def process_dic(word_path='result_file/dic/bi_gram_dic.txt'):
        with open(word_path,'r',encoding='utf-8') as file1:
            lines = file1.readlines()
        delete_list = []
        for id,line in enumerate(lines):
            strline = line.split(' ')
            if len(strline)!=3:
                delete_list.append(id)
                continue
            if len(strline[0])==19:
                delete_list.append(id)
        for id in reversed(delete_list):
            del lines[id]
        return lines


    @staticmethod
    def get_args(pi_path='result_file/hmm/pi.txt', a_path='result_file/hmm/a.txt',
                 b_path='result_file/hmm/b.txt', word_path='result_file/dic/bi_gram_dic.txt'):
        Train_Args.init()
        pi_lines = open(pi_path, 'r', encoding='utf-8').readlines()
        a_lines = open(a_path, 'r', encoding='utf-8').readlines()
        b_lines = open(b_path, 'r', encoding='utf-8').readlines()
        word_lines = open(word_path, 'r', encoding='utf-8').readlines()
        for word in word_lines:
            Word_Dic.add(word.split()[0])
        for idx in range(4):  # 配置Pi参数
            pi_state, pi_pos = pi_lines[idx].split()[0:2]
            Pi[pi_state] = float(pi_pos)
        for idx in range(20):  # 配置A参数
            if idx % 5 != 0:
                A[States[int(idx / 5)]][States[idx % 5 - 1]] = float(a_lines[idx].split()[1])
        state = 'B'
        for idx in range(len(b_lines) - 1):
            if b_lines[idx][0] != ' ':
                state = b_lines[idx][0]
            else:
                word, pos = b_lines[idx].split()[0:2]
                B[state][word] = float(pos)


class HMM:

    @staticmethod
    def process_line(seg_line, choice=True):
        word_list = seg_line[:len(seg_line) - 2].split('/ ')
        seg_line, to_seg_word = '', ''
        for idx in range(len(word_list)):
            if len(word_list[idx]) == 1:
                if choice and word_list[idx] in Word_Dic:
                    if to_seg_word:
                        seg_line += HMM.process_word(to_seg_word)
                        to_seg_word = ''
                    seg_line += word_list[idx] + '/ '
                else:
                    to_seg_word += word_list[idx]
                    if idx + 1 == len(word_list):
                        seg_line += HMM.process_word(to_seg_word)
            else:
                if to_seg_word:  # 判断是否该词前面为单字
                    seg_line += HMM.process_word(to_seg_word)
                    to_seg_word = ''
                seg_line += word_list[idx] + '/ '
        return seg_line

    @staticmethod
    def process_word(to_seg_word):
        if len(to_seg_word) == 1:
            return to_seg_word + '/ '
        tag_list = HMM.viterbi(to_seg_word)[1]
        begin, next_i = 0, 0
        res_word = ''  # 输入的to_seg_word分词结果
        for idx, char in enumerate(to_seg_word):
            tag = tag_list[idx]  # 取一个tag
            if tag == 'B':  # 表示开始
                begin = idx
            elif tag == 'E':  # 表示结束
                res_word += to_seg_word[begin:idx + 1] + '/ '
                next_i = idx + 1
            elif tag == 'S':
                res_word += char + '/ '
                next_i = idx + 1
        if next_i < len(to_seg_word):
            res_word += to_seg_word[next_i:] + '/ '
        return res_word

    @staticmethod  # 维特比算法求解
    def viterbi(to_seg_word):
        v = [{}]
        path = {}
        for state in States:  # 初始化
            v[0][state] = Pi[state] + B[state].get(to_seg_word[0], Min)
            path[state] = [state]
        for idx in range(1, len(to_seg_word)):
            v.append({})
            new_path = {}
            for state_1 in States:
                em_p = B[state_1].get(to_seg_word[idx], Min)
                (prob, state) = max([(v[idx - 1][y0] + A[y0].get(state_1, Min) + em_p, y0) for y0 in
                                     Pre_State[state_1]])
                v[idx][state_1] = prob
                new_path[state_1] = path[state] + [state_1]
            path = new_path
        (prob, state) = max((v[len(to_seg_word) - 1][y], y) for y in 'ES')
        return prob, path[state]

    @staticmethod  # 使用HMM分词
    def hmm(txt_path=Test_File, hmm_path='result_file/seg/seg_hmm.txt'):
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(hmm_path, 'w', encoding='utf-8') as hmm_file:
            for line in lines:
                new_line = ''
                for word in line[0:len(line) - 1]:
                    new_line += word + '/ '
                new_line = HMM.process_line(new_line, False) if new_line else ''
                hmm_file.write(new_line + '\n')
