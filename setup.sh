#!/bin/bash
# Kurulum ve model indirme script

echo "=================================="
echo "Maske Algılama - Kurulum Script"
echo "=================================="
echo ""

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Python kontrolü
echo -e "${YELLOW}[1/4] Python kontrolü yapılıyor...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}HATA: Python3 bulunamadı. Lütfen Python 3.7+ yükleyin.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python bulundu: $(python3 --version)${NC}"
echo ""

# pip kontrolü
echo -e "${YELLOW}[2/4] pip kontrolü yapılıyor...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}HATA: pip3 bulunamadı. Lütfen pip yükleyin.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip bulundu: $(pip3 --version)${NC}"
echo ""

# Bağımlılıkları yükle
echo -e "${YELLOW}[3/4] Python bağımlılıkları yükleniyor...${NC}"
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Bağımlılıklar başarıyla yüklendi${NC}"
else
    echo -e "${RED}✗ Bağımlılık yüklemesi başarısız${NC}"
    exit 1
fi
echo ""

# Model dosyalarını indir
echo -e "${YELLOW}[4/4] Model dosyaları indiriliyor...${NC}"

# deploy.prototxt
if [ ! -f "deploy.prototxt" ]; then
    echo "  - deploy.prototxt indiriliyor..."
    wget -q https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
    if [ $? -eq 0 ]; then
        echo -e "    ${GREEN}✓ deploy.prototxt indirildi${NC}"
    else
        echo -e "    ${RED}✗ deploy.prototxt indirilemedi${NC}"
    fi
else
    echo -e "    ${GREEN}✓ deploy.prototxt zaten mevcut${NC}"
fi

# res10_300x300_ssd_iter_140000.caffemodel
if [ ! -f "res10_300x300_ssd_iter_140000.caffemodel" ]; then
    echo "  - res10_300x300_ssd_iter_140000.caffemodel indiriliyor..."
    wget -q https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
    if [ $? -eq 0 ]; then
        echo -e "    ${GREEN}✓ res10_300x300_ssd_iter_140000.caffemodel indirildi${NC}"
    else
        echo -e "    ${RED}✗ res10_300x300_ssd_iter_140000.caffemodel indirilemedi${NC}"
    fi
else
    echo -e "    ${GREEN}✓ res10_300x300_ssd_iter_140000.caffemodel zaten mevcut${NC}"
fi

echo ""
echo "=================================="
echo -e "${GREEN}Kurulum tamamlandı!${NC}"
echo "=================================="
echo ""
echo "Kullanım:"
echo "  1. Model eğitimi için: python3 train_mask_detector.py --dataset <veri_seti_yolu>"
echo "  2. Webcam kullanımı: python3 mask_detector.py"
echo "  3. Basit örnek: python3 simple_example.py"
echo ""
echo "Detaylı bilgi için README.md dosyasına bakın."
echo ""
