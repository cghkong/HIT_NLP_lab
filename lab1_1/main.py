from building_dic import Dic
from HMM import Train_Args
from Statistic_language_system import Dic_two_gram,Dic_one_gram

Dic().generate_train_test()  # 生成训练文件
Train_Args.tag_txt()  # 对训练文本重新进行训练，并将训练得到的参数写入文本文件中
Dic_one_gram.generate_uni_dic()  # 产生离线词典并获得在线数据结构，在训练文本更新时，需运行此行
Dic_two_gram.generate_bi_dic()  # 当二元文法词典改变时，需要运行此行

print('读取训练好的参数')
Train_Args.get_args()  # 从文本中读取HMM的训练参数
Dic_one_gram.get_uni_dic()  # 必要的初始化，为了初始化一元文法模块中的Word_Freqs
Dic_two_gram.get_bi_dic()  # 必要的初始化，为了初始化Bigram中的words_dic
Dic_two_gram.bigram()
