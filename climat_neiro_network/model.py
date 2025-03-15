import torch
import torch.nn.functional as F

class NeuralNetwork(torch.nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.weights_input_to_hidden1 = torch.nn.Linear(5, 20)
        self.weights_hidden1_to_hidden2 = torch.nn.Linear(20, 15)
        self.weights_hidden2_to_hidden3 = torch.nn.Linear(15, 10)
        self.weights_hidden3_to_hidden4 = torch.nn.Linear(10, 5)
        self.weights_hidden4_to_output = torch.nn.Linear(5, 1)

        self.bn1 = torch.nn.BatchNorm1d(20)
        self.bn2 = torch.nn.BatchNorm1d(15)
        self.bn3 = torch.nn.BatchNorm1d(10)
        self.bn4 = torch.nn.BatchNorm1d(5)

    def forward(self, x):
        x = self.bn1(F.relu(self.weights_input_to_hidden1(x)))
        x = self.bn2(F.relu(self.weights_hidden1_to_hidden2(x)))
        x = self.bn3(F.relu(self.weights_hidden2_to_hidden3(x)))
        x = self.bn4(F.relu(self.weights_hidden3_to_hidden4(x)))
        x = self.weights_hidden4_to_output(x)
        return x