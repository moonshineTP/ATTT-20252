# Chứng Chỉ Số X.509 – Chi Tiết Kỹ Thuật và Các Chuẩn Liên Quan

---

## 1. Lịch Sử Phát Triển X.509

| Phiên bản | Năm | Điểm mới |
|---|---|---|
| X.509 v1 | 1988 | Cấu trúc cơ bản: tên + khóa + chữ ký CA |
| X.509 v2 | 1993 | Thêm Subject/Issuer Unique Identifier |
| **X.509 v3** | **1996** | **Thêm Extensions — phiên bản phổ biến nhất hiện nay** |

Chuẩn IETF liên quan: **RFC 5280** (Internet X.509 PKI Certificate and CRL Profile)

---

## 2. Cấu Trúc X.509 v3 – Chi Tiết

### 2.1 Định Dạng ASN.1 / DER / PEM

Chứng chỉ X.509 được mã hóa theo chuẩn **ASN.1 (Abstract Syntax Notation One)**:
- **DER (Distinguished Encoding Rules):** Nhị phân — dùng trong Java, .NET
- **PEM (Privacy Enhanced Mail):** Base64 mã hóa DER — dùng trong Linux/OpenSSL
  - Bắt đầu: `-----BEGIN CERTIFICATE-----`
  - Kết thúc: `-----END CERTIFICATE-----`
- **PFX/PKCS#12 (.pfx, .p12):** Gói cả cert + private key + trust chain (có mật khẩu)
- **CER/DER (.cer, .crt):** Binary hoặc PEM

### 2.2 TBSCertificate – Phần Dữ Liệu Được Ký

```asn1
TBSCertificate ::= SEQUENCE {
  version         [0] EXPLICIT INTEGER DEFAULT v1,
  serialNumber          CertificateSerialNumber,
  signature             AlgorithmIdentifier,
  issuer                Name,
  validity              Validity,
  subject               Name,
  subjectPublicKeyInfo  SubjectPublicKeyInfo,
  issuerUniqueID  [1] IMPLICIT UniqueIdentifier OPTIONAL,  -- v2+
  subjectUniqueID [2] IMPLICIT UniqueIdentifier OPTIONAL,  -- v2+
  extensions      [3] EXPLICIT Extensions OPTIONAL         -- v3
}
```

### 2.3 Giải Thích Các Trường Quan Trọng

#### version
- `0` = v1, `1` = v2, `2` = v3
- Hầu hết chứng chỉ hiện tại là **v3**

#### serialNumber
- Số nguyên duy nhất do CA cấp
- Dùng trong CRL để xác định chứng chỉ bị thu hồi
- Phải ngẫu nhiên (≥64 bit) để tránh tấn công hash collision (RFC 5280)

#### signature (AlgorithmIdentifier)
Thuật toán sử dụng để ký TBSCertificate:
- `sha256WithRSAEncryption` (OID 1.2.840.113549.1.1.11) — phổ biến nhất
- `ecdsa-with-SHA256` (OID 1.2.840.10045.4.3.2) — nhanh hơn RSA
- `sha384WithRSAEncryption`, `ecdsa-with-SHA384`

#### issuer (Distinguished Name)
```
C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA
```

#### validity
```
notBefore: 2024-01-01T00:00:00Z
notAfter:  2025-01-01T23:59:59Z
```
- Thời hạn tối đa: 398 ngày (kể từ 2020, Apple/Chrome yêu cầu)

#### subject (Distinguished Name)
```
CN=www.example.com, O=Example Corp, L=Hanoi, ST=HN, C=VN
```

#### subjectPublicKeyInfo
```
algorithm: rsaEncryption (1.2.840.113549.1.1.1)
publicKey: 2048-bit RSA key
```

---

## 3. Extensions X.509 v3 – Các Trường Mở Rộng

### 3.1 Basic Constraints (critical)
```
basicConstraints: {
  cA: TRUE/FALSE,
  pathLenConstraint: INTEGER  -- tối đa bao nhiêu CA con
}
```
- `cA=TRUE`: Đây là chứng chỉ CA
- `cA=FALSE`: Đây là chứng chỉ end-entity
- **Phải là critical** để tránh tấn công CA impersonation

### 3.2 Key Usage (critical)
Tập hợp các bit xác định mục đích sử dụng khóa:
| Bit | Tên | Ý nghĩa |
|---|---|---|
| 0 | digitalSignature | Ký số (TLS, email) |
| 1 | nonRepudiation | Không chối cãi |
| 2 | keyEncipherment | Mã hóa khóa phiên (RSA key exchange) |
| 3 | dataEncipherment | Mã hóa trực tiếp dữ liệu |
| 4 | keyAgreement | Thỏa thuận khóa (DH/ECDH) |
| 5 | keyCertSign | Ký chứng chỉ (dành cho CA) |
| 6 | cRLSign | Ký CRL |
| 7 | encipherOnly | Chỉ mã hóa (với keyAgreement) |
| 8 | decipherOnly | Chỉ giải mã (với keyAgreement) |

### 3.3 Extended Key Usage (EKU)
Xác định ứng dụng cụ thể hơn:
| OID | Tên | Dùng trong |
|---|---|---|
| 1.3.6.1.5.5.7.3.1 | serverAuth | TLS server (HTTPS) |
| 1.3.6.1.5.5.7.3.2 | clientAuth | TLS client authentication |
| 1.3.6.1.5.5.7.3.3 | codeSigning | Ký phần mềm |
| 1.3.6.1.5.5.7.3.4 | emailProtection | S/MIME email |
| 1.3.6.1.5.5.7.3.8 | timeStamping | Dịch vụ đóng dấu thời gian |
| 1.3.6.1.5.5.7.3.9 | OCSPSigning | Ký phản hồi OCSP |

### 3.4 Subject Alternative Name (SAN)
```
subjectAltName: {
  DNS: www.example.com
  DNS: example.com
  DNS: *.example.com    -- Wildcard certificate
  IP:  192.168.1.1
  email: admin@example.com
}
```
- **Bắt buộc** từ Chrome 58+ (2017): CN không còn được dùng để xác thực domain
- Wildcard `*.example.com` chỉ bao gồm **một cấp subdomain**

### 3.5 CRL Distribution Points
```
cRLDistributionPoints: {
  http://crl.example.com/ca.crl
  ldap://ldap.example.com/cn=crl,...
}
```

### 3.6 Authority Information Access (AIA)
```
authorityInfoAccess: {
  OCSP: http://ocsp.example.com
  caIssuers: http://certs.example.com/ca.cer
}
```

### 3.7 Subject/Authority Key Identifier
- `subjectKeyIdentifier`: SHA-1 hash của khóa công khai chủ thể
- `authorityKeyIdentifier`: Để xác định CA ký chứng chỉ này

---

## 4. Certificate Signing Request (CSR)

### 4.1 Định Nghĩa
CSR là tài liệu người dùng/server gửi cho CA để xin chứng chỉ:

```
CSR chứa:
├── Subject (tên, tổ chức, domain...)
├── Khóa công khai (KP)
├── Chữ ký bằng khóa riêng (KR) — chứng minh sở hữu KR
└── Các thuộc tính bổ sung
```

### 4.2 Tạo CSR Bằng OpenSSL
```bash
# Tạo khóa RSA 2048-bit
openssl genrsa -out server.key 2048

# Tạo CSR
openssl req -new -key server.key -out server.csr \
  -subj "/C=VN/ST=HN/L=Hanoi/O=Example/CN=www.example.com"

# Xem nội dung CSR
openssl req -text -noout -in server.csr
```

---

## 5. Các Loại Chứng Chỉ SSL/TLS

### 5.1 Phân Loại Theo Mức Độ Xác Minh

| Loại | Tên | Mức xác minh | Thời gian cấp |
|---|---|---|---|
| **DV** | Domain Validated | Chỉ kiểm soát domain (email/DNS/file) | Phút |
| **OV** | Organization Validated | Kiểm tra tổ chức hợp lệ | 1-3 ngày |
| **EV** | Extended Validation | Kiểm tra đầy đủ pháp lý (CAB Forum) | 1-2 tuần |

- **DV:** Dùng cho websites thông thường, blog
- **OV:** Dùng cho công ty, cơ quan nhà nước
- **EV:** Dùng cho ngân hàng, giao dịch tài chính (trước 2019 hiển thị green bar)

### 5.2 Phân Loại Theo Số Lượng Domain

| Loại | Mô tả |
|---|---|
| **Single Domain** | Chỉ cho 1 domain (example.com) |
| **Wildcard** | Bao gồm 1 cấp subdomains (*.example.com) |
| **Multi-Domain (SAN/UCC)** | Nhiều domain khác nhau trong 1 cert |

---

## 6. Certificate Revocation – Thu Hồi Chứng Chỉ

### 6.1 CRL (Certificate Revocation List)

Cấu trúc CRL theo RFC 5280:
```
CertificateList ::= {
  tbsCertList: {
    version:            v2
    signature:          sha256WithRSAEncryption
    issuer:             tên CA
    thisUpdate:         thời gian tạo CRL
    nextUpdate:         thời gian CRL tiếp theo
    revokedCertificates: [
      {
        userCertificate:  serial 12345
        revocationDate:   2024-06-01
        crlEntryExtensions: {
          reasonCode: keyCompromise (1)
        }
      },
      ...
    ]
    crlExtensions: { authorityKeyIdentifier, cRLNumber }
  }
  signatureAlgorithm: sha256WithRSAEncryption
  signature: ...
}
```

#### Reason Codes (Lý Do Thu Hồi)
| Code | Tên | Mô tả |
|---|---|---|
| 0 | unspecified | Không xác định |
| 1 | keyCompromise | Khóa riêng bị lộ |
| 2 | cACompromise | CA bị xâm phạm |
| 3 | affiliationChanged | Thay đổi tổ chức |
| 4 | superseded | Được thay thế bởi cert mới |
| 5 | cessationOfOperation | Ngừng hoạt động |
| 6 | certificateHold | Tạm dừng |
| 9 | privilegeWithdrawn | Thu hồi quyền |

### 6.2 OCSP (Online Certificate Status Protocol – RFC 6960)

```
Client                    OCSP Responder
  │                              │
  │── OCSPRequest ──────────────→│
  │   (serialNumber)             │
  │                              │
  │←─ OCSPResponse ─────────────│
  │   (good/revoked/unknown      │
  │    + timestamp + signature)  │
```

**OCSP Stapling (RFC 6066):**
- Server định kỳ lấy phản hồi OCSP từ CA và **đính kèm** vào TLS handshake
- Client nhận phản hồi OCSP từ server → không cần gọi CA trực tiếp
- Cải thiện hiệu năng và bảo mật (không rò rỉ danh sách websites người dùng truy cập tới CA)

---

## 7. Các Chuẩn PKCS Liên Quan

| Chuẩn | Tên | Nội dung |
|---|---|---|
| PKCS#1 | RSA Cryptography Standard | Định dạng RSA key |
| PKCS#7 / CMS | Cryptographic Message Syntax | Định dạng dữ liệu ký (S/MIME) |
| PKCS#10 | CSR | Chuẩn CSR (yêu cầu cấp chứng chỉ) |
| **PKCS#11** | Cryptoki | Giao diện token mật mã (HSM, smart card) |
| **PKCS#12** | PFX | Gói chứng chỉ + khóa riêng (binary) |
| PKCS#8 | Private-Key Info | Định dạng lưu khóa riêng |

---

## 8. Các RFC Quan Trọng Về PKI

| RFC | Nội dung |
|---|---|
| RFC 5280 | X.509 PKI Certificate and CRL Profile |
| RFC 6960 | OCSP – Online Certificate Status Protocol |
| RFC 5652 | CMS – Cryptographic Message Syntax |
| RFC 4210 | CMP – Certificate Management Protocol |
| RFC 5958 | PKCS#8 – Private Key Information Syntax |
| RFC 7468 | PEM encoding |
| RFC 8555 | ACME Protocol (Let's Encrypt) |
