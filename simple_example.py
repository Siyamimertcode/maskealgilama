#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit Maske Algılama Örneği
OpenCV Haar Cascade kullanan basitleştirilmiş versiyon
"""

import cv2
import numpy as np


def simple_mask_detector():
    """
    Haar Cascade ile basit maske algılama.
    Model dosyası gerektirmeyen basitleştirilmiş versiyon.
    """
    print("[BİLGİ] Basit maske algılayıcı başlatılıyor...")
    print("[BİLGİ] Bu örnek, Haar Cascade kullanarak yüz algılama yapar")
    print("[BİLGİ] Gerçek maske algılama için mask_detector.py kullanın")
    
    # Haar Cascade yüz algılayıcı
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Webcam başlat
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[HATA] Kamera açılamadı!")
        return
    
    print("[BİLGİ] Kamera başlatıldı. Çıkmak için 'q' tuşuna basın")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Gri tonlamaya çevir
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Yüzleri tespit et
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )
        
        # Her yüz için
        for (x, y, w, h) in faces:
            # Yüz bölgesini al
            face_roi = frame[y:y+h, x:x+w]
            
            # Basit renk analizi ile maske tahmini
            # Yüzün alt yarısındaki ortalama renk
            lower_face = face_roi[h//2:, :]
            avg_color = np.mean(lower_face)
            
            # Basit tahmin (gerçek model kadar doğru değil)
            # Açık renkse maskeli olabilir
            if avg_color > 100:
                label = "Muhtemelen Maskeli"
                color = (0, 255, 0)
            else:
                label = "Muhtemelen Maskesiz"
                color = (0, 0, 255)
            
            # Çerçeve çiz
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Bilgi göster
        cv2.putText(frame, "Basit Ornek - Gercek model icin mask_detector.py kullanin",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Tespit edilen yuz: {len(faces)}",
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Göster
        cv2.imshow("Basit Maske Algilama Ornegi", frame)
        
        # Çıkış
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("[BİLGİ] Uygulama kapatıldı")


def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("BASIT MASKE ALGILAMA ÖRNEĞİ")
    print("=" * 60)
    print()
    print("Bu basit bir demo uygulamasıdır.")
    print("Daha doğru sonuçlar için mask_detector.py kullanın.")
    print()
    print("Kontroller:")
    print("  - 'q': Çıkış")
    print()
    print("=" * 60)
    
    try:
        simple_mask_detector()
    except KeyboardInterrupt:
        print("\n[BİLGİ] Kullanıcı tarafından sonlandırıldı")
    except Exception as e:
        print(f"[HATA] Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
