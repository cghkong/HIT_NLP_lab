from collections import Counter


#加工处理分词得到的文件和标准文件，主要是处理有中括号的分词（[....]），将中括号里的词展开
def process_seg_list(seg_path, encoding):
    file = open(seg_path, 'r', encoding=encoding)
    seg_list = []  # 保存最后结果
    for line in file:
        if line == '\n':
            continue
        new_line = ''  # 保存处理过后的一行
        for word in line.split():
            new_line += word[1 if word[0] == '[' else 0:word.index('/')] + '/ '
        seg_list.append(new_line)
    return seg_list

#统计错误的词性,分析算法差异
def error_word(std_seg_path,my_seg_path,result_path,std_seg_encoding='utf-8',my_seg_encoding='utf-8'):
    standard_lines = process_seg_list(std_seg_path, std_seg_encoding)
    my_lines = process_seg_list(my_seg_path, my_seg_encoding)
    error_prep = []
    error_list = []
    for id,line1 in enumerate(standard_lines):
        line2 = my_lines[id]
        line1 = line1.split('/ ')
        line2 = line2.split('/ ')
        error_flag = [x not in line2 for x in line1]
        error_list.append(error_flag)
    with open(std_seg_path,'r',encoding=std_seg_encoding) as std_file:
        std_lines = std_file.readlines()
    count = 0
    for id ,std_line in enumerate(std_lines):
        if std_line=='\n':
            count += 1
            continue
        line = error_list[id-count]
        for i, mask in enumerate(line):
            if mask:
                std_line1 = std_line.split('  ')
                res = std_line1[i].split('/')
                if i==0:
                    continue
                error_prep.append(res[1])
    result = dict(Counter(error_prep))
    result1 = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
    with open(result_path,'w',encoding='utf-8') as outputfile:
        for x,y in result1.items():
            outputfile.write(x + ':' + str(y) + '\n')


#比较标准文本和我的输出文本，放回召回率，准确率，F值
def compute_Acc_Recall_F(std_seg_path, my_seg_path, std_seg_encoding, my_seg_encoding, k=1):
    std_seg_words, right_words_number, my_seg_words = 0, 0, 0
    Std_lines = process_seg_list(std_seg_path, std_seg_encoding)
    My_lines = process_seg_list(my_seg_path, my_seg_encoding)
    for idx, line in enumerate(Std_lines):
        line_words = line.split('/ ')  # 取出标准的分词文本中每行的词语
        my_line_words = My_lines[idx].split('/ ')  # 取对比文本中每行的词语
        len1 = len(line_words) - 1
        len2 = len(my_line_words) - 1
        std_seg_words += len1
        my_seg_words += len2
        i = j = 0
        word_numbers1, word_numbers2 = len(line_words[0]), len(my_line_words[0])
        while i < len1 and j < len2:
            if word_numbers1 == word_numbers2:
                right_words_number += 1
                if i == len1 - 1:
                    break
                i += 1
                j += 1
                word_numbers1 += len(line_words[i])
                word_numbers2 += len(my_line_words[j])
            else:
                while True:
                    if word_numbers1 < word_numbers2:
                        i += 1
                        word_numbers1 += len(line_words[i])
                    elif word_numbers1 > word_numbers2:
                        j += 1
                        word_numbers2 += len(my_line_words[j])
                    else:
                        if i < len1 - 1:
                            word_numbers1 += len(line_words[i + 1])
                            word_numbers2 += len(my_line_words[j + 1])
                        i += 1
                        j += 1
                        break
    precision = right_words_number / float(std_seg_words)
    recall = right_words_number / float(my_seg_words)
    f_value = (k * k + 1) * precision * recall / (k * k * precision + recall)
    return precision, recall, f_value


# 对自己的分词结果和标准结果进行比对，并输出结果到文件中
def score(std_seg_encoding='utf-8', my_seg_encoding='utf-8', score_path='result_file/score/score.txt',
          std_seg_path='result_file/199801_seg&pos.txt', my_seg_path='result_file/seg/uni_gram.txt'):
    print('本次评测得分结果将输出在文本中:\t' + score_path)
    precision, recall, f_value = compute_Acc_Recall_F(std_seg_path, my_seg_path, std_seg_encoding, my_seg_encoding)
    score_result = '标准文件:\t' + std_seg_path + '\n对比文件:\t' + my_seg_path + '\n'
    score_result += '准确率:\t' + str(precision * 100) + '%\n召回率:\t' + str(recall * 100) + '%\n'
    score_result += 'F值:\t' + str(f_value * 100) + '%\n\n'
    open(score_path, 'a', encoding='UTF-8').write(score_result)


def merge_data(path2='result_file/199802.txt',path1='result_file/data/train.txt'):
    with open(path1,'r',encoding='utf-8') as file1:
        lines1 = file1.readlines()
    with open(path2,'r',encoding='gbk') as file2:
        lines2 = file2.readlines()
    file2.close()
    file1.close()
    lines = lines1 + lines2
    file3 = open(path1,'w',encoding='utf-8')
    for id,line in enumerate(lines):
        file3.write(line)
    file3.close()