from dataloader import DataLoader, filebrowser
from interface import Interface

if __name__ == '__main__':
    dataloader = DataLoader(filebrowser(), output_dir='annotations')
    interface = Interface(dataloader)