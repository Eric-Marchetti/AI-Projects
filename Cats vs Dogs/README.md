### Overview

The challenge this project completes is training a neural network to recognize 37 breeds of cats and dogs using transfer learning. The dataset used was "The Oxford-IIIT Pet Dataset". It contains roughly 200 images of 37 breeds of cats and dogs for a total of about 7400 images. These images are much more detailed than ones used in the mnist dataset. These are 224x224x3 whereas the mnist photos were 28x28x1.
Here is a link to the dataset used: https://www.robots.ox.ac.uk/~vgg/data/pets/


### My approach

For this project, I used an existing trained network made from the imagenet dataset called VGG19. This allowed me to use a process called transfer learning to train this model. Essentially, transfer learning is using a model that is already trained and retraining the last few layers. The model has already trained the convolution filters and they output a 25088 element vector. Instead of mapping this vector into 1000 different categories, for this challenge we map it into 37 different categories over the course of 3 layers. This greatly speeds up the training process and allows for higher accuracy.
Here is a link to the imagenet dataset: http://www.image-net.org/


### Performance
We measure performance by looking at the accuracy. For the training data, there was 100% accuracy and for the test data, there was 81.52% accuracy. This shows that there was a lot of overfitting that occured which means that the model could have had more parameters frozen before being trained on the pet dataset. Another solution would be to reduce the output of the 3rd to last layer(fc1). Currently, it has 25088 inputs and 4096 outputs which results in approximately 100 million parameters. Although this could lessen the accuracy, reducing the outputs to somewhere around 1024 or 2048 would greatly reduce the overfitting that is occuring. Another technique that could be used would be dropout which reduces the number of non-zero parameters.
