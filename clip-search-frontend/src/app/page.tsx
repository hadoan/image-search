"use client";

import { useState, ChangeEvent } from 'react';

interface Product {
  name: string;
  image: string;
}

export default function Home() {
  const [image, setImage] = useState<File | null>(null);
  const [result, setResult] = useState<Product | null>(null);

  const handleImageUpload = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setImage(e.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append('image', image);

    try {
      const res = await fetch('http://localhost:8000/api/search/', {
        method: 'POST',
        body: formData,
      });

      const data: Product = await res.json();
      setResult(data);
    } catch (error) {
      console.error('Error during image search:', error);
    }
  };

  return (
    <div>
      <h1>Product Search by Image</h1>
      <input type="file" onChange={handleImageUpload} />
      <button onClick={handleSubmit}>Search</button>

      {result && (
        <div>
          <h2>Result:</h2>
          <p>{result.name}</p>
          <img src={`http://localhost:8000${result.image}`} alt={result.name} width="200" />
        </div>
      )}
    </div>
  );
}
