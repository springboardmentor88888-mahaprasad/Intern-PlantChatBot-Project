import torch
from torchvision import transforms
from PIL import Image
import json

def predict_image(image_path, model, class_names):
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor()
    ])
    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0)

    model.eval()
    with torch.no_grad():
        outputs = model(img)
        _, pred = torch.max(outputs, 1)

    return class_names[pred.item()]

def predict_symptom(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    pred = torch.argmax(outputs.logits, dim=1)
    return pred.item()
