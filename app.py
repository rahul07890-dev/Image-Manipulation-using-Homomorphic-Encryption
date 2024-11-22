from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
import cv2
import numpy as np
import boto3
import tenseal as ts
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management
UPLOAD_FOLDER = './ResImages'  # Folder for uploaded images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

S3_BUCKET_NAME = 'rahulkm'
S3_KEY = 'encrypted_image.npy'  # S3 object key for the encrypted image

# Initialize TenSEAL context for encryption
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
context.global_scale = 2**40
context.generate_galois_keys()

# AWS S3 Configuration
def upload_to_s3(image_bytes, bucket_name, object_key):
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=image_bytes, Bucket=bucket_name, Key=object_key)
    print(f"Encrypted image uploaded to S3 bucket: {bucket_name}/{object_key}")

def download_from_s3(bucket_name, object_key):
    s3_client = boto3.client('s3')
    img_byte_array = BytesIO()
    s3_client.download_fileobj(bucket_name, object_key, img_byte_array)
    img_byte_array.seek(0)
    return img_byte_array.getvalue()

# Preprocess the image (normalize)
def preprocess_image(image):
    image = image.astype(np.float32) / 255.0  # Normalize to [0, 1]
    return image

# Encrypt the image using TenSEAL
def encrypt_image(image, context):
    encrypted_channels = []
    for channel in cv2.split(image):  # Split into B, G, R channels
        flat_channel = channel.flatten().tolist()
        encrypted_channel = ts.ckks_vector(context, flat_channel)
        encrypted_channels.append(encrypted_channel)
    return encrypted_channels

# Decrypt the image
def decrypt_image(encrypted_channels, original_shape):
    decrypted_channels = []
    for encrypted_channel in encrypted_channels:
        decrypted_channel = np.array(encrypted_channel.decrypt())
        decrypted_channel = np.clip(decrypted_channel, 0, 1)  # Clip to valid range
        decrypted_channels.append(decrypted_channel.reshape(original_shape[:2]))
    return cv2.merge(decrypted_channels)  # Merge B, G, R channels back together

# Adjust brightness of encrypted image
def adjust_brightness_encrypted(encrypted_channels, factor):
    return [channel + factor for channel in encrypted_channels]

# Adjust contrast of encrypted image
def adjust_contrast_encrypted(encrypted_channels, factor):
    return [channel * factor for channel in encrypted_channels]

# Serialize encrypted vectors
def serialize_encrypted_image(encrypted_channels):
    serialized_data = []
    for encrypted_channel in encrypted_channels:
        serialized_data.append(np.array(encrypted_channel.decrypt()))  # Decrypt to get the underlying data
    return np.array(serialized_data)

# Deserialize encrypted vectors (reconstruct encrypted CKKS vectors)
def deserialize_encrypted_image(serialized_data, context):
    encrypted_channels = []
    for channel_data in serialized_data:
        encrypted_channel = ts.ckks_vector(context, channel_data.tolist())  # Reconstruct CKKSVector
        encrypted_channels.append(encrypted_channel)
    return encrypted_channels

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        if file and allowed_file(file.filename):
            # Read the image into memory directly from the uploaded file
            in_memory_image = np.asarray(bytearray(file.read()), dtype=np.uint8)
            image = cv2.imdecode(in_memory_image, cv2.IMREAD_COLOR)

            # Preprocess the image
            image = preprocess_image(image)

            # Store the shape of the image in the session
            session['image_shape'] = image.shape

            # Encrypt the image
            encrypted_channels = encrypt_image(image, context)

            # Serialize the encrypted image
            serialized_data = serialize_encrypted_image(encrypted_channels)

            # Save serialized data to BytesIO
            encrypted_bytes = BytesIO()
            np.save(encrypted_bytes, serialized_data)
            encrypted_bytes.seek(0)

            # Upload encrypted data to S3
            upload_to_s3(encrypted_bytes, S3_BUCKET_NAME, S3_KEY)

            return redirect(url_for('process_image'))

    return render_template('index.html')



@app.route('/process', methods=['GET', 'POST'])
def process_image():
    image_shape = session.get('image_shape', None)

    if image_shape is None:
        return redirect(url_for('index'))  # Redirect to home if shape is not found

    if request.method == 'POST':
        # Download encrypted image from S3
        encrypted_image_data = download_from_s3(S3_BUCKET_NAME, S3_KEY)
        serialized_data = np.load(BytesIO(encrypted_image_data), allow_pickle=True)

        # Reconstruct encrypted image
        encrypted_image = deserialize_encrypted_image(serialized_data, context)

        # Apply brightness/contrast adjustments
        brightness_factor = float(request.form['brightness'])
        contrast_factor = float(request.form['contrast'])

        encrypted_brightened_channels = adjust_brightness_encrypted(encrypted_image, brightness_factor)
        encrypted_contrasted_channels = adjust_contrast_encrypted(encrypted_brightened_channels, contrast_factor)

        # Decrypt the image
        decrypted_image = decrypt_image(encrypted_contrasted_channels, image_shape)

        # Save the decrypted image
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted_image.jpg')
        decrypted_image = (decrypted_image * 255.0).astype(np.uint8)
        cv2.imwrite(output_path, decrypted_image)

        # Upload the decrypted image to S3
        upload_to_s3(output_path, S3_BUCKET_NAME, 'decrypted_image.jpg')

        return send_from_directory(app.config['UPLOAD_FOLDER'], 'decrypted_image.jpg')

    return render_template('process.html')


# Utility function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']

if __name__ == '__main__':
    app.run(debug=True)
