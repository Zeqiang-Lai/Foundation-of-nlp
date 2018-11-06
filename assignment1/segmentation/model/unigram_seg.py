# coding=utf-8
from . import dict_generator
import math

class UniGramSeg:
    """ 基于词典以及1-gram的中文分词器. """
    def __init__(self):
        self.dict = None

    def set_dict(self, mdict):
        """ 设置词典. """
        self.dict = mdict
    
    def cut(self, sent, smooth='good_turing'):
        """ 切分给定字符串,返回切分结果.

            Args:
              sent: 待切分字符串.
              smooth: 选择不同的平滑算法,可选值有:.

            Returns:
              切分结果,一个列表,包含切分出来的各个词语.
        """
        if(smooth not in ['good_turing', 'add1']):
            raise ValueError("invalid value for smooth, only accept good_turing', 'plus1'")

        if(smooth == 'good_turing'):
            return self.__cut(sent)
        else:
           return self.__cut(sent)   

    def __cut(self, sent):

        log = lambda x: float('-inf') if not x else math.log(x)
        # freq = lambda x: self.dict[x] if x in self.dict else 0 if len(x)>1 else 1  # 计算每个词的频次（加入平滑）

        l = len(sent)
        maxsum = [0] * (l+1)	# 以i-1为一个词的结尾的最大log和
        cp = [0] * (l+1)	# cut point(分割点的位置)

        # DP
        for i in range(1, l+1):
            maxsum[i], cp[i] = max([(log(self.freq(sent[k:i]) / self.dict['_t_']) + maxsum[k], k) for k in range(0, i)])

        # 回溯构建分出来的词语
        words = []
        lo, hi = 0, l
        while hi != 0:
            lo = cp[hi]
            words.append(sent[lo:hi])
            hi = lo

        return list(reversed(words))

    def __is_date_or_number(self, string):
        '''判断一个字符串是否为数字或者日期
        '''
        length = len(string)
        if(length < 2):
            return 0

        if(string.isdigit()):
            return 1
        elif((string[length-1]=='年' or string[length-1]=='月' or string[length-1]=='日'or string[length-1]=='时'
              or string[length-1]=='分') and string[0:length-2].isdigit()):
            return 1
        elif(length == 2 and(string[length-1]=='年' or string[length-1]=='月' or string[length-1]=='日'
                or string[length-1]=='时' or string[length-1]=='分') and string[0].isdigit()):
            return 1
        else:
            return 0

    def freq(self, x):
        # print(x)
        if x in self.dict:
            return self.dict[x] 
        elif self.__is_date_or_number(x):
            return max(self.dict.values()) / len(self.dict)
        elif len(x)>1:  
            return 0  # 不是单字的没有概率
        else:
            return 1  # 单字的不在词典的话有1

    

if __name__ == '__main__':
    # s = '其中最简单的就是最大匹配的中文分词'
    s = "本报南昌讯记者鄢卫华报道：１７日上午，由本报和圣象·康树联合主办的瓦尔德内尔挑战赛在南昌圆满落幕。"
    
    seg = UniGramSeg()
    mdict = dict_generator.load_sogou_dict('datasets/SogouLabDic.dic')
    seg.set_dict(mdict)
    
    words = seg.cut(s)

    print("/".join(words))