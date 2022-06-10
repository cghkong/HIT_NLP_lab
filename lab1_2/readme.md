#汉语自动分词系统使用手册

##文件夹说明
源文件在result_file根目录下，生成文件在各个文件夹中。data用来存储划分的训练文件、测试文件、标准文件，用于k次交叉检验；
dic是各种词典的文件夹；hmm是HMM模型参数的文件夹；score是各种分词算法或模型的分词效果分析的文件夹；
seg是用来存储各种生成的分词结果文件，包括seg_LM.txt也在其中

##程序说明
HMM.py是构建隐马尔可夫模型。
Statistic_language_system.py是一元和二元+HMM分词系统。
utils.py是辅助函数工具包，用来分析分词的score等功能。
test.py是测试代码各部分的功能。
main.py是使用二元文法+HMM测试新的数据集。


##q：如何使用二元文法系统测试新的测试集
> 将新的测试集放在result_file根目录下（与198801_sent.txt同一级目录），并将测试集命名为test.txt。
> 然后直接运行main.py程序即可，输出文件在result_file/seg/seg_LM.txt中。
> 主要注意的是，测试集的编码方式必须是gbk，输出文件seg_LM的编码格式为utf-8。

##q: 生成分词文件seg_LM的文件格式
>每个词通过'/ '来分隔，文件编码为utf-8


##其它问题
请联系我，2718458514@qq.com
