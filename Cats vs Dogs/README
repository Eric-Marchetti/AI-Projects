### Overview
What is the challenge? The challenge this project completes is training a neural network to recognize 37 breeds of cats and dogs using transfer learning.
What is the dataset? The dataset used was "The Oxford-IIIT Pet Dataset". It contains roughly 200 images of 37 breeds of cats and dogs for a total of about 7400 images. These images are much more detailed than ones used in the mnist dataset. These are 224x224x3 whereas the mnist photos were 28x28x1.
Here is a link to the dataset used: https://www.robots.ox.ac.uk/~vgg/data/pets/


### My approach
For this project, I used an existing trained network made from the imagenet dataset called VGG19. This allowed me to use a process called transfer learning to train this model. Essentially, transfer learning is using a model that is already trained and retraining the last few(typically 3) layers. The model has already trained the convolution filters so the rougly 120 million parameters it does re-train on the new dataset allows it to remap the previous 1000 outputs to output 37 different breeds of cats and dogs. This greatly speeds up the training process and allows for higher accuracy.
Here is a link to the imagenet dataset: http://www.image-net.org/


### Performance
We measure performance by looking at the accuracy. For the training data, there was 100% accuracy and for the test data, there was 81.52% accuracy. This shows that there was a lot of overfitting that occured which means that the model could have had more parameters frozen before being trained on the pet dataset.
