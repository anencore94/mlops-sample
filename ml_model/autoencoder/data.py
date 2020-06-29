import tensorflow as tf
import pandas as pd
import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


def is_binary(x):
  return set(x.astype(str)) <= set('01')


### data should have "label" column

def read_data(name, scale=True):
  os.chdir(os.path.dirname(__file__) + '/datasets')
  data = pd.read_csv(name + '.csv')
  features = list(data.columns)
  if 'label' in features:
    features.remove('label')
    label = data['label']
    data.pop('label')

  ### Standardization
  if scale:
    scale = []
    for i in range(len(features)):
      x = features[i]
      if 'int' == data[x].dtypes:
        if is_binary(data[x]) == False:
          scale.append(i)
        data[x] = data[x].astype(float)
      elif 'float' == data[x].dtypes:
        scale.append(i)
    standardization = ColumnTransformer(
      transformers=[("standardization", StandardScaler(), scale)])
    st_data = standardization.fit_transform(data.values)
    st_data = pd.DataFrame(st_data)
    not_scale = [x for x in range(len(features)) if x not in scale]
    data = st_data.join(data.iloc[:, not_scale])
  return data, label


def split_data(data, label):
  ### split data into train_set and test_set
  ### train_set - only normal
  ### test_set - abnormal and normal ( 1:2 ration sampling from normal)
  total_data = data.join(label)
  total_data = total_data.join(
    pd.DataFrame(total_data.index, columns=['index']))
  normal_count = label.value_counts()[0]
  abnormal_count = label.value_counts()[1]
  normal = total_data.loc[total_data['label'] == 0]
  abnormal = total_data.loc[total_data['label'] == 1]
  test_df = normal.sample(int(abnormal_count * 0.1)).append(
    abnormal.sample(1000))
  normal_df = normal.drop(test_df.index, errors="ignore")
  return normal_df.reset_index(drop=True), test_df.reset_index(drop=True)


def tf_data(dataframe, shuffle=True, index=True, batch_size=256):
  ### convert data into tf_data
  dataframe = dataframe.copy()
  label = dataframe.pop('label')
  if index:
    index = dataframe.pop('index')
    tf_dataset = tf.data.Dataset.from_tensor_slices(
      (dataframe.values, label.values, index))
  else:
    dataframe.pop('index')
    tf_dataset = tf.data.Dataset.from_tensor_slices(
      (dataframe.values, label.values))
  if shuffle:
    tf_dataset = tf_dataset.shuffle(buffer_size=len(dataframe))
  tf_dataset = tf_dataset.batch(batch_size)
  return tf_dataset
