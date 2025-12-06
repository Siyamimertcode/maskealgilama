#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maske Algılama Modeli Eğitim Script
Bu script, maske takılan ve takılmayan yüz görüntülerinden model eğitir.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D, Dropout, Flatten, Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import argparse


def load_dataset(dataset_path, img_size=(224, 224)):
    """
    Veri setini yükler.
    
    Args:
        dataset_path: Veri seti klasör yolu
        img_size: Görüntü boyutu
    
    Returns:
        data: Görüntü dizisi
        labels: Etiket dizisi
    """
    print("[BİLGİ] Veri seti yükleniyor...")
    
    data = []
    labels = []
    
    # 'with_mask' ve 'without_mask' klasörlerini kontrol et
    categories = ['with_mask', 'without_mask']
    
    for category in categories:
        category_path = os.path.join(dataset_path, category)
        if not os.path.exists(category_path):
            print(f"[UYARI] Klasör bulunamadı: {category_path}")
            continue
        
        for img_name in os.listdir(category_path):
            img_path = os.path.join(category_path, img_name)
            
            try:
                image = load_img(img_path, target_size=img_size)
                image = img_to_array(image)
                image = preprocess_input(image)
                
                data.append(image)
                labels.append(category)
            except Exception as e:
                print(f"[HATA] Görüntü yüklenemedi {img_path}: {e}")
    
    print(f"[BİLGİ] Toplam {len(data)} görüntü yüklendi")
    
    return np.array(data), np.array(labels)


def create_model(input_shape=(224, 224, 3)):
    """
    MobileNetV2 tabanlı transfer öğrenme modeli oluşturur.
    
    Args:
        input_shape: Giriş görüntü boyutu
    
    Returns:
        model: Oluşturulan model
    """
    print("[BİLGİ] Model oluşturuluyor...")
    
    # MobileNetV2 base model
    baseModel = MobileNetV2(weights="imagenet", include_top=False,
                           input_tensor=Input(shape=input_shape))
    
    # Head model
    headModel = baseModel.output
    headModel = AveragePooling2D(pool_size=(7, 7))(headModel)
    headModel = Flatten(name="flatten")(headModel)
    headModel = Dense(128, activation="relu")(headModel)
    headModel = Dropout(0.5)(headModel)
    headModel = Dense(2, activation="softmax")(headModel)
    
    # Final model
    model = Model(inputs=baseModel.input, outputs=headModel)
    
    # Base model katmanlarını dondur
    for layer in baseModel.layers:
        layer.trainable = False
    
    print("[BİLGİ] Model başarıyla oluşturuldu")
    return model


def train_model(dataset_path, output_model_path="mask_detector.model",
               epochs=20, batch_size=32, learning_rate=1e-4):
    """
    Modeli eğitir.
    
    Args:
        dataset_path: Veri seti yolu
        output_model_path: Çıktı model yolu
        epochs: Epoch sayısı
        batch_size: Batch boyutu
        learning_rate: Öğrenme oranı
    """
    # Veri setini yükle
    data, labels = load_dataset(dataset_path)
    
    if len(data) == 0:
        print("[HATA] Veri seti boş! Eğitim yapılamıyor.")
        return
    
    # Label encoding
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels)
    labels = to_categorical(labels)
    
    # Train/test split
    (trainX, testX, trainY, testY) = train_test_split(data, labels,
                                                       test_size=0.20,
                                                       stratify=labels,
                                                       random_state=42)
    
    # Data augmentation
    aug = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    
    # Model oluştur
    model = create_model()
    
    # Model derleme
    print("[BİLGİ] Model derleniyor...")
    opt = Adam(learning_rate=learning_rate)
    model.compile(loss="binary_crossentropy", optimizer=opt,
                 metrics=["accuracy"])
    
    # Model eğitimi
    print("[BİLGİ] Model eğitimi başlıyor...")
    H = model.fit(
        aug.flow(trainX, trainY, batch_size=batch_size),
        steps_per_epoch=len(trainX) // batch_size,
        validation_data=(testX, testY),
        validation_steps=len(testX) // batch_size,
        epochs=epochs
    )
    
    # Model değerlendirmesi
    print("[BİLGİ] Model değerlendiriliyor...")
    predIdxs = model.predict(testX, batch_size=batch_size)
    predIdxs = np.argmax(predIdxs, axis=1)
    
    print(classification_report(testY.argmax(axis=1), predIdxs,
                               target_names=lb.classes_))
    
    # Modeli kaydet
    print(f"[BİLGİ] Model kaydediliyor: {output_model_path}")
    model.save(output_model_path)
    
    # Eğitim grafiğini çiz
    plot_training(H, epochs)
    
    print("[BİLGİ] Eğitim tamamlandı!")


def plot_training(history, epochs):
    """
    Eğitim grafiğini çizer.
    
    Args:
        history: Eğitim geçmişi
        epochs: Epoch sayısı
    """
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, epochs), history.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs), history.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epochs), history.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, epochs), history.history["val_accuracy"], label="val_acc")
    plt.title("Eğitim Kaybı ve Doğruluğu")
    plt.xlabel("Epoch #")
    plt.ylabel("Kayıp/Doğruluk")
    plt.legend(loc="lower left")
    plt.savefig("training_plot.png")
    print("[BİLGİ] Eğitim grafiği kaydedildi: training_plot.png")


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description="Maske Algılama Modeli Eğitimi"
    )
    parser.add_argument("-d", "--dataset", type=str, required=True,
                       help="Veri seti klasör yolu")
    parser.add_argument("-m", "--model", type=str,
                       default="mask_detector.model",
                       help="Çıktı model dosya yolu")
    parser.add_argument("-e", "--epochs", type=int, default=20,
                       help="Epoch sayısı")
    parser.add_argument("-b", "--batch", type=int, default=32,
                       help="Batch boyutu")
    parser.add_argument("-l", "--learning-rate", type=float, default=1e-4,
                       help="Öğrenme oranı")
    
    args = parser.parse_args()
    
    # Veri seti kontrolü
    if not os.path.exists(args.dataset):
        print(f"[HATA] Veri seti klasörü bulunamadı: {args.dataset}")
        print("[BİLGİ] Lütfen veri setini şu yapıda oluşturun:")
        print("  dataset/")
        print("    ├── with_mask/")
        print("    │   ├── image1.jpg")
        print("    │   └── image2.jpg")
        print("    └── without_mask/")
        print("        ├── image1.jpg")
        print("        └── image2.jpg")
        return
    
    # Model eğitimi
    train_model(args.dataset, args.model, args.epochs, 
               args.batch, args.learning_rate)


if __name__ == "__main__":
    main()
