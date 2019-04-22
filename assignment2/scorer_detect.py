import kenlm
from model.proofreader import CNProofReader

def precision(answer_list, truth_list, total):
    '''求查找错误的正确率
    '''
    correct = 0
    total_num = total
    for i in range(len(answer_list)):
        try:
            if answer_list[i][0] == '0':
                continue
            else:
                for answer in answer_list[i]:
                    if answer in truth_list[i]:
                        correct += 1  
        except:
            print(answer_list[i])
    return float(correct) / total_num 

def recall(answer_list, truth_list):
    '''求查找错误的召回率
    '''
    correct = 0
    total_num = 0

    for i in range(len(answer_list)):
        if truth_list[i][0] == '0':
            continue
        else:
            total_num += len(truth_list[i])

    for i in range(1000):
        if answer_list[i][0] == '0':
            continue
        else:
            for answer in answer_list[i]:
                if answer in truth_list[i]:
                    correct += 1

    return float(correct) / total_num

def f1_score(answer_list, truth_list, total):
    '''求查找错误的f1值
    '''
    prec = precision(answer_list, truth_list, total)
    rec = recall(answer_list, truth_list)

    return 2.0 * prec * rec / (prec + rec)

if __name__ == '__main__':
    pf = CNProofReader()
    
    test_list = []
    with open('./test/Task1_simple.txt', 'r', encoding = 'utf-8') as f1:
        all_lines = f1.readlines()
        for line in all_lines:
            test_list.append(line[11:])

    truth_list = []
    with open('./test/Task1_Truth_simple.txt', 'r', encoding = 'utf-8') as f2:
        all_lines = f2.readlines()
        for line in all_lines:
            truth_list.append(line[6:].strip('\n').split(', '))

    answers = []

    for sent in test_list:
        answers.append(pf.proofread(sent))
        
    total = 0
    answer_list = []
    for answer in answers:
        temp_list = []
        if answer == []:
            temp_list.append('0')
            answer_list.append(temp_list)
            continue
        for temp_tuple in answer:
            total += 1
            temp1, temp2 = temp_tuple[0][1],temp_tuple[0][2]
            for i in range(temp1 + 1, temp2 + 1):
                temp_list.append(str(i))
        answer_list.append(temp_list)

    print("Precision: {0}.".format(precision(answer_list, truth_list, total)))
    print("Recall: {0}.".format(recall(answer_list, truth_list)))
    print("F1 Score: {0}.".format(f1_score(answer_list, truth_list, total)))