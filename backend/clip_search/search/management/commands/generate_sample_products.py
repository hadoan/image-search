# search/management/commands/generate_sample_products.py
import os
import json
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from search.models import Product
from PIL import Image
import io

class Command(BaseCommand):
    help = 'Generate sample products'

    def generate_image(self, name):
        """Generate a simple placeholder image."""
        img = Image.new('RGB', (200, 200), color=(73, 109, 137))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return ContentFile(img_bytes.read(), name=f'{name}.png')

    def generate_embedding(self):
        """Generate a random embedding."""
        return [0.1, 0.2, 0.3]  # Example embedding (replace with actual embeddings as needed)

    def handle(self, *args, **kwargs):
        sample_products = [
            {
                'name': 'Sample Product 1',
                'image': self.generate_image('Sample_Product_1'),
                'image_embedding': json.dumps(self.generate_embedding())
            },
            {
                'name': 'Sample Product 2',
                'image': self.generate_image('Sample_Product_2'),
                'image_embedding': json.dumps(self.generate_embedding())
            },
            {
                'name': 'Sample Product 3',
                'image': self.generate_image('Sample_Product_3'),
                'image_embedding': json.dumps(self.generate_embedding())
            },
        ]

        for product_data in sample_products:
            product = Product(
                name=product_data['name'],
                image=product_data['image'],
                image_embedding=product_data['image_embedding']
            )
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.name}'))
