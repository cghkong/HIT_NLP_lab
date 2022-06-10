from building_dic import Dic,configure
from utils import score
from Max_matching import Matching
from score_analysis import Score_Analysis
from Optimize_Matching import Matching_Optimize
from Statistic_language_system import Dic_one_gram,Dic_two_gram
from HMM import HMM,Train_Args,Word_Dic

# 测试构建词典
def test_building_dic():
    print('构建词典')
    dic = Dic()
    dic.generate_train_test()  # 重新生成训练文件
    dic.generate_dic()  # 运行产生离线词典的程序


# 测试优化前的最大匹配分词
def test_Matching():
    print('测试最大匹配分词算法')
    dic = Dic()
    dic.generate_train_test()  # 重新生成训练文本
    dic.generate_dic()
    matching = Matching()
    matching.FMM()  # 前向最大匹配
    matching.BMM()  # 后向最大匹配


# 测试正反向分词效果分析
def test_score_analysis():
    print('测试最大匹配分词效果')
    Score_Analysis.score(std_encoding='gbk', std_path=configure['Std_File'],
          fmm_path='result_file/seg/seg_FMM.txt', bmm_path='result_file/seg/seg_BMM.txt')


# 最大匹配分词算法优化
def test_Optimize_Matching():
    print("测试优化后的最大匹配算法")
    Dic().generate_train_test()  # 重新分割数据
    matching_optimize = Matching_Optimize()
    matching_optimize.fmm()  # 前向最大匹配
    matching_optimize.bmm()  # 后向最大匹配

# 测试优化后的正反向分词效果分析
def test_optimize_score_analysis():
    print('测试优化后的最大匹配分词效果')
    Score_Analysis.score(score_path='result_file/score/score_optim.txt',std_encoding='gbk', std_path=configure['Std_File'],
          fmm_path='result_file/seg/seg_FMM.txt', bmm_path='result_file/seg/seg_BMM.txt')

# 测试代码优化后的最大匹配算法效果
def test_time():
    Score_Analysis.time_optimize()  # 分析两者的运行速度快慢，并记录在文件中io_file/time_cost.txt


# 测试一元文法+未登录词识别
def test_one_language():
    Dic().generate_train_test()
    print("训练参数")
    Dic_one_gram.generate_uni_dic()  # 产生离线词典并获得在线数据结构，在训练文本更新时，需要运行此行

    print('读取训练好的参数')
    Dic_one_gram.get_uni_dic()  # 读离线词典，得到必要的数据结构
    Dic_one_gram.unigram()  # 对文本文件进行分词
    print('评价一元文法分词结果，结果输出在result_file/score/score_uni_gram.txt中')
    score(my_seg_encoding='utf-8', score_path='result_file/score/score_uni_gram.txt',std_seg_encoding='gbk',
          std_seg_path=configure['Std_File'], my_seg_path='result_file/seg/uni_gram.txt')


# 测试二元文法+未登录词识别
def test_two_language():
    print('重新训练参数')
    Dic().generate_train_test()  # 生成训练文件
    Train_Args.tag_txt()  # 对训练文本重新进行训练，并将训练得到的参数写入文本文件中
    Dic_one_gram.generate_uni_dic()  # 产生离线词典并获得在线数据结构，在训练文本更新时，需运行此行
    Dic_two_gram.generate_bi_dic()  # 当二元文法词典改变时，需要运行此行

    print('读取训练好的参数')
    Train_Args.get_args()  # 从文本中读取HMM的训练参数
    Dic_one_gram.get_uni_dic()  # 必要的初始化，为了初始化一元文法模块中的Word_Freqs
    Dic_two_gram.get_bi_dic()  # 必要的初始化，为了初始化Bigram中的words_dic
    Dic_two_gram.bigram()

    print('评价二元文法分词结果，结果输出在result_file/score/score_bi_gram.txt中')
    score(my_seg_encoding='utf-8', score_path='result_file/score/score_bi_gram.txt',
                 std_seg_encoding='gbk', std_seg_path=configure['Std_File'],
                 my_seg_path='result_file/seg/bi_gram.txt')


# 测试纯HMM分词
def test_HMM():
    print('重新训练参数，重新构建词典')
    Dic().generate_train_test()  # 生成训练文件
    Train_Args.tag_txt()  # 对训练文本重新进行训练，并将训练得到的参数写入文本文件中

    print('读取训练好的参数')
    Train_Args.get_args()  # 从文本中读取HMM的训练参数
    Word_Dic.clear()
    HMM.hmm()  # 仅使用HMM分词
    print('正在对HMM分词结果评价，评价结果输出在result_file/score/score_HMM.txt中')
    score(my_seg_encoding='utf-8', score_path='result_file/score/score_HMM.txt',
                 std_seg_encoding='gbk', std_seg_path=configure['Std_File'],
                 my_seg_path='result_file/seg/seg_hmm.txt')


if __name__ == '__main__':
    #test_building_dic()  # 测试构建词典部分
    #test_Matching()  # 测试最少代码量实现机械匹配分词
    #test_score_analysis()  # 测试正反向分词效果分析
    #test_Optimize_Matching()  # 运行优化后的机械匹配分词算法
    #test_optimize_score_analysis() #优化后的效果分析
    #test_time()
    #test_one_language()  # 测试一元文法
    #test_two_language()  # 测试二元文法+未登录词识别
    test_HMM()  # 测试纯HMM分词
