# -*- coding:utf-8 -*-

import os
import sys
import time
import tensorflow as tf
import data_helper as DH
import math
"""
提供对模型的预测
"""
# Parameters
# ==================================================

#DH.Get_Save_CategoryFromOriginData()
categories,cat_to_id = DH.Get_Categories()
id_to_cat = DH.Get_Id_To_Cat()
words,word_to_id = DH.read_vocab(DH.TextConfig.vocab_filename)
vocab_size = len(words)

num_classes = len(categories)

pad_seq_len = DH.TextConfig.seq_length



logger = DH.logger_fn('tflog', 'logs/predict-{0}.log'.format(time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))))

# Data Parameters

tf.flags.DEFINE_string("predict_data_file", DH.TextConfig.predict_File, "Data source for the test data")
tf.flags.DEFINE_string("checkpoint_dir", "./runs/checkpoints", "Checkpoint directory from training run")
# tf.flags.DEFINE_string("vocab_data_file", "./", "Vocabulary file")

# Model Hyperparameters
# tf.flags.DEFINE_integer("pad_seq_len", 100, "Recommended padding Sequence length of data (depends on the data)")
tf.flags.DEFINE_integer("embedding_dim", 128, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_integer("embedding_type", 1, "The embedding type (default: 1)")
tf.flags.DEFINE_integer("fc_hidden_size", 1024, "Hidden size for fully connected layer (default: 1024)")
tf.flags.DEFINE_string("filter_sizes", "3,4,5", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")
tf.flags.DEFINE_integer("num_classes", num_classes, "Number of labels (depends on the task)")
tf.flags.DEFINE_integer("top_num", 1, "Number of top K prediction classes (default: 5)")
tf.flags.DEFINE_float("threshold", 0.5, "Threshold for prediction classes (default: 0.5)")

# Test Parameters
tf.flags.DEFINE_integer("batch_size", 128, "Batch Size (default: 64)")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
tf.flags.DEFINE_boolean("gpu_options_allow_growth", False, "Allow gpu options growth")

FLAGS = tf.flags.FLAGS
FLAGS.flag_values_dict()
para_key_values = FLAGS.__flags

logger = DH.logger_fn('tflog', 'logs/predict-{0}.log'.format( time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) ))
logger.info("input parameter:")
parameter_info = " ".join(["\nparameter: {0} value: {1}".format(key, val) for key, val in para_key_values.items()])
logger.info(parameter_info)


print("load train and val data sets.....")
logger.info('✔︎ Test data processing...')
# x_train, y_train = DH.process_file(FLAGS.training_data_file)
# x_val, y_val = DH.process_file(FLAGS.validation_data_file)
# x_test, y_test = DH.process_file(FLAGS.test_data_file)
#
# # 得到所有数据中最长文本长度
# pad_seq_len = DH.get_pad_seq_len(x_train, x_val, x_test)
#
# # 将数据pad为统一长度，同时对label进行0，1编码

originData,x_predict = DH.predict_file(FLAGS.predict_data_file,word_to_id,DH.TextConfig.seq_length,'gb18030')
# x_predict, _ = DH.process_file(DH.TextConfig.handldData,word_to_id, cat_to_id,num_classes,DH.TextConfig.seq_length)
# originData = DH.get_File_All_Lines(DH.TextConfig.originTrainData,'gb18030')
# originData = originData[1:]

print('数据处理完毕')


def predict(originContent,predicts):
    """Predict Use TextCNN model."""

    # Load cnn model
    logger.info("✔ Loading model... ")
    checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
    logger.info(checkpoint_file)

    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)
        session_conf.gpu_options.allow_growth = FLAGS.gpu_options_allow_growth
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{0}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            scores = graph.get_operation_by_name("output/scores").outputs[0]
            feed_dict = {
                input_x: predicts,
                dropout_keep_prob: 1.0,
            }
            batch_scores = sess.run(scores, feed_dict)
            predicted_labels_threshold, predicted_values_threshold = \
                DH.get_label_using_scores_by_threshold(scores=batch_scores, threshold=FLAGS.threshold)

            # print(predicted_labels_threshold, predicted_values_threshold)
            all_threshold = []
            for _ in predicted_labels_threshold:
                temp = []
                for id in _:
                    temp.append(id_to_cat[int(id)])
                all_threshold.append(temp)
            #print(all_threshold)

            # Predict by topK
            all_topK = []
            predicted_labels_topk, predicted_values_topk = \
                DH.get_label_using_scores_by_topk(batch_scores, top_num=FLAGS.top_num)
            for _ in predicted_labels_topk:
                temp = []
                for id in _:
                    temp.append(id_to_cat[int(id)])
                all_topK.append(temp)

            all_top = []
            if(DH.TextConfig.thirdLevelCategory == False):
                dictLabel = DH.Build_Dict_Third_Key_To_Label_Value()
                for one in all_topK:
                    label = dictLabel[one[0]]
                    all_top.append(label)
            else:
                all_top = all_topK
            print('预测完成，输出结果中')

            DH.OutPutPredictResult(originContent,all_top,DH.TextConfig.predict_Result_File)
            #return DH.WriteToOriginFile_PredictResult(originContent, all_top, './OriginData/train.csv')
            logger.info('文件写入完毕')
            #return all_top
    logger.info("✔ Done.")
    #临时语句


if __name__ == '__main__':

    acc = 0
    ori = 0
    pre = 0

    span = 50000
    length = len(x_predict)
    spanCount = math.ceil(length/span)
    start = 0
    end = span
    for i in range(span):
        if(end>length):
            end = length
            #predict(originData[start:end],x_predict[start:end])
            # pre,ori = predict(originData[start:end], x_predict[start:end])
            # acc += pre
            break
        predict(originData[start:end], x_predict[start:end])
        # pre, ori = predict(originData[start:end],x_predict[start:end])
        # logger.info('源数据' + str(ori) + '个' + '  正确' + str(pre) + '个' + '\n')
        # acc += pre
        logger.info(str(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))) + '第' + str(i) + '趟' + '\n')

        start = end
        end += span

    # logger.info('总共' + str(len(originData)) + '个' + '  正确' + str(acc) + '个' + '\n')


