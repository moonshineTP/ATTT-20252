# PKI – Hạ Tầng Khóa Công Khai: Tổng Quan

---

## 1. Vấn Đề Cần Giải Quyết

### 1.1 Bài Toán Phân Phối Và Xác Thực Khóa Công Khai

Mật mã khóa công khai giải quyết được bài toán trao đổi bí mật, chữ ký số — nhưng nảy sinh vấn đề mới:

> **"Khi A nhận khóa công khai của B, làm sao A biết đó THỰC SỰ là khóa của B, không phải của kẻ tấn công?"**

#### Tấn Công Man-in-the-Middle (MITM)
```
Bình thường:   Alice ←→ Bob
               Alice nhận KPB thật → giao tiếp an toàn

MITM:          Alice ←→ [Mallory] ←→ Bob
               Mallory gửi KP_Mallory cho Alice giả vờ là KPB
               Alice mã hóa bằng KP_Mallory → Mallory đọc được
               Mallory mã hóa lại bằng KPB → Bob không biết
```

#### Giải Pháp Cần Thiết
- Cần **bên thứ ba đáng tin cậy** xác nhận: "Khóa công khai này thuộc về đúng người đó"
- → **PKI (Public Key Infrastructure)** được tạo ra để giải quyết vấn đề này

### 1.2 Bốn Mô Hình Phân Phối Khóa Công Khai (Từ Giáo Trình)

| Mô hình | Mô tả | Điểm yếu |
|---|---|---|
| **Công bố công khai** | Bên tự công bố KP của mình | Dễ bị giả mạo |
| **Thư mục công khai** | Bên thứ 3 C quản lý thư mục KP | Nếu C bị tấn công, toàn bộ KP bị giả mạo |
| **Trung tâm ủy quyền (PKA)** | PKA xác thực mỗi giao dịch trao đổi KP | Phức tạp, PKA là điểm nút cổ chai |
| **Chứng chỉ số (Certificate)** | CA cấp chứng chỉ, bên tự quản lý | **→ Đây là nền tảng PKI** |

---

## 2. PKI Là Gì?

### 2.1 Định Nghĩa
**PKI (Public Key Infrastructure – Hạ tầng Khóa Công Khai)** là tổ hợp bao gồm:
- **Phần cứng, phần mềm, con người, chính sách và quy trình** cần thiết để:
  - Tạo, quản lý, phân phối, sử dụng, lưu trữ và **thu hồi (revoke)** chứng chỉ số
  - Quản lý mã hóa khóa công khai

### 2.2 Mục Tiêu Của PKI
1. **Xác thực (Authentication):** Xác nhận danh tính người dùng/thiết bị/tổ chức
2. **Bảo mật (Confidentiality):** Mã hóa dữ liệu trao đổi
3. **Toàn vẹn (Integrity):** Đảm bảo dữ liệu không bị thay đổi
4. **Không chối cãi (Non-repudiation):** Người gửi không thể phủ nhận đã gửi

### 2.3 Thành Phần Cốt Lõi Của PKI

```
┌─────────────────────────────────────────────────────────┐
│                       PKI                               │
│                                                         │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐ │
│  │  Root CA   │──→ │Intermediate  │──→ │  End-Entity │ │
│  │(Trust Anchor)│  │     CA       │    │ Certificate │ │
│  └────────────┘    └──────────────┘    └─────────────┘ │
│                                                         │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐ │
│  │    RA      │    │  Repository  │    │  CRL/OCSP   │ │
│  │(Reg Auth)  │    │  (LDAP/HTTP) │    │  (Revoke)   │ │
│  └────────────┘    └──────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Các Thành Phần Của PKI

### 3.1 CA – Certificate Authority (Tổ Chức Cấp Chứng Chỉ)

**CA** là trái tim của PKI — đơn vị đáng tin cậy có nhiệm vụ:
- **Phát hành (Issue)** chứng chỉ số cho các thực thể (người dùng, server, tổ chức)
- **Ký số (Sign)** chứng chỉ bằng khóa riêng của CA
- **Thu hồi (Revoke)** chứng chỉ khi cần (khóa riêng bị lộ, thông tin sai, hết hạn trước thời hạn)
- **Duy trì danh sách thu hồi CRL**

#### Phân Loại CA
| Loại | Mô tả |
|---|---|
| **Root CA** | CA gốc, tự ký (self-signed), là điểm tin cậy tối cao |
| **Intermediate CA** | CA cấp trung, được Root CA cấp chứng chỉ, cấp chứng chỉ cho CA con hoặc end-entity |
| **Leaf/End-Entity CA** | Cấp chứng chỉ trực tiếp cho người dùng/server cuối |

#### Quy Trình Cấp Chứng Chỉ Cơ Bản
```
1. End-Entity tạo cặp khóa (KP, KR)
2. Gửi yêu cầu CSR (Certificate Signing Request) tới CA
   CSR chứa: KP + thông tin định danh + chữ ký bằng KR
3. CA xác minh danh tính (qua RA hoặc trực tiếp)
4. CA ký CSR bằng khóa riêng của CA → tạo Chứng chỉ số
5. CA gửi Chứng chỉ cho End-Entity + đưa vào Repository
```

### 3.2 RA – Registration Authority (Tổ Chức Đăng Ký)

- **Trung gian** giữa người dùng và CA
- Nhận yêu cầu cấp chứng chỉ từ người dùng
- **Xác minh danh tính** người dùng (kiểm tra CMND, hộ chiếu, email...)
- Chuyển yêu cầu đã được xác minh cho CA
- **Không có quyền ký** chứng chỉ (chỉ CA mới có)

### 3.3 Repository – Kho Lưu Trữ Chứng Chỉ

- **LDAP Directory:** Kho lưu trữ chứng chỉ và CRL phổ biến nhất
- **HTTP/HTTPS Server:** Phục vụ chứng chỉ và CRL qua web
- **Chức năng:** Cho phép mọi người truy cập, tải chứng chỉ công khai và CRL

### 3.4 CRL – Certificate Revocation List (Danh Sách Thu Hồi)

Đôi khi chứng chỉ cần bị **thu hồi trước khi hết hạn** vì:
- Khóa riêng bị lộ
- CA bị xâm phạm
- Thông tin trong chứng chỉ không còn đúng
- Ngừng sử dụng

**CRL** là danh sách được CA ký của các chứng chỉ đã bị thu hồi, gồm:
- Serial number của chứng chỉ bị thu hồi
- Thời gian thu hồi
- Lý do thu hồi
- Chữ ký của CA

### 3.5 OCSP – Online Certificate Status Protocol

- **Thay thế/bổ sung** cho CRL
- Thay vì tải toàn bộ CRL (có thể rất lớn), client gửi yêu cầu kiểm tra từng chứng chỉ **theo thời gian thực**
- **OCSP Responder:** Server trả lời: `good` / `revoked` / `unknown`
- **OCSP Stapling:** Server đính kèm phản hồi OCSP vào TLS handshake (hiệu năng tốt hơn)

### 3.6 End-Entity (Thực Thể Cuối)

Là đối tượng được cấp chứng chỉ:
- **Người dùng:** Email certificate, smart card
- **Máy chủ:** SSL/TLS server certificate (HTTPS)
- **Thiết bị:** IoT devices, network equipment
- **Phần mềm:** Code signing certificate

---

## 4. Chứng Chỉ Số – Digital Certificate

### 4.1 Khái Niệm
Chứng chỉ số là **tài liệu điện tử** được CA ký, liên kết **danh tính** với **khóa công khai**:

```
Chứng chỉ = {Danh tính + Khóa công khai + Metadata} được ký bởi CA
```

### 4.2 Cơ Chế Tin Cậy

```
                    CA ký bằng KR_CA
                         ↓
Chứng chỉ của Bob: [ID_Bob + KP_Bob + ...]_Ký_KR_CA

Alice muốn xác thực:
1. Alice có KP_CA (đã được cài sẵn / biết trước)
2. Dùng KP_CA để xác minh chữ ký của CA trên chứng chỉ của Bob
3. Nếu hợp lệ → Alice tin tưởng KP_Bob thật sự thuộc về Bob
```

### 4.3 Nội Dung Chứng Chỉ Số (Sơ Đồ Từ Giáo Trình)
```
Chứng thư số chứa:
├── Số serial của chứng thư số
├── Thông tin riêng của người sở hữu (tên, tổ chức...)
├── Khóa công khai của người sở hữu
├── Chứng thực của CA: mã hóa bằng KR_CA
├── Thời hạn hiệu lực (Not Before / Not After)
├── Đảm bảo tính toàn vẹn (chữ ký)
└── Thuật toán mật mã được sử dụng
```

---

## 5. Chuẩn X.509

### 5.1 Giới Thiệu
- X.509 là **chuẩn ITU-T** cho chứng chỉ khóa công khai
- Phiên bản hiện tại: **X.509 v3** (RFC 5280)
- Được sử dụng rộng rãi trong HTTPS, S/MIME, VPN, code signing...

### 5.2 Cấu Trúc Chứng Chỉ X.509 v3

```
Certificate ::= {
  tbsCertificate:  {
    version:           v3 (2)
    serialNumber:      số serial duy nhất
    signature:         thuật toán ký (vd: sha256WithRSAEncryption)
    issuer:            tên CA cấp (DN: Distinguished Name)
    validity:          { notBefore, notAfter }
    subject:           tên chủ thể (DN)
    subjectPublicKeyInfo: {
      algorithm:       RSA / ECDSA / ...
      subjectPublicKey: giá trị khóa công khai
    }
    extensions:        {
      basicConstraints:       isCA? / pathLength
      keyUsage:              digitalSignature, keyEncipherment...
      extendedKeyUsage:      serverAuth, clientAuth, codeSigning...
      subjectAltName:        DNS names, IP addresses, email...
      cRLDistributionPoints: URL tải CRL
      authorityInfoAccess:   URL OCSP, URL cert CA cha
      subjectKeyIdentifier:  hash của KP
      authorityKeyIdentifier: hash của KP CA
    }
  }
  signatureAlgorithm: sha256WithRSAEncryption
  signature:          chữ ký số của CA
}
```

### 5.3 Distinguished Name (DN)
```
CN    = Common Name (vd: www.example.com)
O     = Organization (vd: Example Corp)
OU    = Organizational Unit
L     = Locality (thành phố)
ST    = State / Province
C     = Country (vd: VN)
```

### 5.4 Extensions Quan Trọng Trong X.509 v3

| Extension | Ý Nghĩa |
|---|---|
| `basicConstraints` | Xác định đây có phải CA hay không, độ sâu chuỗi chứng chỉ |
| `keyUsage` | Mục đích sử dụng khóa (ký, mã hóa, xác thực...) |
| `extendedKeyUsage` | Mục đích mở rộng (TLS server, client, code signing...) |
| `subjectAltName (SAN)` | Các tên thay thế (DNS, IP, email) — thay thế CN |
| `cRLDistributionPoints` | URL để tải CRL |
| `authorityInfoAccess` | URL dịch vụ OCSP và URL cert của CA cấp |

---

## 6. Mô Hình Tin Cậy PKI (Trust Models)

### 6.1 Mô Hình Phân Cấp (Hierarchical / Single Root)
```
          Root CA
         /       \
   Int CA      Int CA
   /   \        /   \
 Leaf  Leaf  Leaf  Leaf
```
- **Root CA** tự ký (self-signed)
- **Intermediate CA** giảm rủi ro: Root CA chỉ cần online để cấp cert cho Intermediate
- Root CA được **cài sẵn** trong hệ điều hành / trình duyệt (Mozilla, Microsoft, Apple list)
- **Xác minh chuỗi (Chain Validation):** Duyệt từ Leaf → Intermediate → Root

### 6.2 Mô Hình Mạng Tin Cậy (Web of Trust – PGP)
- Không có Root CA tập trung
- Người dùng ký chứng chỉ cho nhau
- Được sử dụng trong **PGP / GPG**
- Phụ thuộc vào "keyserver" và cộng đồng người dùng

### 6.3 Mô Hình Phân Cấp Chéo (Cross-Certification / Bridge CA)
```
Root CA A ←→ Bridge CA ←→ Root CA B
```
- Cho phép hai PKI domain khác nhau tin tưởng lẫn nhau
- Dùng trong liên kết PKI giữa các tổ chức / quốc gia

### 6.4 So Sánh

| Đặc điểm | Phân cấp | Web of Trust | Cross-Cert |
|---|---|---|---|
| Mô hình | Cây | Mạng lưới | Đồ thị |
| Tin cậy gốc | Root CA | Cộng đồng | Bridge CA |
| Ứng dụng | HTTPS, email công ty | PGP/Email cá nhân | Liên tổ chức |
| Quản lý | Tập trung | Phi tập trung | Chia sẻ |

---

## 7. Chu Kỳ Sống Của Chứng Chỉ

```
Tạo khóa → CSR → Xác minh → Cấp phát → Sử dụng → Gia hạn
                                                  ↓
                                              Thu hồi → CRL/OCSP
```

### Các Trạng Thái Của Chứng Chỉ
- **Valid (Hợp lệ):** Trong thời hạn, chưa bị thu hồi
- **Expired (Hết hạn):** Quá ngày Not After
- **Revoked (Bị thu hồi):** CA đã thu hồi, có trong CRL
- **Suspended (Tạm dừng):** Tạm thời thu hồi (ít dùng)
