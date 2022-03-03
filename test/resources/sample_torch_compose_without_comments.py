import torch
from torchvision import transforms

train_transforms = transforms.Compose(
    [
        transforms.CenterCrop(10),
        transforms.PILToTensor(), 
        
        transforms.RandomResizedCrop(SIZE, scale=(0.08, 1.0)),
        
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

test_transforms = transforms.Compose(
    [
        transforms.CenterCrop(10),
        transforms.PILToTensor(),
        transforms.ConvertImageDtype(torch.float),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ]
)
