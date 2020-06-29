import tensorflow as tf

tf.keras.backend.set_floatx('float64')


class Encoder(tf.keras.layers.Layer):
  def __init__(self, hidden_dim, hidden_dim_2):
    super(Encoder, self).__init__()
    self.first_hidden = tf.keras.Sequential(
      [
        tf.keras.layers.Dense(
          units=hidden_dim,
          activation=tf.nn.leaky_relu,
          kernel_initializer='he_uniform'),
        tf.keras.layers.BatchNormalization(),
      ])

    self.second_hidden = tf.keras.Sequential(
      [
        tf.keras.layers.Dense(
          units=hidden_dim_2,
          activation=tf.nn.leaky_relu,
          kernel_initializer='he_uniform'),
        tf.keras.layers.BatchNormalization(),
      ]
    )

    self.output_layer = tf.keras.layers.Dense(
      units=hidden_dim_2,
      activation=tf.nn.sigmoid
    )

  ### feedforward of Encoder
  @tf.function
  def call(self, input_x):
    activation = self.first_hidden(input_x)
    activation2 = self.second_hidden(activation)
    return self.output_layer(activation2)

  @tf.function
  def hidden(self, input_x):
    hidden_1 = self.first_hidden(input_x, training=False)
    hidden_2 = self.second_hidden(hidden_1, training=False)
    return hidden_1, hidden_2


class Decoder(tf.keras.layers.Layer):
  def __init__(self, hidden_dim, hidden_dim_2, original_dim):
    super(Decoder, self).__init__()
    self.first_hidden = tf.keras.Sequential(
      [
        tf.keras.layers.Dense(
          units=hidden_dim,
          activation=tf.nn.leaky_relu,
          kernel_initializer='he_uniform'),
        tf.keras.layers.BatchNormalization(),
      ])

    self.second_hidden = tf.keras.Sequential(
      [
        tf.keras.layers.Dense(
          units=hidden_dim_2,
          activation=tf.nn.leaky_relu,
          kernel_initializer='he_uniform'
        ),
        tf.keras.layers.BatchNormalization(),
      ]
    )

    self.output_layer = tf.keras.layers.Dense(
      units=original_dim,
      activation=tf.nn.sigmoid
    )

  ### feedforward of Decoder
  @tf.function
  def call(self, input_x):
    activation = self.first_hidden(input_x)
    activation2 = self.second_hidden(activation)
    return self.output_layer(activation2)


class Autoencoder(tf.keras.Model):
  def __init__(self, hidden_dim_1, hidden_dim_2, original_dim):
    super(Autoencoder, self).__init__()
    self.encoder = Encoder(hidden_dim=hidden_dim_1, hidden_dim_2=hidden_dim_2)
    self.decoder = Decoder(hidden_dim=hidden_dim_1, hidden_dim_2=hidden_dim_2,
                           original_dim=original_dim)

  ### feedforward of Autoencoder
  @tf.function
  def call(self, input_x):
    latent = self.encoder(input_x)
    reconstructed = self.decoder(latent)
    return reconstructed
