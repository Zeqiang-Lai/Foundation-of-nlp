# coding=utf-8

import sys
sys.path.append('..')
import utilities
from shared import hmm

class HmmTagger:
    """ 采用隐式马尔可夫模型的中文词性标注器
    """
    def __init__(self):
        self.builder = None
        self.hmm = None

    def train(self, corpus):
        """ 根据数据集构建隐式马尔可夫模型.

            可能耗费较长时间.
        """
        idxed_corpus, (self.obsv2idx, self.idx2obsv), (self.hide2idx, self.idx2hide) = hmm.index_corpus(corpus)
        self.builder = hmm.HmmMatBuilder(idxed_corpus, 
                                         len(self.obsv2idx.keys()),
                                         len(self.hide2idx.keys()))
        self.builder.build()

        self.hmm = hmm.Hmm()
        self.hmm.setup(self.builder.sp_mat, self.builder.tp_mat, self.builder.ep_mat, 
                       self.builder.num_obsv, self.builder.num_hide)

    def load(self, path):
        """ 加载模型 """
        self.obsv2idx, self.idx2obsv, self.hide2idx, self.idx2hide = hmm.load_dicts(path)
        self.builder = hmm.HmmMatBuilder()
        self.builder.load(path)

        self.hmm = hmm.Hmm()
        self.hmm.setup(self.builder.sp_mat, self.builder.tp_mat, self.builder.ep_mat, 
                       self.builder.num_obsv, self.builder.num_hide)

    def save(self, path):
        """ 保存模型 """
        self.builder.save(path)
        dicts = (self.obsv2idx, self.idx2obsv, self.hide2idx, self.idx2hide)
        hmm.save_dicts(dicts, path)

    def tag(self, sentence):
        """ 对给定句子进行词性标注,需要提前分词.

            Args:
              sentence: 元组,长度为句子包含的词语数.

            Returns:
              词性序列.
        """
        if self.hmm == None:
            raise Exception("You have to train or load model before tagging.")
        tags = []
        idxed_seq = [self.obsv2idx[obsv] for obsv in sentence]
        idxed_tag = self.hmm.find_hidden_state(idxed_seq)
        tags = [self.idx2hide[idx] for idx in idxed_tag]
        return tags       

if __name__ == '__main__':
    corpus = utilities.load_renmin('datasets/199801.txt')
    tagger = HmmTagger()
    # tagger.train(corpus)
    # tagger.save("hmm_para")
    tagger.load("hmm_para")
    seq = ['19980101-01-001-002','中共中央','总书记', '、', '国家', '主席', '江', '泽民']
    tags = tagger.tag(seq)   
    print(" ".join(tags))
     
   