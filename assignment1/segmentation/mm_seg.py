#coding=utf-8

import dict_generator

class MMSeg:
    """ 基于最大匹配法(Maximum Matching)的中文分词器.

        必须提供词典路径,词典的编码方式.词典必须为json格式,且key值为词语.
        默认的词典加载方式为按需加载,可以使用下列函数手动加载.
        ```
        load_dict()
        ```
    """
    def __init__(self, dict_path, dict_encoding):
        self.dict_path = dict_path
        self.dict_encoding = dict_encoding
        self.corpus_dict = None

    def load_dict(self):
        """ 手动加载初始化时提供的词典.
        """
        self.corpus_dict = dict_generator.json_read(self.dict_path, 
                                                    encoding=self.dict_encoding)

    def cut(self, sent, mode='fmm'):
        """ 切分给定字符串,返回切分结果.

            Args:
              sent: 待切分字符串.
              mode: 选择不同的切分算法,可选值有:'fmm','bmm','bimm'.

            Returns:
              切分结果,一个列表,包含切分出来的各个词语.
        """
        if(mode not in ['fmm', 'bmm', 'bimm']):
            raise ValueError("invalid value for mode, only accept 'fmm', 'bmm' and 'bimm'")

        if(mode == 'fmm'):
            return self.__fmm_cut(sent)
        elif(mode == 'bmm'):
            return self.__bmm_cut(sent)
        else:
           return self.__bimm_cut(sent)

    def __fmm_cut(self, sent):
        """ 使用fmm(正向最大匹配算法)切分句子
        """
        if(self.corpus_dict == None):
            self.load_dict()

        result = []

        i, j = 0, len(sent)
        while i <= len(sent)-1:
            while i+1 < j:
                if(sent[i:j] in self.corpus_dict.keys()):
                    break
                else:
                    j -= 1
            result.append(sent[i:j])
            i = j
            j = len(sent)
        
        return result

    def __bmm_cut(self, sent):
        """ 使用bmm(反向最大匹配算法)切分句子
        """
        result = []
        # TODO: backward
        return result

    def __bimm_cut(self, sent):
        """ 使用bi-mm(双向最大匹配算法)切分句子
        """
        result = []
        # TODO: bidirectional
        return result
        
if __name__ == '__main__':
    s = "本报南昌讯记者鄢卫华报道：１７日上午，由本报和圣象·康树联合主办的瓦尔德内尔挑战赛在南昌圆满落幕。"
    print("原始句子:" + s + "\n")

    seg = MMSeg("dicts/dict.json", 'utf-16')
    # FMM前向算法测试
    print("----- FMM前向算法分词结果 -----")
    for word in seg.cut(s, mode='fmm'):
        print(word,end="/")
    print()

    # BMM后向算法测试
    print("----- BMM后向算法分词结果 -----")
    for word in seg.cut(s, mode='bmm'):
        print(word,end="/")
    print()

    # MM双向算法测试
    print("----- MM双向算法分词结果 -----")
    for word in seg.cut(s, mode='bimm'):
        print(word,end="/")
    print()