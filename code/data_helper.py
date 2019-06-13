import jieba
from collections import Counter
import tensorflow.contrib.keras as kr
import codecs
import re
import os
import pandas
import numpy as np
import csv
import logging
import importlib,sys
importlib.reload(sys)


#
"""
文件操作类
包含数据预处理函数，以及对文件的操作函数都在里面
"""

class TextConfig():

    pre_trianing = None  # use vector_char trained by word2vec

    seq_length = 40  # max length of sentence
    # vector_word_filename = './OriginData/vector_word.txt'
    # vector_word_npz = './OriginData/vector_word.npz'



    originTrainData = './OriginData/train.tsv'
    originTestData = './OriginData/test.tsv'
    handldData = './OriginData/handledTrain.csv'
    thirdLevelCategory = False
    third_Key_Label_Value = './OriginData/third_Key_Label_Value.txt'
    trainFileCsv = './OriginData/trainData.csv'
    predict_File = './OriginData/test.tsv'
    predict_Result_File = './OriginData/predict_Result.csv'
    val_filename = './OriginData/valData.csv'
    categoryFile = './OriginData/category.txt'
    vocab_filename = './OriginData/vocab.txt'

    testFile = './OriginData/test.txt'
    # trainFileCsv = './OriginData/tempHand.csv'
    # val_filename = './OriginData/tempHand.csv'
    # categoryFile = './OriginData/categoryTemp.txt'
    # vocab_filename = './OriginData/vocabTemp.txt'
    #
    # oneHotLabel = './OriginData/oneHotLabel.txt'
    # oneHotContent = './OriginData/oneHotContent.txt'

def tempUse(contents,labels):
    with codecs.open(TextConfig.oneHotContent,'w','utf-8') as file:
        for one in contents:
            file.write(str(one)+'\n\n')

    with codecs.open(TextConfig.oneHotLabel,'w','utf-8') as file:
        for one in labels:
            file.write(str(one)+'\n')

def batch_iter(data, batch_size, num_epochs, shuffle=True):
    '''
    含有 yield 说明不是一个普通函数，是一个 Generator.
    函数效果：对 data，一共分成 num_epochs 个阶段（epoch），在每个 epoch 内，如果 shuffle=True，就将 data 重新洗牌，
    批量生成 (yield) 一批一批的重洗过的 data，每批大小是 batch_size，一共生成 int(len(data)/batch_size)+1 批。

    Args:
        data: The data
        batch_size: The size of the data batch
        num_epochs: The number of epochs
        shuffle: Shuffle or not (default: True)
    Returns:
        A batch iterator for data set
    '''
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((data_size - 1) / batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


def Get_Content_Label(fileName):
    '''
    获得文件的两列数据，内容以及标签
    '''
    dataset = pandas.read_csv(fileName,names=['ITEM_NAME','TYPE'],low_memory=False)
    array = dataset.values
    items_Content = array[1:,0:1]
    items_Label = array[1:,1]
    Content = []
    label = []
    for Index in items_Content:
        Content.append(str(Index[0]).split(' '))
    # for Index in items_Label:
    #     label.extend(str(Index).split('    '))
    return Content,items_Label
    # return items_Content, items_Label

def Build_Dict_Third_Key_To_Label_Value():
    '''
    构造一个key：第三级标题，value：label的字典
    :return: 返回该字典
    '''
    with codecs.open(TextConfig.third_Key_Label_Value,'r','utf-8') as file:
        data = file.read().splitlines()
        key = []
        value = []
        for one in data:
            key_Value = one.split('    ')
            assert (len(key_Value)==2)
            key.append(key_Value[0])
            value.append(key_Value[1])

    return dict(zip(key,value))


def Get_Val_Data_From_TrainData():
    '''
    因为给的数据只有训练集和测试集，所以需要从训练集中分出部·分数据作为验证集
    '''

    content,labels = Get_Content_Label(TextConfig.handldData)
    index = []
    with codecs.open(TextConfig.val_filename,'w','utf_8_sig') as file:
        write = csv.writer(file)
        write.writerow(['ITEM_NAME','TYPE'])
        tempLabel = labels[0]
        start = 0
        end = 0
        oneLabelCount = 0
        for oneLabel in labels:
            if(oneLabel != tempLabel):
                getCount = int(oneLabelCount*0.1)
                getCount = 1 if getCount < 1 else getCount
                for i in range(start,start+getCount):
                    write.writerow([' '.join(ClearUselessWord(str(content[i]))),str(labels[i])])
                    index.append(i)
                tempLabel = oneLabel
                oneLabelCount = 0
                start = end+1
                end = start
            else:
                end += 1
                oneLabelCount += 1
        print('val完成')

    with codecs.open(TextConfig.trainFileCsv,'w','utf_8_sig') as file:
        write = csv.writer(file)
        write.writerow(['ITEM_NAME', 'TYPE'])
        for i in range(0,len(labels)):
            if i in index:
                continue
            else:
                write.writerow([' '.join(ClearUselessWord(str(content[i]))),str(labels[i])])

def test(lines):
    '''
    临时测试函数
    '''
    with codecs.open(TextConfig.testFile, 'w', 'utf-8') as file:
        for line in lines:
            file.write(str(line)+'\n')


def Get_Save_CategoryFromOriginData():
    '''

    :param thirdLevelCategory:True:将三级分类全部写入文件;False:只写入第三级分类
    :return:
    '''

    allLabel = []
    wholeLabel = []
    content,label = Get_Content_Label(TextConfig.handldData)
    for index in label:
        index = index.split('    ')
        assert (len(index) == 3)
        if (TextConfig.thirdLevelCategory):
            for oneLabel in index:
                if (oneLabel not in allLabel):
                    allLabel.append(oneLabel)
        else:
            if (index[2] not in allLabel):
                allLabel.append(index[2])
                wholeLabel.append('--'.join(index))

    with codecs.open(TextConfig.categoryFile,'w+','utf-8') as file:
        for oneLabel in allLabel:
            file.write(str(oneLabel)+'\n')

    if(TextConfig.thirdLevelCategory == False):
        with codecs.open(TextConfig.third_Key_Label_Value, 'w', 'utf-8') as file:
            assert (len(allLabel) == len(wholeLabel))
            for index in range(len(allLabel)):
                file.write(allLabel[index] + '    ' + wholeLabel[index] + '\n')


def Get_Categories():
    '''
    获得全部分类
    :return:
    '''
    with codecs.open(TextConfig.categoryFile,'r','utf-8') as file:
        categories = file.read().splitlines()
        category_to_id = dict(zip(categories,range(len(categories))))
        return categories,category_to_id

def CollectionCategory(count,level):
    with codecs.open('./OriginData/temp.txt', 'w', 'utf-8') as file:
        counter = Counter(count)
        for one in counter:
            space = ''
            i = level[one]
            if(i==1):
                space = '  '
            if(i==2):
                space = '    '
            file.write(space+str(one)+':'+str(counter.get(one)) + '\n')


def OutPutPredictResult(data,result,fileName,mode='a+',coding='utf-8'):
    '''

    :param data:预测原始数据
    :param result: 预测结果
    :param fileName: 保存文件名
    :param mode: 写入方式，覆盖还是在文件末追加
    :return:
    '''
    with codecs.open(fileName,mode,coding) as file:
        write = csv.writer(file)
        for content,Label in zip(data,result):
            write.writerow([content,Label])

def WriteToOriginFile_PredictResult(data,result,fileName,mode='a+',coding='utf_8_sig'):
    '''
    将预测结果写入源文件另外一列
    :param result:
    :param fileName:
    :return:
    '''
    assert (len(result) == len(data))
    label = []
    with codecs.open(fileName,mode,coding) as file:
        write = csv.writer(file)
        for index in range(len(data)):
            temp = []
            line = data[index].split('\t')
            if(len(line) != 2):
                line = data[index].split(',')
                tempLine = line[0]
                for i in range(1,len(line)-1):
                    tempLine += ','+line[i]
                temp.append(tempLine)
                temp.append(line[len(line)-1])
                label.append(line[len(line)-1])
            else:
                temp.append(str(line[0]))
                temp.append(str(line[1]))
                label.append(line[1])
            temp.append(result[index])
            write.writerow([temp[0],temp[1],temp[2]])

    return Find_Same_From_Train_Predict(label,result)

def get_File_All_Lines(fileName,coding='utf-8'):
    with codecs.open(fileName,'r',coding) as file:
        lines = file.read().splitlines()
        return lines


def handFileProblem():
    '''
    原始数据有部分有问题，用这个函数处理掉
    :return:
    '''
    lines = []
    with codecs.open('./OriginData/word.txt','r','utf-8') as file:
        lines = file.read().splitlines()

    #写入处理后的文件
    # with codecs.open('./OriginData/handledTrain.csv','a+','utf-8') as file:
    #     write = csv.writer(file)
    #     for line in lines:
    #         line = line.split('\t')
    #         assert (len(line)==2)
    #         content = ClearUselessWord(line[0])
    #         tags = line[1].split("--")
    #         assert (len(tags) == 3)
    #         write.writerow([(' '.join(content)),('    '.join(tags))])

    #写入处理前的文件
    with codecs.open('./OriginData/train.tsv','a+','gb18030') as file:
        write = csv.writer(file)
        for line in lines:
            line = line.split('\t')
            assert (len(line)==2)
            write.writerow([line[0],line[1]])



def build_vocab(filenames, vocab_dir, vocab_size=160000):

    """
    构造词汇表
    Args:
        filename:trian_filename,test_filename,val_filename
        vocab_dir:path of vocab_filename
        vocab_size:number of vocabulary
    Returns:
        writting vocab to vocab_filename

    """
    Get_Save_CategoryFromOriginData()
    all_data = []
    for filename in filenames:
        data,_ = Get_Content_Label(filename)
        for one in data:
            all_data.extend(one)
    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    words = ['<PAD>'] + list(words)

    with codecs.open(vocab_dir, 'w', encoding='utf-8') as f:
        f.write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):
    """
    读取词汇表
    Args:
        filename:path of vocab_filename
    Returns:
        words: a list of vocab
        word_to_id: a dict of word to id

    """
    words = codecs.open(vocab_dir, 'r', encoding='utf-8').read().strip().split('\n')
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id

def process_file(filename,word_to_id,cat_to_id,numClass,max_length=600):
    """
    Args:
        filename:train_filename or test_filename or val_filename
        word_to_id:get from def read_vocab()
        cat_to_id:get from def read_category()
        max_length:allow max length of sentence
    Returns:
        x_pad: sequence data from  preprocessing sentence
        y_pad: sequence data from preprocessing label

    """
    contents,labels=Get_Content_Label(filename)
    data_id,label_id=[],[]
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label =  labels[i].split('    ')
        if(len(label)!=3):
            continue
        oneId = [0]*numClass
        if(TextConfig.thirdLevelCategory):
            for oneLable in label:
                oneId[cat_to_id[oneLable]] = 1
            label_id.append(oneId)
        else:
            oneId[cat_to_id[label[2]]] = 1
            label_id.append(oneId)
        #label_id.append(cat_to_id[labels[i].split(' ')[0]])
    x_pad=kr.preprocessing.sequence.pad_sequences(data_id,max_length,padding='post', truncating='post')
    y_pad=kr.utils.to_categorical(label_id)
    return x_pad,label_id

def predict_sentence(sentence,word_to_id,max_length=600):
    content = ClearUselessWord(sentence)
    if(len(content)<1):
        return []
    data_id = []
    data_id.append([word_to_id[x] for x in content if x in word_to_id])
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length, padding='post', truncating='post')
    return data_id



def predict_file(fileName,word_to_id,max_length=600,coding='utf-8'):
    '''
    将预测文件中每行句子处理成适合程序处理的形式
    '''


    with codecs.open(fileName,'r',coding) as file:
        lines = file.read().splitlines()
        drop_out_lines = []
        content = []
        datas_id = []
        i = 0
        for line in lines:
            id = predict_sentence(line,word_to_id,max_length)
            if(len(id) != 0):
                datas_id.extend(id)
                content.append(line)
            else:
                drop_out_lines.append(i)

            i += 1

        return content,kr.preprocessing.sequence.pad_sequences(datas_id, max_length, padding='post', truncating='post')


def HandleOriginData(inputFileName,outputFileName):
    '''
    处理原始数据
    存入新文件中
    主要是将内容处理并且分词，将标签分割开
    '''
    with codecs.open(inputFileName,'r',encoding='gb18030', errors='ignore') as file:
        count = []
        level = {}

        reader = csv.reader(file)
        next(reader)
        with codecs.open(outputFileName,"w",'utf_8_sig') as writeFile:
            write = csv.writer(writeFile)
            write.writerow(['ITEM_NAME','TYPE'])
            for row in reader:
                rowContent = (row[0]).split("\t")
                if(len(rowContent)<2):
                    # line = jieba.lcut(ClearUselessWord(rowContent[0]))
                    # write.writerow([(" ".join(line))])
                    continue
                else:
                    originLine = rowContent[0]
                    originTags = rowContent[1]
                    # line = jieba.lcut(ClearUselessWord(originLine))
                    line = ClearUselessWord(originLine)
                    tags = originTags.split("--")
                    for i in range(len(tags)):
                        level[tags[i]] = i
                    count.extend(tags)

                    write.writerow([(' '.join(line)),('    '.join(tags))])

        CollectionCategory(count,level)




def ClearUselessWord(line):
    """
        1. 将除汉字外的字符转为一个空格
        2. 将连续的多个空格转为一个空格
        3. 除去句子前后的空格字符
        """
    # line = re.sub(r'[^\u4e00-\u9fffQ]', ' ', line)
    # line = re.sub(r'\s{2,}', ' ', line)
    # return line.strip()
    words = jieba.lcut(line)
    result = []
    for one in words:
        temp = re.match(r'^[a-zA-Z]{2,}$', one)
        if temp:
            result.append(one)
        else:
            temp = re.match(r'[\u4e00-\u9fff]+', one)
            if temp:
                result.append(one)
    return result


def Get_Id_To_Cat():
    categories,id = Get_Categories()
    id_To_Cat = dict(zip(range(len(categories)), categories))
    return id_To_Cat

def Get_F_Acc(inputFile,AccOutFile,FOutPut):
    '''
    从日志文件获取Acc和F值
    :param inputFile:
    :param AccOutFile:
    :param FOutPut:
    :return:
    '''
    F = []
    Acc = []
    with codecs.open(inputFile,'r','utf-8') as File:
        lines = File.read().splitlines()
        for line in lines:
            if('threshold' in line):
                temp = line.split(' ')
                Acc.append((re.search(r'[0-9].[0-9]+',temp[12])).group())
                F.append((re.search(r'[0-9].[0-9]+',temp[14])).group())

    with codecs.open(AccOutFile,'w','utf-8') as File:
        for index in Acc:
            File.write(str(index)+'\n')

    with codecs.open(FOutPut,'w','utf-8') as File:
        for index in F:
            File.write(str(index)+'\n')

def logger_fn(name, input_file, level=logging.INFO):
    tf_logger = logging.getLogger(name)
    tf_logger.setLevel(level)
    log_dir = os.path.dirname(input_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    fh = logging.FileHandler(input_file, mode='w',encoding = 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    tf_logger.addHandler(fh)
    return tf_logger



def cal_metric(predicted_labels, labels):
    """
    Calculate the metric(recall, accuracy, F, etc.).

    Args:
        predicted_labels: The predicted_labels
        labels: The true labels
    Returns:
        The value of metric
    """
    label_no_zero = []
    for index, label in enumerate(labels):
        if int(label) == 1:
            label_no_zero.append(index)
    count = 0
    for predicted_label in predicted_labels:
        if int(predicted_label) in label_no_zero:
            count += 1
    rec = count / len(label_no_zero)
    acc = count / len(predicted_labels)
    if (rec + acc) == 0:
        F = 0.0
    else:
        F = (2 * rec * acc) / (rec + acc)
    return rec, acc, F


def get_label_using_scores_by_threshold(scores, threshold=0.5):
    """
    Get the predicted labels based on the threshold.
    If there is no predict value greater than threshold, then choose the label which has the max predict value.

    Args:
        scores: The all classes predicted scores provided by network
        threshold: The threshold (default: 0.5)
    Returns:
        predicted_labels: The predicted labels
        predicted_values: The predicted values
    """
    predicted_labels = []
    predicted_values = []
    scores = np.ndarray.tolist(scores)
    for score in scores:
        count = 0
        index_list = []
        value_list = []
        for index, predict_value in enumerate(score):
            if predict_value > threshold:
                index_list.append(index)
                value_list.append(predict_value)
                count += 1
        if count == 0:
            index_list.append(score.index(max(score)))
            value_list.append(max(score))
        predicted_labels.append(index_list)
        predicted_values.append(value_list)
    return predicted_labels, predicted_values


def get_label_using_scores_by_topk(scores, top_num=1):
    """
    Get the predicted labels based on the topK number.

    Args:
        scores: The all classes predicted scores provided by network
        top_num: The max topK number (default: 5)
    Returns:
        The predicted labels
    """
    predicted_labels = []
    predicted_values = []
    scores = np.ndarray.tolist(scores)
    for score in scores:
        value_list = []
        index_list = np.argsort(score)[-top_num:]
        index_list = index_list[::-1]
        for index in index_list:
            value_list.append(score[index])
        predicted_labels.append(np.ndarray.tolist(index_list))
        predicted_values.append(value_list)
    return predicted_labels, predicted_values

def Find_Same_From_Train_Predict(origin,predict):
    '''

    :param origin:
    :param predict:
    :return:
    '''
    assert (len(origin) == len(predict))
    correct = 0

    for Index in range(len(origin)):
        if(origin[Index] == predict[Index]):
            correct += 1

    return correct,len(origin)



if __name__ == '__main__':

    #HandleOriginData(TextConfig.originTrainData,TextConfig.handldData)
    Get_Val_Data_From_TrainData()
    fileNames = [TextConfig.trainFileCsv,TextConfig.val_filename]
    build_vocab(fileNames,TextConfig.vocab_filename)
    #Get_Save_CategoryFromOriginData()
    print("data_helper完成")



