# Ứng Dụng PKI Trong Thực Tế

---

## 1. HTTPS / TLS – Bảo Mật Web

### 1.1 Tổng Quan TLS/SSL
- **SSL (Secure Sockets Layer):** Phiên bản cũ — SSL 2.0 (1995), 3.0 (1996) — đã bị lỗi thời
- **TLS (Transport Layer Security):** Kế thừa SSL — TLS 1.0, 1.1, 1.2, **1.3 (2018)**
- TLS 1.0 và 1.1 **đã bị deprecated** từ 2021 (RFC 8996)
- **TLS 1.3** hiện là chuẩn mới nhất, loại bỏ nhiều thuật toán yếu

### 1.2 TLS Handshake (TLS 1.2)
```
Client                              Server
  │                                    │
  │──── ClientHello ──────────────────→│
  │     (TLS versions, ciphers,        │
  │      random, extensions)           │
  │                                    │
  │←─── ServerHello ──────────────────│
  │     (selected cipher, random)      │
  │←─── Certificate ──────────────────│  ← Chứng chỉ X.509 của server
  │←─── ServerHelloDone ──────────────│
  │                                    │
  │  [Client xác minh chứng chỉ:       │
  │   - Kiểm tra chain of trust        │
  │   - Kiểm tra thời hạn              │
  │   - Kiểm tra CRL/OCSP              │
  │   - Kiểm tra hostname (SAN)]       │
  │                                    │
  │──── ClientKeyExchange ────────────→│  ← pre-master secret (RSA encrypt)
  │──── ChangeCipherSpec ─────────────→│
  │──── Finished ─────────────────────→│
  │←─── ChangeCipherSpec ─────────────│
  │←─── Finished ─────────────────────│
  │                                    │
  │════ Application Data (mã hóa) ════│
```

### 1.3 TLS 1.3 Cải Tiến
- **0-RTT / 1-RTT:** Rút ngắn handshake (chỉ 1 round-trip)
- Loại bỏ RSA key exchange → **chỉ dùng ECDHE** (Forward Secrecy)
- Loại bỏ: MD5, SHA-1, RC4, DES, 3DES, CBC mode
- **Perfect Forward Secrecy (PFS):** Mỗi phiên dùng khóa phiên khác nhau → lộ khóa dài hạn không ảnh hưởng phiên cũ

### 1.4 Xác Minh Chứng Chỉ Trong TLS
Khi trình duyệt kết nối HTTPS, nó kiểm tra:
1. **Chữ ký CA hợp lệ** (xây dựng và xác minh chuỗi tới Root CA)
2. **Thời hạn** (`notBefore` ≤ now ≤ `notAfter`)
3. **Domain khớp** (CN hoặc SAN phải khớp với hostname)
4. **Chứng chỉ không bị thu hồi** (OCSP / CRL check)
5. **Root CA có trong trust store** (danh sách do OS/browser quản lý)

### 1.5 Wildcard & Multi-Domain
```
Wildcard:    *.example.com  → bao gồm a.example.com, b.example.com
                             KHÔNG bao gồm a.b.example.com

Multi-SAN:   SAN: example.com
                  www.example.com
                  api.example.com
                  example.vn
```

---

## 2. Chữ Ký Số Điện Tử

### 2.1 Nguyên Lý Chữ Ký Số
```
Ký văn bản:
  1. Hash(văn bản) → H (vd: SHA-256)
  2. Encrypt(H, KR_sender) → Chữ ký số S
  3. Gửi: {văn bản + S + Chứng chỉ của sender}

Xác minh:
  1. Decrypt(S, KP_sender) → H'
  2. Hash(văn bản) → H
  3. Nếu H = H' → chữ ký hợp lệ
  4. Kiểm tra chứng chỉ của sender (via PKI chain)
```

### 2.2 Khung Pháp Lý Việt Nam
- **Luật Giao dịch điện tử 2005** (Luật số 51/2005/QH11)
- **Luật Giao dịch điện tử 2023** (Luật số 20/2023/QH15, hiệu lực 1/7/2024)
- **Nghị định 130/2018/NĐ-CP:** Quy định chi tiết về chữ ký số, chứng thư số
- **Nghị định 13/2023/NĐ-CP:** Bảo vệ dữ liệu cá nhân

#### Các Tổ Chức Cung Cấp Dịch Vụ CA Ở Việt Nam
| Tên | Loại |
|---|---|
| NEAC (Ban Cơ yếu Chính phủ - rootCA) | Root CA Nhà nước |
| VNPT-CA | CA Doanh nghiệp |
| Viettel-CA | CA Doanh nghiệp |
| BKAV-CA | CA Doanh nghiệp |
| FPT-CA | CA Doanh nghiệp |
| New CA (MoIT) | CA Nhà nước |

### 2.3 Quy Trình Ký Số Văn Bản Hành Chính
```
Tổ chức A                CA Nhà nước          Tổ chức B (nhận)
    │                        │                      │
    │── Đăng ký, xác thực ──→│                      │
    │← Chứng thư số ─────────│                      │
    │                                               │
    │── Ký văn bản bằng KR ─────────────────────────│
    │   (kèm chứng thư số)                          │
    │                                               │
    │                        │← Kiểm tra chứng thư │
    │                        │   (chain, CRL/OCSP)  │
    │                        │→ Hợp lệ/Không hợp −│
```

---

## 3. S/MIME – Bảo Mật Email

### 3.1 S/MIME (Secure/Multipurpose Internet Mail Extensions)
- Chuẩn **RFC 8551** (trước là RFC 5751)
- Sử dụng **chứng chỉ X.509** cho ký số và mã hóa email
- Tích hợp trong: Microsoft Outlook, Apple Mail, Thunderbird

### 3.2 Chức Năng
| Chức năng | Mô tả |
|---|---|
| **Ký số (Signing)** | Xác thực người gửi, đảm bảo toàn vẹn nội dung |
| **Mã hóa (Encryption)** | Chỉ người nhận mới đọc được |
| **Ký + Mã hóa** | Kết hợp cả hai |

### 3.3 Quy Trình S/MIME Mã Hóa Email
```
Alice (gửi):
  1. Tạo khóa phiên ngẫu nhiên Ks
  2. Mã hóa email bằng Ks (AES-256)
  3. Mã hóa Ks bằng KP_Bob (RSA)
  4. Gửi: {Email mã hóa + Ks mã hóa + Cert Alice}

Bob (nhận):
  1. Giải mã Ks bằng KR_Bob
  2. Giải mã email bằng Ks
  3. Xác minh chứng chỉ Alice (nếu có ký)
```

---

## 4. VPN – Mạng Riêng Ảo

### 4.1 IPSec VPN
- **IPSec** sử dụng **IKE (Internet Key Exchange)** để thiết lập SA (Security Association)
- **IKEv2** sử dụng chứng chỉ X.509 để xác thực hai bên
- PKI cấp chứng chỉ cho cả VPN gateway và VPN clients

```
VPN Client                    VPN Gateway
    │                               │
    │── IKE Init (Certificate) ────→│
    │   (cert client, KP_Client)    │
    │←─ IKE Auth (Certificate) ────│
    │   (cert gateway, KP_GW)       │
    │  [Xác minh chứng chỉ qua PKI] │
    │══ Tunnel được thiết lập ══════│
    │   (IPSec ESP/AH)              │
```

### 4.2 SSL/TLS VPN (OpenVPN, WireGuard)
- **OpenVPN:** Sử dụng OpenSSL, hỗ trợ đầy đủ PKI (CA, cert, CRL)
- **WireGuard:** Dùng public key trực tiếp (không dùng X.509 certificate)

---

## 5. Code Signing – Ký Phần Mềm

### 5.1 Mục Đích
- Xác thực nhà phát hành phần mềm
- Đảm bảo phần mềm không bị sửa đổi sau khi ký
- Windows SmartScreen, macOS Gatekeeper, Android APK signing

### 5.2 Quy Trình
```
1. Nhà phát triển nhận Code Signing Certificate (OV hoặc EV)
2. Ký file thực thi (exe, dll, apk, pkg...)
3. Kèm timestamp signature (chứng minh ký trước khi cert hết hạn)
4. OS/Platform xác minh chữ ký khi cài đặt
```

### 5.3 EV Code Signing
- **Extended Validation** cho code signing
- Yêu cầu xác minh pháp lý tổ chức nghiêm ngặt
- Trên Windows: bỏ qua cảnh báo SmartScreen ngay lập tức

---

## 6. PKI Trong Giao Dịch Điện Tử

### 6.1 SET (Secure Electronic Transaction)
- Chuẩn giao thức cũ do Visa + Mastercard phát triển
- Sử dụng PKI để xác thực cả **merchant** và **cardholder**
- Đã lỗi thời, thay bằng 3-D Secure, tokenization

### 6.2 3-D Secure (3DS2)
- Xác thực thẻ qua OTP, biometrics
- Kết hợp với TLS (PKI) để bảo vệ kênh truyền

### 6.3 eIDAS (Electronic Identification, Authentication and Trust Services)
- Quy định EU số 910/2014 về định danh điện tử
- Quy định **Qualified Electronic Signature (QES)** — tương đương chữ ký tay
- PKI là nền tảng kỹ thuật cho QES

### 6.4 Ứng Dụng Trong Banking/Finance
| Ứng dụng | Vai trò PKI |
|---|---|
| Internet Banking | TLS/HTTPS + xác thực 2 chiều |
| Ký hợp đồng điện tử | Chữ ký số X.509 |
| E-invoicing (hóa đơn điện tử) | Ký số + timestamp |
| Swift messaging | PKI cho xác thực tổ chức tài chính |

---

## 7. PKI Cho IoT và Thiết Bị Nhúng

### 7.1 Thách Thức
- Hàng triệu thiết bị → quản lý chứng chỉ phức tạp
- Tài nguyên giới hạn (CPU, RAM, storage)
- Vòng đời thiết bị dài → chứng chỉ cần gia hạn tự động

### 7.2 Giải Pháp
- **Lightweight certificates** (ECC thay vì RSA)
- **EST (Enrollment over Secure Transport – RFC 7030):** Tự động cấp phát cert
- **SCEP (Simple Certificate Enrollment Protocol):** Dùng trong Cisco, network devices
- **Device onboarding protocols:** IEEE 802.1AR (DevID)

---

## 8. PKI Trong Hệ Thống Quốc Gia Việt Nam

### 8.1 Kiến Trúc PKI Quốc Gia Việt Nam
```
NEAC Root CA (Ban Cơ yếu Chính phủ)
         │
         ├── Sub-CA Chính phủ
         │        └── CA Bộ, Ngành, UBND
         │
         ├── Sub-CA Doanh nghiệp
         │        └── VNPT-CA, Viettel-CA, BKAV-CA...
         │
         └── Sub-CA Cá nhân
```

### 8.2 Ứng Dụng Thực Tế
- **Cổng dịch vụ công quốc gia** (dichvucong.gov.vn): Ký số văn bản hành chính
- **Hóa đơn điện tử:** Bắt buộc từ 2022 (Nghị định 123/2020)
- **Hải quan điện tử (VNACCS):** Khai báo hải quan điện tử
- **Đấu thầu qua mạng (MUASAMCONG):** Ký số hồ sơ thầu
- **Thuế điện tử (eTax):** Nộp thuế và khai thuế điện tử
