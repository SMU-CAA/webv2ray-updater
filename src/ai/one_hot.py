import torch

from ai import common


def text_to_vector(text):
    # column 4, row 14
    vector = torch.zeros(common.captcha_size, len(common.captcha_array))
    for i in range(len(text)):
        vector[i, common.captcha_array.index(text[i])] = 1
    return vector


def vector_to_text(vector):
    vector = torch.argmax(vector, dim=1)
    text = ""
    for i in vector:
        text += common.captcha_array[i]
    return text


if __name__ == '__main__':
    vec = text_to_vector("1+1=")
    print("{}\n{}".format(vec, vec.shape))
    print("flattened: {}".format(vec.view(1, -1)[0].shape))
    print("the fomula is: {}".format(vector_to_text(vec)))
