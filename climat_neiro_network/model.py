import torch
import torch.nn.functional as F

class NeuralNetwork(torch.nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.weights_input_to_hidden1 = torch.nn.Linear(4, 8)
        self.weights_hidden1_to_hidden2 = torch.nn.Linear(8, 8)
        self.weights_hidden2_to_hidden3 = torch.nn.Linear(8, 8)
        self.weights_hidden3_to_output = torch.nn.Linear(8, 1)

        self.bn1 = torch.nn.BatchNorm1d(8)
        self.bn2 = torch.nn.BatchNorm1d(8)
        self.bn3 = torch.nn.BatchNorm1d(8)

        self.dropout = torch.nn.Dropout(0.2)

    def forward(self, x):
        x = self.bn1(F.relu(self.weights_input_to_hidden1(x)))
        x = self.dropout(x)
        x = self.bn2(F.relu(self.weights_hidden1_to_hidden2(x)))
        x = self.dropout(x)
        x = self.bn3(F.relu(self.weights_hidden2_to_hidden3(x)))
        x = self.dropout(x)
        x = self.weights_hidden3_to_output(x)
        return x