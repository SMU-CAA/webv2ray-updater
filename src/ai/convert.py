import torch


def convert():
    m = torch.load('model.pt', map_location=torch.device('cpu'))
    jm = torch.jit.script(m)
    torch.jit.save(jm, 'model.jit.pt')
    print('ok')


if __name__ == '__main__':
    convert()
