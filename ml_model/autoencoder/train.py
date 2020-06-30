from model import *


### MSE loss
@tf.function
def loss(model, original_data, training=True):
  if training:
    reconstruction_error = tf.reduce_mean(
      tf.square(tf.subtract(model(original_data), original_data)), axis=-1)
  else:
    reconstruction_error = tf.reduce_mean(
      tf.square(
        tf.subtract(model(original_data, training=False), original_data)),
      axis=-1)
  return reconstruction_error


### Gradients taping
@tf.function
def train(loss_metric, model, opt, original_data):
  with tf.GradientTape() as tape:
    gradients = tape.gradient(loss_metric(model, original_data),
                              model.trainable_variables)
    gradient_variables = zip(gradients, model.trainable_variables)
    opt.apply_gradients(gradient_variables)
