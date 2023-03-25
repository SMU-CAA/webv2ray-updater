import torch
from torch import nn

from ai import common


class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1,
                      out_channels=64,
                      kernel_size=3,  # kernel box size is 3x3
                      padding=1  # padding set to 0
                      ),
            nn.ReLU(),  # active layer
            nn.MaxPool2d(kernel_size=2)
        )  # [64, 64, 70, 200]
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=64,
                      out_channels=128,
                      kernel_size=3,
                      padding=1
                      ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )  # [64, 128, 35, 100]
        self.layer3 = nn.Sequential(
            nn.Conv2d(in_channels=128,
                      out_channels=256,
                      kernel_size=3,
                      padding=1
                      ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )  # [64, 256, 17, 50]
        self.layer4 = nn.Sequential(
            nn.Conv2d(in_channels=256,
                      out_channels=512,
                      kernel_size=3,
                      padding=1
                      ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )  # [64, 512, 8, 25]
        self.layer5 = nn.Sequential(
            nn.Flatten(),  # flatten the , get [64, 102400]
            nn.Linear(in_features=102400, out_features=4096),
            nn.Dropout(0.2),  # to avoid overfitting
            nn.ReLU(),  # activation
            nn.Linear(in_features=4096, out_features=common.captcha_size * common.captcha_array.__len__())
        )

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.layer5(x)
        return x


if __name__ == '__main__':
    # 64 images; gray is 1
    data = torch.ones(64, 1, 140, 400)
    mymodel = MyModel()
    x = mymodel(data)
    print(x.shape)
