from building_dic import Dic,configure
from utils import score
from Max_matching import Matching
from score_analysis import Score_Analysis
from Optimize_Matching import Matching_Optimize

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
    Score_Analysis.score(score_path='result_file/score/score.txt',std_encoding='gbk', std_path=configure['Std_File'],
          fmm_path='result_file/seg/seg_FMM.txt', bmm_path='result_file/seg/seg_BMM.txt')

# 测试代码优化后的最大匹配算法效果
def test_time():
    Score_Analysis.time_optimize()  # 分析两者的运行速度快慢，并记录在文件中io_file/time_cost.txt



if __name__ == '__main__':
    test_building_dic()  # 测试构建词典部分
    #test_Matching()  # 测试最少代码量实现机械匹配分词,时间较长，不推荐
    #test_score_analysis()  # 测试正反向分词效果分析
    test_Optimize_Matching()  # 运行优化后的机械匹配分词算法
    test_optimize_score_analysis() #优化后的效果分析
    #test_time()
