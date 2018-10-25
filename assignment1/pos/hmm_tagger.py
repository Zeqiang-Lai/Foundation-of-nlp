# coding=utf-8

import sys
import os
sys.path.append('..')
import utilities
from shared import hmm

class HmmTagger(hmm.BaseHmmTagger):
    """ 采用隐式马尔可夫模型的中文词性标注器
    """
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
    script_dir = os.path.dirname(__file__)
    corpus_path = os.path.join(script_dir, 'datasets/199801.txt')
    corpus = utilities.load_renmin(corpus_path)
    tagger = HmmTagger()
    # tagger.train(corpus)
    # tagger.save("hmm_para")
    model_path = os.path.join(script_dir, "hmm_para")
    tagger.load(model_path)
    seq = ['19980101-01-001-002','中共中央','总书记', '、', '国家', '主席', '江', '泽民']
    tags = tagger.tag(seq)   
    print(" ".join(tags))
     
   