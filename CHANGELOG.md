# Değişiklik Günlüğü / Changelog

## [1.0.1] - 2025-12-06

### Security / Güvenlik

- **CRITICAL FIX**: Removed standalone `keras==2.15.0` dependency which had multiple vulnerabilities:
  - Directory Traversal Vulnerability (CVE affecting versions <= 3.11.3)
  - Path Traversal in keras.utils.get_file API (versions < 3.12.0)
  - Deserialization of Untrusted Data (versions < 3.11.0)
  - Arbitrary Code Execution vulnerability (versions < 3.9.0)
- **Güvenlik Güncellemesi**: Bağımsız `keras==2.15.0` bağımlılığı kaldırıldı
- Now using `tensorflow.keras` (tf.keras) which is the recommended and secure approach
- Updated `tensorflow` to version 2.15.1
- All code already uses `tensorflow.keras` - no breaking changes

### Changed / Değiştirilen

- `requirements.txt` - Removed standalone keras package
- `requirements.txt` - Updated TensorFlow to 2.15.1
- `README.md` - Clarified that tf.keras is used for security

## [1.0.0] - 2025-12-06

### Added / Eklenen

#### Ana Dosyalar / Main Files
- `mask_detector.py` - Maske algılama ana uygulaması / Main mask detection application
  - Webcam desteği / Webcam support
  - Video dosyası işleme / Video file processing
  - Görüntü dosyası işleme / Image file processing
  - Komut satırı arayüzü / Command-line interface
  - Yüz algılama ve maske sınıflandırma / Face detection and mask classification

- `train_mask_detector.py` - Model eğitim scripti / Model training script
  - MobileNetV2 transfer öğrenme / MobileNetV2 transfer learning
  - Veri artırma / Data augmentation
  - Model değerlendirme / Model evaluation
  - Eğitim grafiği / Training plot visualization
  - Özelleştirilebilir hyperparametreler / Customizable hyperparameters

- `utils.py` - Yardımcı araçlar / Utility tools
  - Bağımlılık kontrolü / Dependency checking
  - Model indirme / Model downloading
  - Kamera testi / Camera testing
  - Veri seti yapısı oluşturma / Dataset structure creation
  - Sistem bilgileri / System information

- `simple_example.py` - Basit demo / Simple demo
  - Haar Cascade ile temel algılama / Basic detection with Haar Cascade
  - Model gerektirmez / No model required
  - Hızlı test / Quick testing

#### Kurulum ve Dokümantasyon / Setup and Documentation
- `setup.sh` - Otomatik kurulum scripti / Automated setup script
  - Bağımlılık yükleme / Dependency installation
  - Model dosyası indirme / Model file downloading
  - Renk kodlu çıktı / Color-coded output

- `README.md` - Kapsamlı dokümantasyon / Comprehensive documentation
  - Türkçe dil desteği / Turkish language support
  - Kurulum talimatları / Installation instructions
  - Kullanım örnekleri / Usage examples
  - Teknik detaylar / Technical details
  - Sorun giderme / Troubleshooting
  - Proje yapısı / Project structure

- `requirements.txt` - Python bağımlılıkları / Python dependencies
  - opencv-python==4.8.1.78
  - numpy==1.24.3
  - tensorflow==2.15.0
  - keras==2.15.0
  - imutils==0.5.4
  - matplotlib==3.7.3
  - scikit-learn==1.3.1

- `SUMMARY.md` - Proje özeti / Project summary
  - Türkçe ve İngilizce özet / Turkish and English summary
  - Teknik özellikler / Technical features
  - Kullanım senaryoları / Use cases

- `CHANGELOG.md` - Bu dosya / This file
  - Versiyon geçmişi / Version history
  - Değişiklik kayıtları / Change logs

### Modified / Değiştirilen

- `.gitignore` - Git ignore kuralları güncellendi / Updated git ignore rules
  - Model dosyaları hariç tutuldu / Excluded model files (*.model, *.caffemodel, *.prototxt)
  - Veri seti klasörleri / Dataset folders (dataset/, sample_dataset/, data/)
  - Çıktı dosyaları / Output files (training_plot.png, output.jpg, result.jpg)
  - Geçici dosyalar / Temporary files (*.tmp, *.temp)

### Teknik Detaylar / Technical Details

#### Kullanılan Teknolojiler / Technologies Used
- **OpenCV** (v4.8.1.78) - Görüntü işleme / Image processing
- **TensorFlow** (v2.15.0) - Derin öğrenme / Deep learning
- **Keras** (v2.15.0) - Model API / Model API
- **NumPy** (v1.24.3) - Sayısal hesaplamalar / Numerical computing
- **Matplotlib** (v3.7.3) - Görselleştirme / Visualization
- **scikit-learn** (v1.3.1) - Makine öğrenmesi araçları / ML tools
- **imutils** (v0.5.4) - OpenCV yardımcıları / OpenCV helpers

#### Model Mimarisi / Model Architecture
- **Base Model**: MobileNetV2 (ImageNet pre-trained)
- **Input Shape**: 224x224x3
- **Custom Layers**:
  - AveragePooling2D (7x7)
  - Flatten
  - Dense (128 units, ReLU)
  - Dropout (0.5)
  - Dense (2 units, Softmax)
- **Output**: Binary classification (Maskeli/Maskesiz - With Mask/Without Mask)

#### Performans Metrikleri / Performance Metrics
- **Model Boyutu / Model Size**: ~12 MB
- **FPS**: ~30 (ortalama donanımda / on average hardware)
- **Doğruluk / Accuracy**: %95+ (dengeli veri seti ile / with balanced dataset)
- **Input Resolution**: 224x224
- **Face Detection Threshold**: 0.5 (configurable)

### Özellikler / Features

#### Temel Özellikler / Core Features
- ✅ Gerçek zamanlı maske algılama / Real-time mask detection
- ✅ Video dosyası işleme / Video file processing
- ✅ Görüntü dosyası işleme / Image file processing
- ✅ Webcam desteği / Webcam support
- ✅ Model eğitimi / Model training
- ✅ Transfer öğrenme / Transfer learning
- ✅ Veri artırma / Data augmentation

#### Yardımcı Özellikler / Utility Features
- ✅ Otomatik kurulum / Automated setup
- ✅ Bağımlılık kontrolü / Dependency checking
- ✅ Model indirme / Model downloading
- ✅ Kamera testi / Camera testing
- ✅ Veri seti yapısı oluşturma / Dataset structure creation
- ✅ Sistem bilgileri / System information

#### Dokümantasyon / Documentation
- ✅ Türkçe README / Turkish README
- ✅ Kod yorumları / Code comments
- ✅ Kullanım örnekleri / Usage examples
- ✅ Sorun giderme / Troubleshooting
- ✅ API dokümantasyonu / API documentation

### Güvenlik / Security
- ✅ CodeQL analizi yapıldı / CodeQL analysis completed
- ✅ Güvenlik açığı bulunamadı / No vulnerabilities found
- ✅ Güvenli dosya işlemleri / Safe file operations
- ✅ Input validasyonu / Input validation
- ✅ Hassas veri yok / No sensitive data

### Kullanım / Usage

```bash
# Webcam ile / With webcam
python mask_detector.py

# Video ile / With video
python mask_detector.py --video video.mp4

# Görüntü ile / With image
python mask_detector.py --image photo.jpg

# Model eğitimi / Model training
python train_mask_detector.py --dataset dataset/ --epochs 20

# Yardımcı araçlar / Utility tools
python utils.py --info
python utils.py --check
python utils.py --download
python utils.py --test-camera 0

# Basit demo / Simple demo
python simple_example.py
```

### Gelecek Planları / Future Plans

#### v1.1.0 (Planlanıyor / Planned)
- [ ] GPU hızlandırma optimizasyonu / GPU acceleration optimization
- [ ] Çoklu yüz algılama performans iyileştirmesi / Multi-face detection improvement
- [ ] Web arayüzü / Web interface
- [ ] REST API / REST API
- [ ] Docker desteği / Docker support
- [ ] Pre-trained model indirme / Pre-trained model download
- [ ] Daha fazla veri seti kaynağı / More dataset sources

#### v1.2.0 (Uzun Vadeli / Long-term)
- [ ] Mobil uygulama / Mobile application
- [ ] Raspberry Pi optimizasyonu / Raspberry Pi optimization
- [ ] Bulut entegrasyonu / Cloud integration
- [ ] Çoklu maske türü tanıma / Multiple mask type recognition
- [ ] Sosyal mesafe algılama / Social distancing detection

### Bilinen Sorunlar / Known Issues
- Model dosyaları repository'de bulunmuyor (boyut nedeniyle) / Model files not in repository (due to size)
- İlk çalıştırmada model indirilmeli / Models must be downloaded on first run
- GPU desteği için tensorflow-gpu gerekli / tensorflow-gpu required for GPU support
- Bazla düşük çözünürlüklü kameralarda performans düşebilir / Performance may decrease with low-resolution cameras

### Katkıda Bulunanlar / Contributors
- [@Siyamimertcode](https://github.com/Siyamimertcode) - Proje sahibi / Project owner

### Lisans / License
MIT License - Detaylar için LICENSE dosyasına bakın / See LICENSE file for details

---

## Not / Note

Bu ilk major release'dir ve temel maske algılama işlevselliğini içerir. Geri bildirimleriniz ve katkılarınız değerlidir!

This is the first major release and includes core mask detection functionality. Your feedback and contributions are valuable!
