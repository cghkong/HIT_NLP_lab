import time

from utils import compute_Acc_Recall_F,compare_difference,error_word
from Optimize_Matching import Matching_Optimize
from Max_matching import Matching


class Score_Analysis:
    @staticmethod
    #计算准确率、召回率、F值
    def score(score_path='result_file/score/score.txt', std_path='result_file/199801_seg&pos.txt',
              fmm_path='result_file/seg/seg_FMM.txt', bmm_path='result_file/seg/seg_BMM.txt',
              std_encoding='gbk', my_encoding='utf-8'):
        score_result = '本次评测得分\n'
        precision, recall, f_value = compute_Acc_Recall_F(std_path, fmm_path, std_encoding, my_encoding)  # FMM
        score_result += 'FMM准确率:\t' + str(precision * 100) + '%\nFMM召回率:\t' + str(recall * 100) + '%'
        score_result += "\nFMM的F值:\t" + str(f_value * 100) + '%\n\n'
        precision, recall, f_value = compute_Acc_Recall_F(std_path, bmm_path, std_encoding, my_encoding)  # BMM
        score_result += 'BMM准确率:\t' + str(precision * 100) + '%\nBMM召回率:\t' + str(recall * 100) + '%'
        score_result += "\nBMM的F值:\t" + str(f_value * 100) + "%\n\n"
        open(score_path, 'a', encoding='UTF-8').write(score_result)

    @staticmethod
    #统计出错词性
    def error_prep(result_path_fmm ='result_file/score/error_prep_FMM.txt',result_path_bmm='result_file/score/error_prep_BMM.txt' ):
        error_word(std_seg_path='result_file/199801_seg&pos.txt',my_seg_path='result_file/seg/seg_FMM.txt',result_path=result_path_fmm)
        error_word(std_seg_path='result_file/199801_seg&pos.txt',my_seg_path='result_file/seg/seg_BMM.txt',result_path=result_path_bmm)

    @staticmethod
    #测试时间cost
    def time_optimize(time_cost_path='result_file/score/time_cost.txt'):  # 用于评价实验第四部分做的优化时间对比
        print('测试运行时间')
        out_put_str = ''
        print('正在测试优化前的正向最大匹配运行')
        start_time = time.time()
        matching = Matching_Optimize()
        matching.fmm()  # 前向最大匹配
        fmm_time = time.time()
        print('正在测试优化前的逆向最大匹配运行')
        matching.bmm()  # 后向最大匹配
        bmm_time = time.time()
        out_put_str += '优化后：\n'
        out_put_str += 'FMM耗时\t' + str(fmm_time - start_time) + 's\n'
        out_put_str += 'BMM耗时\t' + str(bmm_time - fmm_time) + 's\n\n'
        with open(time_cost_path, 'a', encoding='utf-8')as time_cost_file:
            time_cost_file.write(out_put_str)

