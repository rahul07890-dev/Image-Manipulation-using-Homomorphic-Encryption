# Image Manipulation Using Homomorphic Encryption

## Overview
This Flask-based web application demonstrates how to perform brightness and contrast adjustments on encrypted images using **homomorphic encryption**. The application uses **TenSEAL** for encryption, **NumPy** and **OpenCV** for image manipulation, and **AWS S3** for securely storing and retrieving encrypted data. Users can upload an image, apply operations directly on the encrypted data, and view the processed image without compromising data privacy.

---

## Features
- **Encrypted Image Upload**: Upload an image and preprocess it for encryption.
- **Privacy-Preserving Operations**: Perform brightness and contrast adjustments directly on encrypted data.
- **Secure Storage**: Store and retrieve encrypted images securely using AWS S3.
- **Decryption and Download**: Decrypt and download the processed image for local use.
- **Homomorphic Encryption**: Ensures data privacy throughout all operations.

---

## Technologies Used
- **Flask**: For building the web application.
- **TenSEAL**: For implementing homomorphic encryption.
- **AWS S3**: For encrypted image storage and retrieval.
- **NumPy** and **OpenCV**: For image processing and manipulation.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rahul07890-dev/Image-Manipulation-using-Homomorphic-Encryption.git
   cd Image-Manipulation-using-Homomorphic-Encryption
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS S3 Credentials**:
   - Set up AWS CLI and provide credentials for accessing the S3 bucket.
   - Ensure the bucket name and object keys in the code match your S3 setup.

4. **Run the Application**:
   ```bash
   python app.py
   ```

---

## Directory Structure
```
Image-Manipulation-using-Homomorphic-Encryption/
|
├── app.py               # Main Flask application
├── encryption/          # Encryption and decryption utilities
├── static/              # Static files (CSS, JS, etc.)
├── templates/           # HTML templates
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Future Enhancements
- **Additional Image Operations**: Support for more advanced manipulations (e.g., filtering, transformations).
- **Performance Optimization**: Enhance efficiency of encryption and processing.
- **Cloud Integration**: Add support for other cloud storage services (e.g., Google Cloud Storage, Azure).
- **Enhanced UI**: Improve the frontend interface for better user experience.

---

## Contribution
Contributions are welcome! Feel free to fork this repository, create a branch, and submit a pull request with your improvements or new features.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
- **TenSEAL Documentation**: For guidance on implementing homomorphic encryption.
- **AWS Documentation**: For resources on secure file storage.
- **Open-Source Community**: For inspiration and tools to build innovative applications.

