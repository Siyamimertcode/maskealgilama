# Maske Algılama (Mask Detection) Projesi

Bu proje, yapay zeka ve bilgisayarla görü teknolojilerini kullanarak kişilerin maske takıp takmadığını gerçek zamanlı olarak tespit eden bir uygulamadır.

## 🎯 Özellikler

- ✅ Gerçek zamanlı maske algılama
- ✅ Webcam, video dosyası veya görüntü dosyası üzerinde çalışma
- ✅ MobileNetV2 tabanlı transfer öğrenme
- ✅ Yüksek doğruluk oranı
- ✅ Türkçe dil desteği
- ✅ Kolay kullanım ve entegrasyon

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- Webcam (gerçek zamanlı algılama için)

## 🚀 Kurulum

### 1. Repository'yi klonlayın

```bash
git clone https://github.com/Siyamimertcode/maskealgilama.git
cd maskealgilama
```

### 2. Gerekli kütüphaneleri yükleyin

```bash
pip install -r requirements.txt
```

### 3. Model dosyalarını hazırlayın

#### Yüz Algılama Modeli

OpenCV'nin DNN modülü için gerekli dosyaları indirin:

```bash
# deploy.prototxt
wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt

# res10_300x300_ssd_iter_140000.caffemodel
wget https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
```

#### Maske Algılama Modeli

Model eğitimi için kendi veri setinizi hazırlayın veya mevcut bir modeli kullanın.

## 📊 Veri Seti Hazırlama

Model eğitimi için veri setinizi şu yapıda oluşturun:

```
dataset/
├── with_mask/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── without_mask/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

**Not:** Veri setinde dengeli sayıda maskeli ve maskesiz görüntü bulundurmanız önerilir.

## 🎓 Model Eğitimi

Kendi veri setinizle model eğitmek için:

```bash
python train_mask_detector.py --dataset dataset --epochs 20
```

### Ek Parametreler

- `--dataset`: Veri seti klasör yolu (zorunlu)
- `--model`: Çıktı model dosyası (varsayılan: mask_detector.model)
- `--epochs`: Epoch sayısı (varsayılan: 20)
- `--batch`: Batch boyutu (varsayılan: 32)
- `--learning-rate`: Öğrenme oranı (varsayılan: 1e-4)

### Örnek:

```bash
python train_mask_detector.py \
    --dataset dataset \
    --model mask_detector.model \
    --epochs 25 \
    --batch 16 \
    --learning-rate 0.0001
```

## 💻 Kullanım

### 1. Webcam ile Gerçek Zamanlı Algılama

```bash
python mask_detector.py
```

### 2. Video Dosyası ile Algılama

```bash
python mask_detector.py --video video.mp4
```

### 3. Görüntü Dosyası ile Algılama

```bash
python mask_detector.py --image image.jpg --output result.jpg
```

### Ek Parametreler

- `-i, --image`: Görüntü dosyası yolu
- `-v, --video`: Video dosyası yolu
- `-m, --model`: Maske algılama modeli yolu (varsayılan: mask_detector.model)
- `-f, --face`: Yüz algılama prototxt dosyası (varsayılan: deploy.prototxt)
- `-w, --weights`: Yüz algılama model ağırlıkları
- `-o, --output`: Çıktı görüntüsü yolu (varsayılan: output.jpg)
- `-c, --confidence`: Yüz algılama güven eşiği (varsayılan: 0.5)

### Tam Örnek:

```bash
python mask_detector.py \
    --image test.jpg \
    --model mask_detector.model \
    --face deploy.prototxt \
    --weights res10_300x300_ssd_iter_140000.caffemodel \
    --output result.jpg \
    --confidence 0.6
```

## 🎮 Kontroller

- `q`: Uygulamadan çıkış (video/webcam modunda)

## 🏗️ Proje Yapısı

```
maskealgilama/
├── mask_detector.py           # Ana algılama script
├── train_mask_detector.py     # Model eğitim script
├── requirements.txt            # Python bağımlılıkları
├── README.md                   # Proje dokümantasyonu
├── LICENSE                     # MIT Lisansı
├── .gitignore                  # Git ignore dosyası
├── deploy.prototxt             # Yüz algılama model mimarisi
├── res10_300x300_ssd_iter_140000.caffemodel  # Yüz algılama ağırlıkları
└── mask_detector.model         # Eğitilmiş maske algılama modeli
```

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

- **OpenCV**: Görüntü işleme ve yüz algılama
- **TensorFlow/Keras**: Derin öğrenme framework (tf.keras kullanılır - güvenlik için)
- **MobileNetV2**: Transfer öğrenme için temel model
- **NumPy**: Sayısal hesaplamalar
- **Matplotlib**: Görselleştirme

### Model Mimarisi

1. **Yüz Algılama**: OpenCV DNN modülü ile SSD (Single Shot Detector)
2. **Maske Sınıflandırma**: MobileNetV2 tabanlı transfer öğrenme
   - Input: 224x224x3 RGB görüntü
   - Base Model: MobileNetV2 (ImageNet ağırlıkları)
   - Custom Layers: AveragePooling2D → Flatten → Dense(128) → Dropout(0.5) → Dense(2)
   - Output: 2 sınıf (Maskeli/Maskesiz)

### Performans

- Model boyutu: ~12 MB
- Gerçek zamanlı işleme: ~30 FPS (ortalama donanımda)
- Doğruluk oranı: %95+ (dengeli veri seti ile)

## 📈 Sonuçlar

Model eğitimi sonrasında şu çıktıları alırsınız:

- `mask_detector.model`: Eğitilmiş model
- `training_plot.png`: Eğitim kayıp ve doğruluk grafiği
- Konsol çıktısı: Sınıflandırma raporu (precision, recall, f1-score)

## 🐛 Sorun Giderme

### Model dosyaları bulunamıyor

```bash
# Yüz algılama modelini tekrar indirin
wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
wget https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
```

### Webcam açılmıyor

- Webcam bağlantısını kontrol edin
- Başka bir uygulama webcam'i kullanıyor olabilir
- Video kaynağı indexini değiştirmeyi deneyin: `python mask_detector.py --video 1`

### Import hataları

```bash
# Tüm bağımlılıkları tekrar yükleyin
pip install --upgrade -r requirements.txt
```

### Düşük performans

- Batch boyutunu azaltın
- Görüntü çözünürlüğünü düşürün
- GPU desteği için TensorFlow-GPU yükleyin

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

**Siyamimertcode**

- GitHub: [@Siyamimertcode](https://github.com/Siyamimertcode)

## 🙏 Teşekkürler

- OpenCV ekibine
- TensorFlow/Keras geliştiricilerine
- Açık kaynak topluluğuna

## 📚 Kaynaklar

- [OpenCV DNN Module](https://docs.opencv.org/master/d2/d58/tutorial_table_of_content_dnn.html)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)
- [Transfer Learning Guide](https://www.tensorflow.org/tutorials/images/transfer_learning)

## ⚠️ Uyarı

Bu uygulama eğitim ve araştırma amaçlıdır. Gerçek dünya uygulamalarında kullanılmadan önce kapsamlı testler yapılmalıdır.

---

**Not:** Sorularınız veya önerileriniz için GitHub Issues kullanabilirsiniz.
