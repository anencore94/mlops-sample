import argparse
import time

import numpy as np
from sklearn import metrics

from data_preprocess import *
from train import *


def run(hyperparameters):
  name = 'experiment_pvi'
  data, label = read_data(name)
  n_anomaly = [x for x in label if x == 1]
  train_set, test_set = split_data(data, label)
  print('number of data : {}, number of Anomaly: {}'.
        format(len(data), len(n_anomaly)))
  print('number of train_set : {}, number of test_set : {}, shape : {}'.
        format(train_set.shape[0],
               test_set.shape[0], test_set.shape[1]))
  tf_train = tf_data(train_set)
  tf_test = tf_data(test_set)

  ### Hyperparameters for the model
  original_dim = train_set.shape[1] - 2
  ### Hyperparameters for the model
  first_hidden_dim = int(hyperparameters['first_hidden_dim'])
  second_hidden_dim = int(hyperparameters['second_hidden_dim'])
  epoch = int(hyperparameters['epoch'])
  learning_rate = float(hyperparameters['learning_rate'])

  autoencoder = Autoencoder(hidden_dim_1=first_hidden_dim,
                            hidden_dim_2=second_hidden_dim,
                            original_dim=original_dim)
  optimizer = tf.optimizers.Adam(learning_rate=learning_rate)

  ### Training
  train_loss = tf.keras.metrics.Mean()
  for epoch in range(1, epoch + 1):
    start_time = time.time()
    train_loss.reset_states()
    for train_x, label, index in tf_train:
      train(loss, autoencoder, optimizer, train_x)
      train_loss.update_state(loss(autoencoder, train_x))
    end_time = time.time()
    print('Epoch : {}, train_loss : {}, time_elapse : {}'.format(
      epoch, train_loss.result(), end_time - start_time))

    ### Test
    normal_recon = []
    abnormal_recon = []
    normal_recon_ix = []
    abnormal_recon_ix = []

    for test_x, label, index in tf_test:
      recon = loss(autoencoder, test_x, training=False)
      true_label = []
      scores = []
      for i in range(len(label)):
        true_label.append(label[i])
        scores.append(recon[i])
        ### record the index of test_set
        if label[i] == 0:
          normal_recon.append(recon[i])
          normal_recon_ix.append(index[i])
        elif label[i] == 1:
          abnormal_recon.append(recon[i])
          abnormal_recon_ix.append(index[i])
    fprs, tpr, _ = metrics.roc_curve(np.array(true_label), np.array(scores),
                                     pos_label=1)
    print(
      'Epoch : {}, Normal_recon : {}, Normal_std : {}, Abnormal_recon : {},'
      ' Abnormal_std : {}'.format(
        epoch, np.mean(normal_recon), np.std(normal_recon),
        np.mean(abnormal_recon), np.std(abnormal_recon)))

    # ### record the index of missclassified data
    normal_high_ix = []
    abnormal_low_ix = []

  print('Accuracy of Normal : {}, Accuracy of Abnormal : {}'.format(
    (len(normal_recon_ix) - len(normal_high_ix)) / len(normal_recon_ix),
    (len(abnormal_recon_ix) - len(abnormal_low_ix)) / len(abnormal_recon_ix)))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  # TODO pod env 에서 str 말고 int 랑 float 으로 받을 수 있는 방법
  parser.add_argument('--learning_rate', type=str, default='0.005')
  parser.add_argument('--epoch', type=str, default='20')
  parser.add_argument('--first_hidden_dim', type=str, default='20')
  parser.add_argument('--second_hidden_dim', type=str, default='10')

  args = parser.parse_args()

  dict_formatted_args = vars(args)

  run(dict_formatted_args)
