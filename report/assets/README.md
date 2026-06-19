# Ảnh minh họa — `report/assets/`

## Tạo / cập nhật sơ đồ (khuyến nghị)

Chạy script sinh PNG căn chỉnh sẵn (không cần Internet):

```powershell
cd "D:\LapTrinh\System\ATTT-20252"
C:\Users\ADMIN\miniconda3\python.exe scripts\generate_figure_assets.py
cd report
.\build.bat
```

Script tạo các file `fig_*.png` — LaTeX chỉ `\includegraphics`, **không dùng TikZ** trong báo cáo.

| File | Nội dung |
|---|---|
| `fig_mitm.png` | Tấn công MITM |
| `fig_pki_ca.png` | CA ràng buộc danh tính |
| `fig_pki_hierarchy.png` | Phân cấp PKI |
| `fig_digital_signature.png` | Chữ ký số |
| `fig_pki_components.png` | Thành phần PKI |
| `fig_cert_lifecycle.png` | Vòng đời chứng chỉ |
| `fig_x509.png` | Cấu trúc X.509 |
| `fig_tls_handshake.png` | Bắt tay TLS |
| `fig_pki_validation.png` | Kiểm tra chuỗi cert |
| `fig_ct.png` | Certificate Transparency |
| `fig_pki_ecosystem.png` | Hệ sinh thái mã nguồn mở |

## Ảnh slide chương II (giáo trình)

| File | Nội dung |
|---|---|
| `EWPU.png`, `EWPR.png`, `EWB.png` | Ba kịch bản khóa bất đối xứng |
| `RSA.png`, `OAEP.png`, `DH_protocol.png`, `digitroll.png` | RSA, OAEP, DH, ký số |

| `soict.jpg` | Logo trang bìa |

Muốn chỉnh sơ đồ: sửa `scripts/generate_figure_assets.py` rồi chạy lại script.
