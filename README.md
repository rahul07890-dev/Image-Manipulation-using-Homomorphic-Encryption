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
  git clone https://github.com/rahul07890-dev/Image-Manipulation-using-Homomorphic-Encryption.git
  cd Image-Manipulation-using-Homomorphic-Encryption

2.## Install dependencies:
   pip install -r requirements.txt

3.## Configure AWS S3 credentials:

Set up AWS CLI and provide credentials for accessing the S3 bucket.
Ensure the bucket name and object keys in the code match your S3 setup.

4.## Run the application:
   python app.py


