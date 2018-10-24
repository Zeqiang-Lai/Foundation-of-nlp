# coding=utf-8

def load_renmin(ds_path, encoding='gbk'):
    """ 加载人民日报-分词与词性标注数据集
    
        Returns:
          返回一个列表,列表内容为一系列词典,每个词典包含一个句子中的
          所有词语及其词性. 示例:[{'开始':'v',...},{...},...]
    """
    corpus = []
    with open(ds_path, 'r', encoding=encoding) as f:
        for line in f.readlines():
            sent = []
            for cb in line.strip().split():
                pair = cb.strip().split('/')
                sent.append((pair[0], pair[1]))
            corpus.append(sent)

    return corpus

def index_corpus(corpus):
    obsv2idx, idx2obsv = {}, {}
    hide2idx, idx2hide = {}, {}
    obsv_idx, hide_idx = 0, 0 

    # build dictionaries and indexing
    idxed_corpus = []
    for seq in corpus:
        idxed_seq = []
        for obsv, hide in seq:
            if obsv not in obsv2idx.keys():
                obsv2idx[obsv] = obsv_idx
                idx2obsv[obsv_idx] = obsv
                obsv_idx += 1
            if hide not in hide2idx.keys():
                hide2idx[hide] = hide_idx
                idx2hide[hide_idx] = hide
                hide_idx += 1
            # indexing
            idxed_seq.append((obsv2idx[obsv], hide2idx[hide]))
        idxed_corpus.append(idxed_seq)
    
    return idxed_corpus, (obsv2idx, idx2obsv), (hide2idx, idx2hide)

if __name__ == '__main__':
    corpus = load_renmin('datasets/199801.txt')
    print(corpus[:3])