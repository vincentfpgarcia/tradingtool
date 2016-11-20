import keras
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, merge
from keras.layers import Dense, Convolution1D
from keras.layers.normalization import BatchNormalization

def create_model():
	inputs = Input(shape=(1,64))
	x = inputs

	x = BatchNormalization()(x)

	x = Convolution1D(128, 3, border_mode='same')(x)
	
	x = Convolution1D(128, 5, border_mode='same')(x)
	x = Convolution1D(128, 5, border_mode='same')(x)
	x = Convolution1D(128, 5, border_mode='same')(x)
	x = Convolution1D(128, 5, border_mode='same')(x)
	x = Convolution1D(128, 5, border_mode='same')(x)

	x = Flatten()(x)
	outputs = Dense(1)(x)

	model = Model(input=inputs, output=outputs)

	return model