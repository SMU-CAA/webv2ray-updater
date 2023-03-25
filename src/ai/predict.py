import os
import torch
from PIL import Image
from torchvision import transforms

from ai import common, one_hot


class Predict:
    def __init__(self):
        real_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(real_dir, 'model.jit.pt')
        self.trained_model = torch.jit.load(model_path, map_location=torch.device('cpu'))
        print('model loaded from {}'.format(model_path))

    def get_prediction(self, img):
        image = Image.open(img)
        image_tensor = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((140, 400)),
            transforms.ToTensor()
        ])
        image_tensor = image_tensor(image)
        image_tensor = torch.reshape(image_tensor, (-1, 1, 140, 400))
        predict_output = self.trained_model(image_tensor)
        predict_output = predict_output.view(-1, len(common.captcha_array))
        predict_output_text = one_hot.vector_to_text(predict_output)
        return predict_output_text, eval(predict_output_text[:-1])


if __name__ == '__main__':
    p = Predict()
    result = p.get_prediction('captcha.png')
    print("{}{}".format(result[0], result[1]))
