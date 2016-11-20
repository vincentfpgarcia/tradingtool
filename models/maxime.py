import keras
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, merge, Activation
from keras.layers import Dense, Convolution1D
from keras.layers.normalization import BatchNormalization

def create_model():
	inputs = Input(shape=(1,63))
	x = inputs

	x = BatchNormalization()(x)

	branch = Convolution1D(128, 3, border_mode='same')(x)
	branch = Activation('relu')(branch)
	x = merge([x, branch], mode='concat', concat_axis=2)

	branch = Convolution1D(128, 5, border_mode='same')(x)
	branch = Activation('relu')(branch)
	x = merge([x, branch], mode='concat', concat_axis=2)

	branch = Convolution1D(128, 7, border_mode='same')(x)
	branch = Activation('relu')(branch)
	x = merge([x, branch], mode='concat', concat_axis=2)


	x = Flatten()(x)
	outputs = Dense(1)(x)

	model = Model(input=inputs, output=outputs)

	return model