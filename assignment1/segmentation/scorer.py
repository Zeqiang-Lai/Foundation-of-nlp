# coding=utf-8

from mm_seg import MMSeg

def precision(pred, std):
    """ 求分词结果的正确率

        Args:
          pred: 分词结果,一个元组,其内容为各个句子的分词结果(仍为元组).
          std: 标准分词结果,结构与pred相同.
        
        Returns:
          返回正确率,取值[0,1].
    """
    correct = 0
    total_num = 0

    for p_s, std_s in zip(pred, std):
        for word in p_s:
            if(word in std_s):
                correct += 1
        total_num += len(p_s)
    
    return float(correct) / total_num

def recall(pred, std):
    """ 求分词结果的召回率

        Args:
          pred: 分词结果,一个元组,其内容为各个句子的分词结果(仍为元组).
          std: 标准分词结果,结构与pred相同.
        
        Returns:
          返回召回率,取值[0,1].
    """
    correct = 0
    total_num = 0

    for p_s, std_s in zip(pred, std):
        for word in p_s:
            if(word in std_s):
                correct += 1
        total_num += len(std_s)
    
    return float(correct) / total_num

def f1_score(pred, std):
    """ 求分词结果的f1值

        Args:
          pred: 分词结果,一个元组,其内容为各个句子的分词结果(仍为元组).
          std: 标准分词结果,结构与pred相同.
        
        Returns:
          返回f1值,取值[0,1].
    """
    prec = precision(pred, std)
    rec = recall(pred, std)

    return 2.0 * prec * rec / (prec + rec)

def sanity_check():
    # TODO: 检查上面三个函数的正确性 
    pass
 
if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--test_path', default='datasets/shanxi/train.txt')
    # parser.add_argument('--gold_path', default='dicts/shanxi_dict.json')
    # parser.add_argument('--encoding', default='utf-16')
    # args = parser.parse_args()

    mmseg = MMSeg("dicts/pku_dict.json", 'utf-16')

    pred = []
    with open("datasets/icwb2-data/testing/pku_test.utf8", "r", encoding='utf-8') as f:
        for sent in f.readlines():
            pred.append(mmseg.cut(sent))

    std = []
    with open("datasets/icwb2-data/gold/pku_test_gold.utf8", "r", encoding='utf-8') as f:
        for sent in f.readlines():
            std.append(sent.strip().split())

    # 保存分词结果
    with open("pku_pred.txt", "w", encoding='gb2312') as f:
        for words in pred:
            s = " ".join(words)
            s.encode('gb2312',errors='ignore')
            f.write(s)

    print("Precision: {0}.".format(precision(pred, std)))
    print("Recall: {0}.".format(recall(pred, std)))
    print("F1 Score: {0}.".format(f1_score(pred, std)))