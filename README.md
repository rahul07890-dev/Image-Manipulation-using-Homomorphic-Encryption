# Image Manipulation Using Homomorphic Encryption

## Overview
This Flask-based web application demonstrates how to perform brightness and contrast adjustments on encrypted images using **homomorphic encryption**. The application uses **TenSEAL** for encryption, **NumPy** and **OpenCV** for image manipulation, and **AWS S3** for securely storing and retrieving encrypted data. Users can upload an image, apply operations directly on the encrypted data, and view the processed image without compromising data privacy.

---

## Features
- Upload an image and preprocess it for encryption.
- Perform brightness and contrast adjustments directly on encrypted data.
- Securely store and retrieve encrypted images in AWS S3.
- Decrypt and download the processed image for local use.
- All operations maintain data privacy using **homomorphic encryption**.

---

## Technologies Used
- **Flask**: For building the web application.
- **TenSEAL**: For implementing homomorphic encryption.
- **AWS S3**: For encrypted image storage.
- **NumPy** and **OpenCV**: For image processing and manipulation.

---

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/image-manipulation-encryption.git
   cd image-manipulation-encryption
