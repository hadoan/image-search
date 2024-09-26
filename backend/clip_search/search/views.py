# search/views.py
import clip
import torch
from PIL import Image
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer
import torchvision.transforms as transforms

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

class ImageSearchView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the uploaded image
        uploaded_image = request.FILES['image']
        image = preprocess(Image.open(uploaded_image))  # Open the image using Pillow

        # Preprocess the image to get a tensor
        image_tensor = transforms.ToTensor()(preprocess(image)).unsqueeze(0).to(device)

        # Generate CLIP embedding for the uploaded image
        with torch.no_grad():
            image_embedding = model.encode_image(image_tensor)

        # Move the embedding to the CPU and convert it to a NumPy array
        image_embedding = image_embedding.cpu().numpy()  # Ensure it's a NumPy array or tensor

        # Compare with stored products
        products = Product.objects.all()
        similarities = []

        for product in products:
            product_embedding = torch.tensor(product.image_embedding)
            similarity = torch.cosine_similarity(torch.tensor(image_embedding), product_embedding)
            similarities.append((similarity, product))

        # Sort products by similarity
        similarities = sorted(similarities, key=lambda x: x[0], reverse=True)
        top_product = similarities[0][1] if similarities else None

        # Return the most similar product
        serializer = ProductSerializer(top_product)
        return Response(serializer.data)
