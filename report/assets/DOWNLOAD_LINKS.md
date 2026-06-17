# Ảnh trong `report/assets/`

## Không cần tải thêm ảnh từ Internet

Báo cáo đã dùng **sơ đồ TikZ** (vector, không méo) cho các chương I, III–VII.
Chỉ còn **ảnh slide môn học** ở chương II — đã có sẵn trong thư mục này.

## File hiện có (đủ để build)

| File | Dùng ở |
|---|---|
| `soict.jpg` | Trang bìa |
| `EWPU.png`, `EWPR.png`, `EWB.png` | Chương II |
| `RSA.png`, `OAEP.png`, `DH_protocol.png`, `digitroll.png` | Chương II |

Các file `digital_signature.png`, `cert_lifecycle.png` **không còn bắt buộc**
(đã thay bằng TikZ). Có thể xóa hoặc giữ làm tài liệu tham khảo.

## Nếu muốn thay ảnh slide chương II

1. Export PNG từ slide giáo trình (Stallings / slide môn học).
2. **Giữ đúng tên file** như bảng trên.
3. Copy vào `report/assets/`.
4. Chạy `report\build.bat`.

LaTeX scale theo **một chiều** (`keepaspectratio`) — không kéo giãn.

## Link Wikimedia (tùy chọn, không bắt buộc)

Link PNG trực tiếp trước đây hay bị chặn (429). Nếu vẫn muốn ảnh ngoài:

1. Mở trang Commons (ví dụ https://commons.wikimedia.org/wiki/File:Public_key_infrastructure.svg)
2. Bấm **Download** trên trang web (không dán link thumb vào trình duyệt)
3. Đổi tên và tự chèn bằng `\slidefig{tên_file.png}` trong `.tex`

Chi tiết giấy phép: `SOURCES.md`.
