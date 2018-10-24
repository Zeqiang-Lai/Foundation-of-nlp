# coding=utf-8

import numpy as np
import utilities

class Hmm:
    """ 通用隐式马尔可夫模型.
    """
    def __init__(self):
        pass

    def setup(self, sp_mat, tp_mat, ep_mat, num_obsv, num_hide):
        """ 初始化马尔可夫模型,提供必要的参数

            Args:
              sp_mat: 初始概率矩阵
              tp_mat: 转移概率矩阵
              ep_mat: 发射概率矩阵
              num_obsv: 观察值种类数量
              num_hide: 隐藏值种类数量
        """
        self.sp_mat = sp_mat
        self.tp_mat = tp_mat
        self.ep_mat = ep_mat
        self.num_obsv = num_obsv
        self.num_hide = num_hide

    def find_hidden_state(self, obsv_seq):
        """ 给定观察序列,使用维特比算法寻找最可能的隐藏序列.
        """
        return self.__veterbi(obsv_seq)    
    
    def __veterbi(self, obsv_seq):
        # 初始化
        len_seq = len(obsv_seq)
        f = np.zeros([len_seq, self.num_hide])
        f_arg = np.zeros([len_seq, self.num_hide], dtype=int)
        # print(f.shape)
        for i in range(0, self.num_hide):
            f[0, i] = self.sp_mat[i] * self.ep_mat[obsv_seq[0], i]
            f_arg[0, i] = 0

        # 动态规划求解
        for i in range(1, len_seq):
            for j in range(self.num_hide):
                fs = [f[i-1, k] * self.tp_mat[j, k] * self.ep_mat[obsv_seq[i], j] 
                               for k in range(self.num_hide)]
                f[i, j] = max(fs)
                f_arg[i, j] = np.argmax(fs)
        
        # 反向求解最好的隐藏序列
        hidden_seq = [0] * len_seq
        z = np.argmax(f[len_seq-1, self.num_hide-1])
        hidden_seq[len_seq-1] = z
        for i in reversed(range(1, len_seq)):
            z = f_arg[i, z]
            hidden_seq[i-1] = z
        
        return hidden_seq

class HmmMatBuilder():
    """ 该类包含构建隐式马尔可夫模型所需矩阵的函数.
    """
    def __init__(self, corpus, num_obsv, num_hide):
        """ 初始化
            
            Args:
              corpus: 数据集
              num_obsv: 观察状态数
              num_hide: 隐藏状态数

            数据集格式要求如下:
              一个列表,列表内容为一系列列表,每个列表包含观察序列及其对应的隐藏序列. 
              示例:[[(观察值,隐藏值),...],[...],...]
              观察值和隐藏值需要提前索引,这里将采用观测值和隐藏值作为矩阵的下标,
              因此其值必须为整型.
        """
        self.corpus = corpus
        self.num_obsv = num_obsv
        self.num_hide = num_hide

    def build(self):
        """ 构建初始概率矩阵,转移概率矩阵以及发射概率矩阵.
        """
        self.sp_mat = np.zeros(self.num_hide)
        self.tp_mat = np.zeros([self.num_hide, self.num_hide])
        self.ep_mat = np.zeros([self.num_obsv, self.num_hide])

        for seq in self.corpus:
            for i in range(len(seq)):
                obsv_cur, hide_cur = seq[i]
                
                if(i == 0):
                    self.sp_mat[hide_cur] += 1
                else:
                    obsv_pre, hide_pre = seq[i-1]
                    self.tp_mat[hide_cur, hide_pre] += 1
                
                self.ep_mat[obsv_cur, hide_cur] += 1

        # 加1平滑
        self.sp_mat += 1
        self.tp_mat += 1
        self.ep_mat += 1

        self.sp_mat /= self.sp_mat.sum()
        self.tp_mat /= self.tp_mat.sum(axis=1)[:,None]
        self.ep_mat /= self.ep_mat.sum(axis=1)[:,None]

        # self.sp_mat *= 1e3
        # self.tp_mat *= 1e3
        # self.ep_mat *= 1e3


    def save(self):
        pass
    
    def load(self):
        pass

if __name__ == '__main__':
    corpus_path = 'datasets/199801.txt'
    corpus = utilities.load_renmin(corpus_path)
    idxed_corpus, (obsv2idx, idx2obsv), (hide2idx, idx2hide) = utilities.index_corpus(corpus)
    builder = HmmMatBuilder(idxed_corpus, len(obsv2idx.keys()),len(hide2idx.keys()))
    builder.build()

    hmm = Hmm()
    hmm.setup(builder.sp_mat, builder.tp_mat, builder.ep_mat, len(obsv2idx.keys()),len(hide2idx.keys()))

    seq = ['19980101-01-001-002','中共中央','总书记', '、', '国家', '主席', '江', '泽民']
    idxed_seq = [obsv2idx[word] for word in seq]

    idxed_pos = hmm.find_hidden_state(idxed_seq)
    pos = [idx2hide[idx] for idx in idxed_pos]
    
    print(idxed_seq)
    print(" ".join(seq))
    print(idxed_pos)
    print(" ".join(pos))

#    19980101-01-001-002/m  中共中央/nt  总书记/n  、/w  国家/n  主席/n  江/nr  泽民/nr  