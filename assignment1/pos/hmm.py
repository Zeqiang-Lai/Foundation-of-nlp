# coding=utf-8

import numpy as np

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
        
        for i in range(self.num_hide):
            f[0][i] = self.sp_mat[i] * self.ep_mat[obsv_seq[i]][0]
            f_arg[0][i] = 0

        # 动态规划求解
        for i in range(1, len_seq):
            for j in range(self.num_hide):
                fs = [f[i-1][k] * self.tp_mat[k][j] * self.ep_mat[j][obsv_seq[i]] 
                               for k in range(self.num_hide)]
                f[i][j] = max(fs)
                f_arg[i][j] = np.argmax(fs)
        
        # 反向求解最好的隐藏序列
        hidden_seq = [0] * len_seq
        z = np.argmax(f[len_seq-1][self.num_hide-1])
        hidden_seq[len_seq-1] = z
        for i in reversed(range(1, len_seq)):
            z = f_arg[i][z]
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
        self.total_count = __count_pair()

    def __count_pair():
        """ 统计(观察值,隐藏值)对的总数.
        """
        count = 0
        for seq in self.corpus:
            count += len(seq)
        return count

    def build(self):
        """ 构建初始概率矩阵,转移概率矩阵以及发射概率矩阵.
        """
        self.sp_mat = np.zeros(self.num_hide)
        self.tp_mat = np.zeros([self.num_hide, self.num_hide])
        self.ep_mat = np.zeros([self.num_hide, self.num_obsv])

        for seq in self.corpus:
            for i in range(len(seq)):
                obsv_cur, hide_cur = seq[i]
                
                if(i == 1):
                    self.sp_mat[hide_cur] += 1
                else:
                    obsv_pre, hide_pre = seq[i-1]
                    self.tp_mat[hide_pre][hide_cur] += 1
                
                self.ep_mat[hide_cur][obsv_cur] += 1

        self.sp_mat /= self.total_count
        self.tp_mat /= self.total_count
        self.ep_mat /= self.total_count 

    def save(self):
        pass
    
    def load(self):
        pass

if __name__ == '__main__':
    num_hide = 2
    num_obsv = 3

    sp_mat = np.array([0.6, 0.4])
    tp_mat = np.array([[0.7, 0.3],
                       [0.4, 0.6]])
    ep_mat = np.array([[0.5, 0.4, 0.1],
                       [0.1, 0.3, 0.6]]) 
    
    hmm = Hmm()
    hmm.setup(sp_mat, tp_mat, ep_mat, num_obsv, num_hide)

    obsv_seq = [0,1,0]
    hidden_seq = hmm.find_hidden_state(obsv_seq)

    print(hidden_seq)