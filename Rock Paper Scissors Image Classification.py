# -*- coding: utf-8 -*-
"""Final Project: Image Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FG1sjCd9aGSJ-0Ck8XxL6CFvml-0qPJe

# Proyek Akhir: Klasifikasi Gambar

---

### Dicoding Submission
### Belajar Machine Learning untuk Pemula

---

Kriteria submission:
- Dataset yang dipakai haruslah dataset berikut : [rockpaperscissors](https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip), atau gunakan link ini pada `wget` command: https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip.
- Dataset harus **dibagi** menjadi **`train set`** dan **`validation set`**.
- Ukuran `validation set` harus **40%** dari total dataset (`data training` memiliki 1314 sampel, dan `data validasi` sebanyak 874 sampel).
- Harus mengimplementasikan **augmentasi gambar**.
- Menggunakan **`ImageDataGenerator`**.
- Model harus menggunakan **model sequential**.
- Pelatihan model tidak melebihi **waktu 30 menit**.
- Program dikerjakan pada **`Google Colaboratory`**.
- **Akurasi** dari model minimal **85%**.
- Dapat **memprediksi gambar** yang diunggah ke Colab seperti gambar di bawah.
![](https://d17ivq9b7rppb3.cloudfront.net/original/academy/202004302318257ec23b834046174a7d426680e488905e.png)
- Manambahkan **data diri** (sesuai profil Dicoding) pada **submission/project** yang dikirimkan.

---

Saran dan Tips:
- Akurasi dari model di atas 85%
- Anda menggunakan lebih dari 1 hidden layer.
- Menerapkan lebih banyak augmentasi gambar.
- Anda menggunakan optimizer dan loss-function yang tidak diajarkan di kelas.
- Model merupakan klasifikasi multi kelas sehingga `loss function` yang digunakan **bukan** `binary_crossentropy`.

---

- **Bintang 3** : Semua ketentuan terpenuhi namun hanya mengikuti seperti apa yang ada pada modul.
- **Bintang 4** : Semua ketentuan terpenuhi dan akurasi dari program di atas 95%.
- **Bintang 5** : Semua ketentuan terpenuhi, akurasi di atas 96%, dan menggunakan tiga atau lebih teknik yang tidak diajarkan di modul seperti penggunaan Callback.

---

# Data Diri

Nama: Andrew Benedictus Jamesie  
E-mail: andrewbjamesie@yahoo.com  

---
---
"""

# Download rockpaperscissors dataset
!wget --no-check-certificate \
  https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip \
  -O /tmp/rockpaperscissors.zip

# Extract files
import zipfile, os

local_zip = '/tmp/rockpaperscissors.zip'
zip_ref   = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

base_dir         = '/tmp/rockpaperscissors/rps-cv-images'
base_dir_r       = os.path.join(base_dir, 'rock')
base_dir_p       = os.path.join(base_dir, 'paper')
base_dir_s       = os.path.join(base_dir, 'scissors')

# Split train set (60%) and validation set (40%)
!pip install split-folders
import splitfolders as sf

sf.ratio(
    base_dir,
    output = os.path.join('/tmp/rockpaperscissors/image'),
    seed   = None,
    ratio  = (0.6, 0.4)
)

# Set train and validation directory for each rock, paper, scissors
image_dir = '/tmp/rockpaperscissors/image'

train_dir_r      = os.path.join(image_dir, 'train/rock')
train_dir_p      = os.path.join(image_dir, 'train/paper')
train_dir_s      = os.path.join(image_dir, 'train/scissors')

validation_dir_r = os.path.join(image_dir, 'val/rock')
validation_dir_p = os.path.join(image_dir, 'val/paper')
validation_dir_s = os.path.join(image_dir, 'val/scissors')

# Count the number of train and validation images
train_set = (
      len(os.listdir(train_dir_r))
    + len(os.listdir(train_dir_p))
    + len(os.listdir(train_dir_s))
)

validation_set = (
      len(os.listdir(validation_dir_r))
    + len(os.listdir(validation_dir_p))
    + len(os.listdir(validation_dir_s))
)

print(f'Train Set      : {train_set}')
print(f'Validation Set : {validation_set}')

train_dir      = os.path.join(image_dir, 'train')
validation_dir = os.path.join(image_dir, 'val')

print(os.listdir(train_dir))
print(os.listdir(validation_dir))

!rm -rf /tmp/rockpaperscissors/rps-cv-images/.ipynb_checkpoints

# Image Augmentation for duplicating image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale          = 1./255,
    rotation_range   = 20,
    horizontal_flip  = True,
    shear_range      = 0.2,
    fill_mode        = 'nearest'
)

test_datagen = ImageDataGenerator(
    rescale          = 1./255
)

# Prepare the training and validation data with .flow_from_directory()
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size = (80, 120),
    batch_size  = 32,
    class_mode  = 'categorical',
    shuffle     = True
)

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size = (80, 120),
    batch_size  = 32,
    class_mode  = 'categorical',
    shuffle     = True
)

# Build the model with Convolutional Neural Network (CNN) and MaxPooling
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32,  (3, 3), activation='relu', input_shape=(80, 120, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64,  (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(512, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

# Compile the model with 'categorical_crossentropy' loss function and Adam optimimzer
model.compile(
    loss      = 'categorical_crossentropy',
    optimizer = tf.optimizers.Adam(),
    metrics   = ['accuracy']
)

# Commented out IPython magic to ensure Python compatibility.
# Create TensorBoard
# %load_ext tensorboard
import datetime, os
logdir = os.path.join('/content/sample_data', datetime.datetime.now().strftime('%YYYY%mm%dd-%HH%MM%SS'))
tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)

# Train the model with model.fit()
history = model.fit(
    train_generator,
    steps_per_epoch  = 25,
    epochs           = 20,
    validation_data  = validation_generator,
    validation_steps = 5,
    verbose          = 2,
    callbacks        = [tensorboard_callback]
)

# Visualize accuracy and loss plot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

accuracy     = history.history['accuracy']
val_accuracy = history.history['val_accuracy']

loss         = history.history['loss']
val_loss     = history.history['val_loss']

epoch        = 20
epoch_range  = range(epoch)

plt.figure(figsize = (12, 4))
plt.subplot(1, 2, 1)
plt.plot(epoch_range, accuracy,     label='Training Accuracy')
plt.plot(epoch_range, val_accuracy, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

plt.subplot(1, 2, 2)
plt.plot(epoch_range, loss,     label='Training Loss')
plt.plot(epoch_range, val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')

plt.show()

# Commented out IPython magic to ensure Python compatibility.
# Predicting Image
import numpy as np
from google.colab import files
from tensorflow.keras.preprocessing import image
# %matplotlib inline

uploaded = files.upload()

for fn in uploaded.keys():
    path = fn
    img  = image.load_img(path, target_size = (80, 120))

    imgplot = plt.imshow(img)
    x       = image.img_to_array(img)
    x       = np.expand_dims(x, axis = 0)
    images  = np.vstack([x])

    classes = model.predict(images, batch_size = 10)
    output  = np.argmax(classes)
    print(fn)

    if output == 0:
        print('Paper')
    elif output == 1:
        print('Rock')
    else:
        print('Scissors')

"""---


References:

[(Python Documentation) ZipFile](https://docs.python.org/3/library/zipfile.html)

[(Medium) flow_from_direcotry](https://vijayabhaskar96.medium.com/tutorial-image-classification-with-keras-flow-from-directory-and-generators-95f75ebe5720)

[(Tutorials Point) Keras Dropout Layers](https://www.tutorialspoint.com/keras/keras_dropout_layers.htm)

[(Keras) Layer Activation Functions](https://keras.io/api/layers/activations)

[(Dicoding) Error Saat Melakukan Pelatihan Model](https://www.dicoding.com/academies/184/discussions/182005)

[(PyImageSearch) ImageNet: VGGNet, ResNet, Inception, and Xception with Keras](https://pyimagesearch.com/2017/03/20/imagenet-vggnet-resnet-inception-xception-keras)
"""