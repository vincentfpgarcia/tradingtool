import keras
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, merge, Activation
from keras.layers import Dense, Convolution1D
from keras.layers.normalization import BatchNormalization

def create_model():
	inputs = Input(shape=(1, 63))
	x = inputs

	# x = BatchNormalization()(x)

	branch1 = Convolution1D(128, 2, border_mode='same')(x)

	branch2 = Convolution1D(128, 7, border_mode='same')(x)

	branch3 = Convolution1D(128, 14, border_mode='same')(x)

	branch4 = Convolution1D(128, 30, border_mode='same')(x)

	branch5 = Convolution1D(128, 62, border_mode='same')(x)

	x = merge([branch1, branch2, branch3, branch4, branch5], mode='concat', concat_axis=2)

	x = Flatten()(x)
	x = Activation('relu')(x)

	x = Dense(300)(x)
	x = Dense(200)(x)
	x = Dense(100)(x)
	x = Dense(200)(x)
	x = Dense(300)(x)
	
	outputs = Dense(1)(x)

	model = Model(input=inputs, output=outputs)

	return model