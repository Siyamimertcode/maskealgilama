#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maske Algılama Yardımcı Fonksiyonlar
"""

import cv2
import os
import numpy as np
from pathlib import Path


def download_model_files():
    """
    Gerekli model dosyalarını indirir.
    """
    import urllib.request
    
    files = {
        'deploy.prototxt': 'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt',
        'res10_300x300_ssd_iter_140000.caffemodel': 'https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel'
    }
    
    for filename, url in files.items():
        if not os.path.exists(filename):
            print(f"[BİLGİ] {filename} indiriliyor...")
            try:
                urllib.request.urlretrieve(url, filename)
                print(f"[BİLGİ] {filename} başarıyla indirildi")
            except Exception as e:
                print(f"[HATA] {filename} indirilemedi: {e}")
        else:
            print(f"[BİLGİ] {filename} zaten mevcut")


def check_dependencies():
    """
    Gerekli kütüphanelerin yüklü olup olmadığını kontrol eder.
    """
    dependencies = [
        'cv2',
        'numpy',
        'tensorflow',
        'keras',
        'sklearn',
        'matplotlib',
        'imutils'
    ]
    
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"[✓] {dep}")
        except ImportError:
            print(f"[✗] {dep} - EKSIK")
            missing.append(dep)
    
    if missing:
        print(f"\n[UYARI] Eksik bağımlılıklar: {', '.join(missing)}")
        print("[BİLGİ] Yüklemek için: pip install -r requirements.txt")
        return False
    else:
        print("\n[BİLGİ] Tüm bağımlılıklar yüklü!")
        return True


def test_camera(camera_index=0):
    """
    Kamera erişimini test eder.
    
    Args:
        camera_index: Kamera indeksi (varsayılan: 0)
    """
    print(f"[BİLGİ] Kamera {camera_index} test ediliyor...")
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"[HATA] Kamera {camera_index} açılamadı")
        return False
    
    ret, frame = cap.read()
    
    if not ret:
        print("[HATA] Kamera görüntüsü alınamadı")
        cap.release()
        return False
    
    print(f"[BİLGİ] Kamera çözünürlüğü: {frame.shape[1]}x{frame.shape[0]}")
    print("[BİLGİ] Kamera başarıyla test edildi!")
    
    cap.release()
    return True


def create_sample_dataset_structure(base_path="sample_dataset"):
    """
    Örnek veri seti klasör yapısı oluşturur.
    
    Args:
        base_path: Ana klasör yolu
    """
    print(f"[BİLGİ] Örnek veri seti yapısı oluşturuluyor: {base_path}")
    
    paths = [
        os.path.join(base_path, "with_mask"),
        os.path.join(base_path, "without_mask")
    ]
    
    for path in paths:
        os.makedirs(path, exist_ok=True)
        print(f"[BİLGİ] Klasör oluşturuldu: {path}")
    
    # README dosyası oluştur
    readme_path = os.path.join(base_path, "README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("Veri Seti Klasör Yapısı\n")
        f.write("=" * 50 + "\n\n")
        f.write("Bu klasöre eğitim görüntülerinizi ekleyin:\n\n")
        f.write("1. with_mask/ klasörüne maskeli yüz görüntüleri\n")
        f.write("2. without_mask/ klasörüne maskesiz yüz görüntüleri\n\n")
        f.write("Öneriler:\n")
        f.write("- Her kategoride en az 100 görüntü olmalı\n")
        f.write("- Görüntüler farklı açılar ve aydınlatmalarda olmalı\n")
        f.write("- Dengeli dağılım için her kategoride eşit sayıda görüntü\n")
        f.write("- JPG, PNG formatları desteklenir\n")
    
    print(f"[BİLGİ] README dosyası oluşturuldu: {readme_path}")
    print("[BİLGİ] Veri seti yapısı hazır!")


def get_system_info():
    """
    Sistem bilgilerini gösterir.
    """
    import platform
    
    print("\n" + "=" * 60)
    print("SİSTEM BİLGİLERİ")
    print("=" * 60)
    print(f"İşletim Sistemi: {platform.system()} {platform.release()}")
    print(f"Python Versiyonu: {platform.python_version()}")
    print(f"OpenCV Versiyonu: {cv2.__version__}")
    
    try:
        import tensorflow as tf
        print(f"TensorFlow Versiyonu: {tf.__version__}")
        print(f"GPU Desteği: {'Var' if len(tf.config.list_physical_devices('GPU')) > 0 else 'Yok'}")
    except:
        print("TensorFlow: Yüklü değil")
    
    print("=" * 60 + "\n")


def main():
    """Ana fonksiyon"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Maske Algılama Yardımcı Araçlar"
    )
    parser.add_argument("--check", action="store_true",
                       help="Bağımlılıkları kontrol et")
    parser.add_argument("--download", action="store_true",
                       help="Model dosyalarını indir")
    parser.add_argument("--test-camera", type=int, default=None,
                       help="Kamera test et (indeks belirtin)")
    parser.add_argument("--create-dataset", type=str, default=None,
                       help="Örnek veri seti yapısı oluştur")
    parser.add_argument("--info", action="store_true",
                       help="Sistem bilgilerini göster")
    
    args = parser.parse_args()
    
    if args.info:
        get_system_info()
    
    if args.check:
        print("\n[BİLGİ] Bağımlılıklar kontrol ediliyor...\n")
        check_dependencies()
    
    if args.download:
        print("\n[BİLGİ] Model dosyaları indiriliyor...\n")
        download_model_files()
    
    if args.test_camera is not None:
        print()
        test_camera(args.test_camera)
    
    if args.create_dataset:
        print()
        create_sample_dataset_structure(args.create_dataset)
    
    # Argüman verilmemişse yardım göster
    if not any([args.check, args.download, args.test_camera is not None, 
                args.create_dataset, args.info]):
        parser.print_help()
        print("\nÖrnekler:")
        print("  python utils.py --info")
        print("  python utils.py --check")
        print("  python utils.py --download")
        print("  python utils.py --test-camera 0")
        print("  python utils.py --create-dataset my_dataset")


if __name__ == "__main__":
    main()
