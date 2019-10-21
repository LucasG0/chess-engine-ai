import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',category=FutureWarning)
    import numpy as np
    from keras.models import Input
    from keras.models import Model
    from keras.layers import Dense
    from keras.layers import Convolution2D
    from keras.layers import MaxPooling2D
    from keras.layers import Flatten
    from keras.layers import BatchNormalization
    from keras.layers import Activation
    from keras.optimizers import SGD
    from keras import regularizers



# Convolutional Neural Network.
# Input : Game congifuration encoded.
# Output : Policy on possibles moves + Value of the configuration.
def build_model():
    chess_input = Input(shape = (8,8,25), name = "chess_input")
    out_1 = conv_layer(chess_input)
    out_2 = conv_layer(out_1)
    out_3 = conv_layer(out_2)
    policy = policy_layer(out_3)
    value = value_layer(out_3)
    model = Model(inputs=[chess_input], outputs=[value,policy])
    model.compile(loss={'value': 'mean_squared_error', 'policy' : 'categorical_crossentropy'}, optimizer=SGD())
    return model

def conv_layer(input_layer):
    conv = Convolution2D(128, (3, 3), kernel_regularizer=regularizers.l2(0.01))(input_layer)
    batch_norm = BatchNormalization()(conv)
    output = Activation('relu')(batch_norm)
    return output

def policy_layer(input_layer):
    conv = Convolution2D(2, (1, 1))(input_layer)
    batch_norm = BatchNormalization()(conv)
    output = Activation('relu')(batch_norm)
    flatten = Flatten()(output)
    policy = Dense(4032,activation='softmax',name='policy', kernel_regularizer=regularizers.l2(0.01))(flatten)
    return policy

def value_layer(input_layer):
    conv = Convolution2D(1, (1, 1))(input_layer)
    batch_norm = BatchNormalization()(conv)
    output_1 = Activation('relu')(batch_norm)
    flatten = Flatten()(output_1)
    full = Dense(256)(flatten)
    output_2 = Activation('relu')(full)
    value = Dense(1,activation='tanh',name='value', kernel_regularizer=regularizers.l2(0.01))(output_2)
    return value

# Residual blocks are used in the original paper of alpha zero.
# def residual(input_layer):
#     conv_1 = Convolution2D(128, 3, 3, input_shape = (8,8,25))(chess_input)
#     batch_norm_1 = BatchNormalization()(conv_1)
#     output_1 = Activation('relu')(batch_norm_1)
#     conv_2 = Convolution2D(128, 3, 3, input_shape = (8,8,25))(output_1)
#     batch_norm_2 = BatchNormalization()(conv_2)
#     input_12 = [input_layer,batch_norm_2]
#     output_2 = Activation('relu')(input_12)
#     return output_2
