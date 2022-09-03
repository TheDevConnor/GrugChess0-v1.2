import numpy as np

# class NeuralNetwork:
layer_1 = np.array([ # The first layer of the neural network
    [1.5, -0.5],       # There are two nerons being registered here 1 and -0.5
    [-1,   1],       # While we have 4 weights here as well, two for each neron
    [-1,   1]        # The nerons go straight down, so neron 1 is 1, -1, -1 while neron 2 is -0.5, 1, 1
])

layer_2 = np.array([ # The secound layer of the neural network
    [-1],            # There is only one neron here
    [1],            # And only two weights
    [1]             # The neron goes straight down, so neron 1 is -1, 1, 1
])

def step(x):         # The activation function
    return np.where(x>0, 1, 0) 
    # We are returning the numpy array, and that everything inside of the array
    # is greater than 0, then return 1, otherwise return 0

def neural_network(inputs, layers, activation_func): # The neural network function
    outputs = inputs # We are setting the output to the inputs because it is pretty much the output of the last layer

    for layer in layers: # Now we are iterating through the layers
        inputs = np.hstack([np.ones(shape=(outputs.shape[0], 1)), outputs])
        # We are adding a 1 to the front of the bias
        # We do this by generating a new np array with only 1s inside of it
        # The array that is being generated is a 2d array and has 1 col andthe same amount of rows as the output
        outputs = activation_func(np.matmul(inputs, layer))
        # We are multiplying the input and the layer together
        # Then we are passing the output into the activation function

    # Then we run it again for the second layer
    return outputs

inputs = [
    [0, 0],
    [1, 0],
    [0, 1],
    [1, 1]
]

# Now we iterate over all the possible inputs
for i in inputs:
    print(i, "->", neural_network(
        inputs=np.array([i]), # We are passing in the inputs
        layers=[layer_1, layer_2], # We are passing in the layers
        activation_func=step # We are passing in the activation function
    ))

print("\nAll the inputs at once:")
print(neural_network(
    inputs=np.array(inputs), # We are passing in the inputs
    layers=[layer_1, layer_2], # We are passing in the layers
    activation_func=step # We are passing in the activation function
))