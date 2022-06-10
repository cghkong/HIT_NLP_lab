from HMM import Train_Args
from utils import score
from Statistic_language_system import Dic_one_gram,Dic_two_gram

'''
注意：将要测试的文件test.txt放在result_file根目录下后，再运行此程序
'''

if __name__ == '__main__':
    print('利用二元文法+HMM测试新的数据集')
    Train_Args.tag_doc()
    Dic_one_gram.generate_uni_dic()
    Dic_two_gram.generate_bi_dic()

    Train_Args.get_args()
    Dic_one_gram.get_uni_dic()
    Dic_two_gram.get_bi_dic()
    Dic_two_gram.bigram_newdata()


    '''
    这里提供对于生成文件seg_LM的效果分析的接口，可用于计算分词的准确率、召回率、F值,生成的分析文件为score_LM.txt（score目录中）
    但需要把标准答案的文件放在与测试文件同一级目录，文件的分词格式和编码格式需要和199801_seg%pos.txt保持一致,
    且文件命名为std.txt
    '''

    '''
    score(my_seg_encoding='utf-8', score_path='result_file/score/score_LM.txt',
                     std_seg_encoding='gbk', std_seg_path='result_file/std.txt',
                     my_seg_path='result_file/seg/seg_LM.txt')
    '''