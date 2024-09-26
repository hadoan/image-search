import clip
import torch

# Fetch and print available models
available_models = clip.available_models()
print("Available CLIP Models:")
for model in available_models:
    print(model)

print( torch.cuda.is_available())

print("Torch version:", torch.__version__)
print("CLIP version:", clip.__spec__)
