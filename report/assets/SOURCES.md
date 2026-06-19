# Nguồn hình minh họa — `report/assets/`

Bảng tra cứu nguồn gốc và giấy phép cho mọi hình dùng trong báo cáo PKI.
Khi thêm hình mới, cập nhật bảng này **trước** khi chèn vào `.tex`.

## Hình tải từ Wikimedia Commons (CC BY-SA / Public Domain)

| Tệp | Mô tả | Nguồn | Giấy phép |
|---|---|---|---|
| `mitm_attack.png` | Tấn công trung gian (MITM) | [Man in the middle attack](https://commons.wikimedia.org/wiki/File:Man_in_the_middle_attack.svg) | CC BY-SA 3.0 |
| `tls_handshake.png` | Bắt tay SSL/TLS với một chứng chỉ | [SSL handshake with only one certificate](https://commons.wikimedia.org/wiki/File:SSL_handshake_with_only_one_certificate.svg) | CC BY-SA 3.0 |
| `x509_structure.png` | Cấu trúc chứng chỉ X.509 | [X.509.svg](https://commons.wikimedia.org/wiki/File:X.509.svg) | CC BY-SA 3.0 |
| `pki_hierarchy.png` | Kiến trúc phân cấp PKI | [Public key infrastructure.svg](https://commons.wikimedia.org/wiki/File:Public_key_infrastructure.svg) | CC BY-SA 3.0 |
| `certificate_transparency.png` | Certificate Transparency | [Certificate Transparency.svg](https://commons.wikimedia.org/wiki/File:Certificate_Transparency.svg) | CC BY-SA 4.0 |
| `openssl_logo.png` | Logo OpenSSL | [OpenSSL logo.svg](https://commons.wikimedia.org/wiki/File:OpenSSL_logo.svg) | Public domain (logo) |
| `letsencrypt_logo.png` | Logo Let's Encrypt | [Lets Encrypt logo.svg](https://commons.wikimedia.org/wiki/File:Lets_Encrypt_logo.svg) | CC BY 4.0 |

Khôi phục các tệp trên:

```powershell
py -3 scripts\fetch_figure_assets.py
```

## Hình sơ đồ TikZ (tự tạo trong báo cáo)

| Label | Chương | Mô tả |
|---|---|---|
| `fig:mitm-vs-pki` | I | So sánh MITM và vai trò CA |
| `fig:pki-components` | III | Thành phần CA, RA, Repository, client |
| `fig:pki-validation-flow` | V | Kiểm tra chuỗi chứng chỉ (đã có) |
| `fig:pki-ecosystem` | VI | Phân lớp hệ sinh thái mã nguồn mở |
| `fig:ct-merkle` | VII | CT log và Merkle tree (đơn giản hóa) |

## Hình có sẵn từ tài liệu / slide môn học

| Tệp | Chương | Ghi chú |
|---|---|---|
| `EWPU.png`, `EWPR.png`, `EWB.png` | II | Mã hóa/giải mã bất đối xứng |
| `RSA.png`, `OAEP.png` | II | Thuật toán RSA và OAEP |
| `DH_protocol.png` | II | Trao đổi khóa Diffie–Hellman |
| `digitroll.png` | II | Mô hình chữ ký số |
| `digital_signature.png` | III | Quy trình chữ ký số |
| `cert_lifecycle.png` | III | Chu kỳ sống chứng chỉ |
| `soict.jpg` | Trang bìa | Logo SOICT |

> Nếu các hình slide không có nguồn công khai rõ ràng, nên thay dần bằng sơ đồ TikZ hoặc hình Wikimedia tương đương.

## Quy ước chèn hình trong LaTeX

- Đặt tệp raster trong `report/assets/`.
- Caption ghi nguồn ngắn: `(Nguồn: Wikimedia Commons, CC BY-SA)`.
- Luôn `\label{fig:...}` và trích dẫn trong prose **trước** khi float xuất hiện.
- Ưu tiên vector/TikZ cho sơ đồ; PNG ≥800px cho sơ đồ phức tạp từ Commons.
