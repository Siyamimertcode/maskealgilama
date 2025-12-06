# Security Policy / Güvenlik Politikası

## Supported Versions / Desteklenen Sürümler

| Version | Supported          | Güvenlik Desteği |
| ------- | ------------------ | ---------------- |
| 1.0.1   | :white_check_mark: | Evet             |
| 1.0.0   | :x:                | Hayır (Güvenlik açığı) |

## Security Updates / Güvenlik Güncellemeleri

### Version 1.0.1 (2025-12-06)

✅ **CRITICAL SECURITY FIX**: Removed vulnerable keras dependency

#### Vulnerabilities Fixed / Düzeltilen Güvenlik Açıkları:

1. **Directory Traversal Vulnerability**
   - Package: keras <= 3.11.3
   - Fixed by: Removing standalone keras, using tf.keras

2. **Path Traversal in keras.utils.get_file API**
   - Package: keras < 3.12.0
   - Fixed by: Removing standalone keras, using tf.keras

3. **Deserialization of Untrusted Data**
   - Package: keras < 3.11.0
   - Fixed by: Removing standalone keras, using tf.keras

4. **Arbitrary Code Execution vulnerability**
   - Package: keras < 3.9.0
   - Fixed by: Removing standalone keras, using tf.keras

#### Solution / Çözüm:

- Removed standalone `keras==2.15.0` from requirements.txt
- Now using `tensorflow.keras` (tf.keras) which is bundled with TensorFlow
- Updated TensorFlow to 2.15.1
- No breaking changes - code already used `tensorflow.keras` imports

## Reporting a Vulnerability / Güvenlik Açığı Bildirimi

### English

If you discover a security vulnerability in this project, please:

1. **DO NOT** open a public issue
2. Email the maintainer directly (see GitHub profile)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work on a fix as soon as possible.

### Türkçe

Bu projede bir güvenlik açığı keşfederseniz, lütfen:

1. Açık bir issue **AÇMAYIN**
2. Bakımcıya doğrudan e-posta gönderin (GitHub profilinde)
3. Şunları ekleyin:
   - Güvenlik açığının açıklaması
   - Tekrarlama adımları
   - Potansiyel etki
   - Önerilen düzeltme (varsa)

48 saat içinde yanıt vereceğiz ve mümkün olan en kısa sürede düzeltme üzerinde çalışacağız.

## Security Best Practices / Güvenlik En İyi Uygulamaları

### For Users / Kullanıcılar İçin

1. **Always use the latest version** / **Her zaman en son sürümü kullanın**
   ```bash
   git pull origin main
   pip install -r requirements.txt --upgrade
   ```

2. **Verify dependencies** / **Bağımlılıkları doğrulayın**
   ```bash
   pip list
   pip audit  # Python 3.11+
   ```

3. **Don't run untrusted models** / **Güvenilmeyen modeller çalıştırmayın**
   - Only use models you trained yourself or from trusted sources
   - Verify model file integrity before loading

4. **Be careful with user input** / **Kullanıcı girdilerine dikkat edin**
   - Validate all file paths
   - Don't allow arbitrary file access
   - Sanitize video/image inputs

### For Developers / Geliştiriciler İçin

1. **Keep dependencies updated** / **Bağımlılıkları güncel tutun**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

2. **Run security scans** / **Güvenlik taramaları yapın**
   ```bash
   # Check for known vulnerabilities
   pip audit  # Python 3.11+
   safety check  # Alternative tool
   ```

3. **Use tf.keras, not standalone keras** / **Bağımsız keras değil tf.keras kullanın**
   ```python
   # Good / İyi
   from tensorflow.keras.models import load_model
   
   # Bad / Kötü
   from keras.models import load_model
   ```

4. **Validate model files** / **Model dosyalarını doğrulayın**
   - Check file extensions
   - Verify file sizes
   - Use trusted model sources only

## Known Issues / Bilinen Sorunlar

### Current / Güncel

None - All known vulnerabilities have been fixed in v1.0.1.

Yok - Tüm bilinen güvenlik açıkları v1.0.1'de düzeltildi.

### Historical / Geçmiş

- **v1.0.0**: Used vulnerable keras==2.15.0 package (FIXED in v1.0.1)
- **v1.0.0**: Güvenlik açığı bulunan keras==2.15.0 paketi kullanıldı (v1.0.1'de DÜZELTİLDİ)

## Security Audit History / Güvenlik Denetimi Geçmişi

| Date       | Tool    | Result | Notes                           |
|------------|---------|--------|---------------------------------|
| 2025-12-06 | CodeQL  | PASS   | No vulnerabilities detected     |
| 2025-12-06 | Advisory DB | FAIL | Keras vulnerabilities found  |
| 2025-12-06 | Advisory DB | PASS | Fixed by removing keras      |

## Acknowledgments / Teşekkürler

We thank the security community for reporting vulnerabilities and helping keep this project secure.

Güvenlik topluluğuna güvenlik açıklarını bildirdiği ve bu projeyi güvenli tutmaya yardımcı olduğu için teşekkür ederiz.

---

For more information, see CHANGELOG.md and SUMMARY.md

Daha fazla bilgi için CHANGELOG.md ve SUMMARY.md dosyalarına bakın.
