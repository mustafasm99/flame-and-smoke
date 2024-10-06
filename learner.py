import os
import cv2
import numpy as np
import keras
from keras import layers


last_image = None
# Function to load images from a directory


def load_images_from_folder(folder):
    global last_image
    images      = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img = cv2.resize(img , (400 , 400))
            images.append(img)
            last_image = img
        
    return np.array(images)

# cv2.imshow("last image " , last_image)

# Load positive (flame) and negative (non-flame) samples | but the classes as 0 , 1 or - , + 
flame_images        = load_images_from_folder('dataset/flame/')
non_flame_images    = load_images_from_folder('dataset/non_flame/')

# Create labels (1 for flame, 0 for non-flame) | giv each class a laberls
flame_labels        = np.ones(len(flame_images))
non_flame_labels    = np.zeros(len(non_flame_images))

# Combine flame and non-flame data
X                   = np.concatenate((flame_images, non_flame_images), axis=0) # each model take x as data
y                   = np.concatenate((flame_labels, non_flame_labels), axis=0) # y as the labels | in our case we got 0 , 1 

# Shuffle the data | create random arrays that 
permutation         = np.random.permutation(len(X))
X                   = X[permutation]
y                   = y[permutation]

# Normalize pixel values to be between 0 and 1 | gray level 
X                   = X / 255.0

# Split the data into training and testing sets | 0.8 -> 80% of the data for training and 20% for testing 
split_ratio         = 0.8
split_index         = int(split_ratio * len(X))

X_train, X_test     = X[:split_index], X[split_index:] 
y_train, y_test     = y[:split_index], y[split_index:]

# Define the CNN model
model               = keras.Sequential([
                    layers.Conv2D(32, (3, 3), activation='relu'), # grid with 20x20 input images
                    layers.MaxPooling2D((2, 2)),
                    layers.Conv2D(64, (3, 3), activation='relu'),
                    layers.MaxPooling2D((2, 2)),
                    layers.Flatten(),
                    layers.Dense(64, activation='relu'),
                    layers.Dense(1, activation='sigmoid')
                    ])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])   # push it to the processor 
# Train the modele
model.fit(X_train, y_train, epochs=3, batch_size=32, validation_split=0.2)         # Fit the model to result form 

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)                                # testing the modle on the same data that train with so we got how many accrecy we can get 
print(f'Test accuracy: {test_acc}')

# Save the model for later use
model.save('flame_smoke_detection_model.h5')                                        # save the model in file so we can use it agin in some where else 

# cv2.imshow("last image" , last_image)
# layer one Conv2D
"""
these layer to handel the images or videos as input to the model 
take the input and give you in output that fit in array like 20x20 ...
the input of all images are may not fit one image biger than the other 


Prams :: 
first is the filters - each layer take a number of filters like first one is taking 32 , second one 64  , and 128 max number 
filter is a mask on the image that will loop through all the images pixel and return a values of the target we need 
to read more go to https://pyimagesearch.com/2018/12/31/keras-conv2d-and-convolutional-layers/

second (3,3) the core | kernel_size 

The kernel_size must be an odd integer as well
f your input images are greater than 128×128 you may choose to use a kernel size > 3 to help (1) learn larger spatial filters and (2) to help reduce volume size

therd the Activation | activation='relu',

is the type of thershould we will use there is 6 types [step , sigmoid , tanh , Relu , leaky , ELU] 
each one of these are an math fanction that will fit on the data set 

"""

# MaxPooling2D 
"""
Max pooling operation for 2D spatial data.

Downsamples the input along its spatial dimensions (height and width) by taking the maximum value over an input window (of size defined by pool_size) for each channel of the input. The window is shifted by strides along each dimension.

The resulting output, when using the "valid" padding option, has a spatial shape (number of rows or columns) of: output_shape = math.floor((input_shape - pool_size) / strides) + 1 (when input_shape >= pool_size)

The resulting output shape when using the "same" padding option is: output_shape = math.floor((input_shape - 1) / strides) + 1

For example, for strides=(1, 1) and padding="valid"

for more info about these algorthem go to https://keras.io/api/layers/pooling_layers/max_pooling2d/

"""

# Flating
"""
Flatten layer that reshapes the output of the previous layer into a one-dimensional vector of size 3x3x64 = 576. This layer prepares the data for the dense layers that follow.

"""

#Dense
"""
The sixth layer is a Dense layer with 64 units and a ReLU activation function. This layer is a fully connected layer that performs a linear transformation on the input vector and applies the ReLU activation function. This layer learns the high-level features from the data and acts as a hidden layer in the model. The output shape of this layer is 64, since it has 64 units.
The seventh layer is another Dense layer with 1 unit and a sigmoid activation function. This layer is the output layer of the model that performs a binary classification on the input vector and applies the sigmoid activation function. The sigmoid function maps the input to a value between 0 and 1, which can be interpreted as the probability of the input belonging to a certain class. The output shape of this layer is 1, since it has 1 unit.
"""