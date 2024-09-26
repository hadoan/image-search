# search/management/commands/populate_embeddings.py
import clip
import torch
from PIL import Image
from django.core.management.base import BaseCommand
from search.models import Product
import torchvision.transforms as transforms

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

class Command(BaseCommand):
    help = 'Generate and store CLIP embeddings for product images'
    
    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        
        for product in products:
            image_path = r'D:\Working\image-search\backend\clip_search\\'  # Use raw string to handle backslashes
            pilImage =Image.open(image_path+""+product.image.name)
            # Convert RGBA to RGB if necessary
            if pilImage.mode == 'RGBA':
                pilImage = pilImage.convert('RGB')
                pilImage = pilImage.resize((2080, 2080))  # Resize to match the input dimensions if required

                print("Convert to RGB")
            if isinstance(pilImage, Image.Image):
                print("This is a valid PIL Image.")
            else:
                print(f"Expected a PIL Image, but got: {type(pilImage)}")
                
            image =transforms.ToTensor()(pilImage).unsqueeze(0).to(device)
            with torch.no_grad():
                image_embedding = model.encode_image(image)
            
            # Move the embedding to the CPU and convert it to a NumPy array
            image_embedding = image_embedding.cpu().numpy()  # Ensure it's a NumPy array or tensor
            
            product.image_embedding = image_embedding.tolist()
            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated embeddings for all products'))
