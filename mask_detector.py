#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maske Algılama (Mask Detection) Script
Bu script, kamera veya video dosyasından yüz ve maske algılama yapar.
"""

import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import argparse
import os


def detect_and_predict_mask(frame, faceNet, maskNet, confidence_threshold=0.5):
    """
    Görüntüdeki yüzleri tespit eder ve maske takıp takmadığını kontrol eder.
    
    Args:
        frame: Giriş görüntüsü
        faceNet: Yüz algılama modeli
        maskNet: Maske sınıflandırma modeli
        confidence_threshold: Yüz algılama için güven eşiği
    
    Returns:
        locs: Yüz konumları listesi
        preds: Tahmin sonuçları listesi
    """
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    
    faceNet.setInput(blob)
    detections = faceNet.forward()
    
    faces = []
    locs = []
    preds = []
    
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > confidence_threshold:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
            
            face = frame[startY:endY, startX:endX]
            if face.shape[0] > 0 and face.shape[1] > 0:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)
                
                faces.append(face)
                locs.append((startX, startY, endX, endY))
    
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    
    return (locs, preds)


def load_face_detector(prototxt_path="deploy.prototxt", 
                       weights_path="res10_300x300_ssd_iter_140000.caffemodel"):
    """
    Yüz algılama modelini yükler.
    
    Args:
        prototxt_path: Model mimarisi dosyası
        weights_path: Model ağırlıkları dosyası
    
    Returns:
        Yüklenen yüz algılama modeli
    """
    print("[BİLGİ] Yüz algılama modeli yükleniyor...")
    if not os.path.exists(prototxt_path) or not os.path.exists(weights_path):
        print(f"[HATA] Model dosyaları bulunamadı: {prototxt_path}, {weights_path}")
        print("[BİLGİ] Alternatif olarak OpenCV'nin yerleşik yüz dedektörü kullanılacak")
        return None
    
    faceNet = cv2.dnn.readNet(prototxt_path, weights_path)
    return faceNet


def load_mask_detector(model_path="mask_detector.model"):
    """
    Maske algılama modelini yükler.
    
    Args:
        model_path: Model dosyası yolu
    
    Returns:
        Yüklenen maske algılama modeli
    """
    print("[BİLGİ] Maske algılama modeli yükleniyor...")
    if not os.path.exists(model_path):
        print(f"[HATA] Maske modeli bulunamadı: {model_path}")
        print("[BİLGİ] Lütfen önce modeli eğitin veya indirin")
        return None
    
    maskNet = load_model(model_path)
    return maskNet


def detect_mask_video(video_source=0, face_detector=None, mask_detector=None):
    """
    Video kaynağından maske algılaması yapar.
    
    Args:
        video_source: Video dosyası yolu veya kamera index (0 için webcam)
        face_detector: Yüz algılama modeli
        mask_detector: Maske algılama modeli
    """
    print("[BİLGİ] Video stream başlatılıyor...")
    vs = cv2.VideoCapture(video_source)
    
    if not vs.isOpened():
        print("[HATA] Video kaynağı açılamadı")
        return
    
    while True:
        ret, frame = vs.read()
        if not ret:
            print("[BİLGİ] Video sona erdi veya kare okunamadı")
            break
        
        if face_detector is None or mask_detector is None:
            cv2.putText(frame, "Model yuklenemedi!", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Maske Algilama", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            continue
        
        (locs, preds) = detect_and_predict_mask(frame, face_detector, mask_detector)
        
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            
            label = "Maskeli" if mask > withoutMask else "Maskesiz"
            color = (0, 255, 0) if label == "Maskeli" else (0, 0, 255)
            
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            
            cv2.putText(frame, label, (startX, startY - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        
        cv2.imshow("Maske Algilama", frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("q"):
            print("[BİLGİ] Çıkış yapılıyor...")
            break
    
    vs.release()
    cv2.destroyAllWindows()


def detect_mask_image(image_path, face_detector=None, mask_detector=None, 
                     output_path="output.jpg"):
    """
    Görüntü dosyasından maske algılaması yapar.
    
    Args:
        image_path: Görüntü dosyası yolu
        face_detector: Yüz algılama modeli
        mask_detector: Maske algılama modeli
        output_path: Çıktı görüntüsü yolu
    """
    print(f"[BİLGİ] Görüntü yükleniyor: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        print("[HATA] Görüntü yüklenemedi")
        return
    
    if face_detector is None or mask_detector is None:
        print("[HATA] Modeller yüklenemedi")
        return
    
    (locs, preds) = detect_and_predict_mask(image, face_detector, mask_detector)
    
    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred
        
        label = "Maskeli" if mask > withoutMask else "Maskesiz"
        color = (0, 255, 0) if label == "Maskeli" else (0, 0, 255)
        
        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
        
        cv2.putText(image, label, (startX, startY - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
    
    cv2.imwrite(output_path, image)
    print(f"[BİLGİ] Sonuç kaydedildi: {output_path}")
    
    cv2.imshow("Maske Algilama", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description="Maske Algılama Uygulaması"
    )
    parser.add_argument("-i", "--image", type=str, default=None,
                       help="Görüntü dosyası yolu")
    parser.add_argument("-v", "--video", type=str, default=None,
                       help="Video dosyası yolu")
    parser.add_argument("-m", "--model", type=str, 
                       default="mask_detector.model",
                       help="Maske algılama modeli yolu")
    parser.add_argument("-f", "--face", type=str,
                       default="deploy.prototxt",
                       help="Yüz algılama prototxt dosyası")
    parser.add_argument("-w", "--weights", type=str,
                       default="res10_300x300_ssd_iter_140000.caffemodel",
                       help="Yüz algılama model ağırlıkları")
    parser.add_argument("-o", "--output", type=str,
                       default="output.jpg",
                       help="Çıktı görüntüsü yolu")
    parser.add_argument("-c", "--confidence", type=float, default=0.5,
                       help="Yüz algılama güven eşiği")
    
    args = parser.parse_args()
    
    # Modelleri yükle
    face_detector = load_face_detector(args.face, args.weights)
    mask_detector = load_mask_detector(args.model)
    
    # Görüntü veya video işle
    if args.image:
        detect_mask_image(args.image, face_detector, mask_detector, args.output)
    elif args.video:
        detect_mask_video(args.video, face_detector, mask_detector)
    else:
        # Varsayılan olarak webcam kullan
        detect_mask_video(0, face_detector, mask_detector)


if __name__ == "__main__":
    main()
