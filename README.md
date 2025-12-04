# LIP-SYNC-float-fast

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0.1-red.svg)](https://pytorch.org/)

*Lip-sync chất lượng cao với FLOAT model*

</div>

---

## 📖 Giới thiệu

**LIP-SYNC-float-fast** là một hệ thống đồng bộ môi (lip-sync) tiên tiến, sử dụng mô hình FLOAT để tạo video với môi khớp hoàn hảo với âm thanh đầu vào.

### ✨ Tính năng nổi bật

- 🎭 **Chất lượng cao**: Đồng bộ môi tự nhiên và mượt mà
- 🚀 **Xử lý nhanh**: Tối ưu hóa cho tốc độ inference
- 🔧 **Dễ dàng sử dụng**: Script đã được cấu hình và tối ưu sẵn
- 🎯 **Phát hiện khuôn mặt tự động**: Tự động detect và crop khuôn mặt
- 💯 **Hỗ trợ nhiều định dạng**: Xử lý được các định dạng video và audio phổ biến

### 🖥️ Yêu cầu hệ thống

- **Hệ điều hành**: Ubuntu (hoặc các bản phân phối Linux khác)
- **Python**: 3.10
- **CUDA**: 11.8 (khuyến nghị cho GPU acceleration)
- **RAM**: Tối thiểu 8GB
- **GPU**: NVIDIA GPU với ít nhất 6GB VRAM (khuyến nghị)

## Các bước cài đặt

### 1. Tạo môi trường ảo
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 2. Cài đặt PyTorch
```bash
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
```

### 3. Cài đặt các thư viện khác
```bash
pip install -r requirements.txt
```

### 4. Tải model checkpoints
```bash
# Cài đặt gdown
pip install gdown

# Tải model FLOAT
gdown --id 1rvWuM12cyvNvBQNCLmG4Fr2L1rpjQBF0

# Di chuyển model vào folder checkpoints
mv float.pth checkpoints/
```

**Lưu ý:** Các model wav2vec2 sẽ được tự động tải khi chạy lần đầu

## Hướng dẫn sử dụng

### Yêu cầu đầu vào

#### 1. Reference Image (Ảnh tham chiếu)
- Format: JPG, PNG
- Chứa khuôn mặt rõ ràng, không bị che khuất
- Chất lượng càng cao càng tốt

#### 2. Audio (File âm thanh)
- Format: WAV, MP3
- Sampling rate: 16000Hz (được xử lý tự động)
- Chất lượng tốt, ít nhiễu

### Chạy inference

#### Cú pháp cơ bản
```bash
python generate.py \
    --ref_path <đường_dẫn_ảnh> \
    --aud_path <đường_dẫn_audio> \
    --seed 15 \
    --a_cfg_scale 2 \
    --e_cfg_scale 1 \
    --ckpt_path ./checkpoints/float.pth
```

#### Ví dụ
```bash
python generate.py --ref_path assets/thl.jpg --aud_path assets/thl_trimmed.wav --seed 15 --a_cfg_scale 2 --e_cfg_scale 1 --ckpt_path ./checkpoints/float.pth
```

### Tham số cấu hình

| Tham số | Mô tả | Mặc định |
|---------|-------|----------|
| `--ref_path` | Đường dẫn đến ảnh tham chiếu | Bắt buộc |
| `--aud_path` | Đường dẫn đến file audio | Bắt buộc |
| `--seed` | Random seed cho reproducibility | 15 |
| `--a_cfg_scale` | Audio classifier-free guidance scale | 2 |
| `--e_cfg_scale` | Emotion classifier-free guidance scale | 1 |
| `--ckpt_path` | Đường dẫn đến model checkpoint | `./checkpoints/float.pth` |
| `--fps` | Frame per second của video đầu ra | 25 |

### Tài nguyên có sẵn

- **Assets**: Folder `assets/` chứa các file mẫu để test
- **Checkpoints**: Folder `checkpoints/` chứa các model đã train
- **Results**: Kết quả sau khi chạy sẽ được lưu vào folder `results/`

### Output

Kết quả video sẽ được lưu trong folder `results/` với format:
- Video file: MP4
- FPS: Theo cấu hình (mặc định 25fps)
- Resolution: Tự động điều chỉnh theo input

## Troubleshooting

### Lỗi thường gặp

1. **CUDA out of memory**
   - Giảm resolution của ảnh đầu vào
   - Sử dụng GPU có VRAM lớn hơn

2. **Face detection failed**
   - Đảm bảo ảnh có khuôn mặt rõ ràng
   - Thử với ảnh có độ phân giải cao hơn
   - Khuôn mặt không bị che khuất

3. **Audio format not supported**
   - Convert audio sang WAV format
   - Đảm bảo sampling rate phù hợp

## Cấu trúc thư mục

```
LIP-SYNC-float-fast/
├── generate.py              # Script chính để chạy inference
├── environments.sh          # Script cài đặt môi trường
├── download_checkpoints.sh  # Script tải model
├── requirements.txt         # Dependencies
├── inference.txt           # Ví dụ lệnh inference
├── assets/                 # File mẫu để test
├── checkpoints/           # Model checkpoints
├── models/               # Model architecture
├── options/             # Configuration options
└── results/            # Output videos

```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- FLOAT model architecture
- Face alignment library
- Wav2Vec2 for audio processing
