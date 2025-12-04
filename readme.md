# PixelExplore – AI-Powered Visual Discovery Platform

PixelExplore is an AI-powered Pinterest-style gallery platform that allows users to upload and explore images with automatically generated, detailed descriptions. The platform supports both **text-based** and **image-based search**, leveraging modern computer vision and NLP techniques for intelligent image discovery.

## Features

### AI-Powered Image Descriptions

* Uploaded images are processed with **BLIP/CLIP** to generate initial captions.
* Captions are enhanced by **Google Gemini LLM** to produce detailed, human-readable descriptions.
* Descriptions are vectorized using **All-MiniLMv6** and stored in a **FAISS vector database** for fast similarity search.

### Dual Search Functionality

* **Text-based search:** User input is vectorized → similarity search in FAISS → top image results displayed.
* **Image-based search:** Uploaded image processed → description generated → vectorized → similarity search → top results displayed.

### Modern Web Interface

* Responsive gallery interface built with **React** and **Tailwind CSS**.
* Interactive image upload, browsing, and search experience.

### Scalable Backend

* **FastAPI** backend handles image uploads, processing, vector embedding, and retrieval.
* **FAISS vector database** ensures efficient storage and retrieval of embeddings.

## Tech Stack

* **AI & NLP:** BLIP/CLIP, Google Gemini, All-MiniLMv6, FAISS
* **Backend:** Python, FastAPI
* **Frontend:** React, Tailwind CSS
* **Database:** FAISS vector store

## How It Works

1. **Image Upload:** Users upload an image to the platform.
2. **Description Generation:**

   * Initial caption generated with BLIP/CLIP.
   * Gemini LLM refines the caption for detailed description.
3. **Vectorization:** The description is converted into embeddings using All-MiniLMv6.
4. **Storage:** Embeddings are stored in FAISS vector database.
5. **Search:**

   * **Text-based:** Input text is vectorized → similarity search → top results.
   * **Image-based:** Input image → description → vector → similarity search → top results.

## Installation

### Prerequisites

* Python 3.8+
* Node.js 16+

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Usage

1. Upload images to the gallery.
2. Explore images using text queries or by uploading another image.
3. View AI-generated descriptions and top search results.

## Future Enhancements

* Support for multiple image formats and batch uploads.
* Personalized recommendation system based on user interactions.
* Advanced filtering options (tags, categories, colors).

## License

MIT License

---

