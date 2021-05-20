import pandas as pd
import numpy as np
from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes

#Need to find out actual number of classes from data set
def extract_labels(Data, one_hot=False, num_classes=2):
    #labels can be numpy array
    labels=[]
    if one_hot:
      return dense_to_one_hot(labels, num_classes)
    pass

#Extract feature values and replace any non numerical feature value with numerical value here
def extract_features(Data):
    pass

def data_importer(one_hot=False,
                   dtype=dtypes.float32,
                   validation_size=5000):
    TEST_SET = pd.read_csv('data/UNSW_NB15_testing-set.csv')
    TRAIN_SET = pd.read_csv('data/UNSW_NB15_training-set.csv')
    dtype = dtypes.float32
    df = pd.DataFrame(np.random.randn(len(TRAIN_SET), 2))
    mask = np.random.rand(len(df)) < 0.8

    ACTUAL_TRAIN_SET = TRAIN_SET[mask]
    VALIDATION_SET = TRAIN_SET[~mask]

    train_samples = extract_features(ACTUAL_TRAIN_SET)
    train_labels = extract_labels(ACTUAL_TRAIN_SET, one_hot=one_hot)

    test_samples = extract_features(TEST_SET)
    test_labels = extract_labels(TEST_SET, one_hot=one_hot)

    validation_samples = extract_features(VALIDATION_SET)
    validation_labels = extract_labels(VALIDATION_SET, one_hot=one_hot)

    train = DataSet(train_samples, train_labels, dtype=dtype)
    validation = DataSet(validation_samples,
                         validation_labels,
                         dtype=dtype)
    test = DataSet(test_samples, test_labels, dtype=dtype)

    return base.Datasets(train=train, validation=validation, test=test)

def dense_to_one_hot(labels_dense, num_classes):
  """Convert class labels from scalars to one-hot vectors."""
  num_labels = labels_dense.shape[0]
  index_offset = np.arange(num_labels) * num_classes
  labels_one_hot = np.zeros((num_labels, num_classes))
  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
  return labels_one_hot

class DataSet(object):

  def __init__(self,
               samples,
               labels,
               one_hot=False,
               dtype=dtypes.float32):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true.  `dtype` can be either
    `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
    `[0, 1]`.
    """
    dtype = dtypes.as_dtype(dtype).base_dtype
    if dtype not in (dtypes.uint8, dtypes.float32):
      raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                      dtype)

    assert samples.shape[0] == labels.shape[0], (
          'samples.shape: %s labels.shape: %s' % (samples.shape, labels.shape))
    self._num_examples = samples.shape[0]


    if dtype == dtypes.float32:
        # Convert from [0, 255] -> [0.0, 1.0].
        samples = samples.astype(np.float32)
        samples = np.multiply(samples, 1.0 / 255.0)
    self._samples = samples
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def samples(self):
    return self._samples

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def next_batch(self, batch_size):
    """Return the next `batch_size` examples from this data set."""
    start = self._index_in_epoch
    self._index_in_epoch += batch_size
    if self._index_in_epoch > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1
      # Shuffle the data
      perm = np.arange(self._num_examples)
      np.random.shuffle(perm)
      self._samples = self._samples[perm]
      self._labels = self._labels[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size
      assert batch_size <= self._num_examples
    end = self._index_in_epoch
    return self._samples[start:end], self._labels[start:end]