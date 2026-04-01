# Các Hệ Thống PKI Mã Nguồn Mở

---

## 1. OpenSSL

### 1.1 Giới Thiệu
- Thư viện mật mã và PKI phổ biến nhất thế giới
- Mã nguồn mở, viết bằng C
- Hỗ trợ: TLS/SSL, chứng chỉ X.509, RSA, ECDSA, AES, SHA...
- Website: https://www.openssl.org
- Giấy phép: Apache License 2.0 (từ phiên bản 3.0)

### 1.2 Kiến Trúc OpenSSL
```
┌─────────────────────────────────────┐
│           Ứng dụng / Tools         │
├─────────────────────────────────────┤
│         OpenSSL CLI (openssl)       │
├───────────────────┬─────────────────┤
│   libssl (TLS)    │  libcrypto      │
│   TLS 1.0–1.3     │  RSA, ECDSA     │
│   Protocol layer  │  AES, SHA, X.509│
│                   │  PKCS#*         │
└───────────────────┴─────────────────┘
```

### 1.3 OpenSSL Làm CA Đơn Giản

#### Tạo Root CA
```bash
# 1. Tạo thư mục cấu trúc CA
mkdir -p /root/ca/{certs,crl,newcerts,private}
chmod 700 /root/ca/private
echo 1000 > /root/ca/serial
touch /root/ca/index.txt

# 2. Tạo khóa riêng Root CA (4096 bit, mã hóa AES256)
openssl genrsa -aes256 -out /root/ca/private/ca.key.pem 4096
chmod 400 /root/ca/private/ca.key.pem

# 3. Tạo chứng chỉ Root CA tự ký (10 năm)
openssl req -config openssl.cnf \
  -key /root/ca/private/ca.key.pem \
  -new -x509 -days 3650 -sha256 -extensions v3_ca \
  -out /root/ca/certs/ca.cert.pem \
  -subj "/C=VN/O=My PKI Lab/CN=My Root CA"
```

#### Tạo Intermediate CA
```bash
# 1. Tạo khóa riêng Intermediate CA
openssl genrsa -aes256 -out intermediate/private/intermediate.key.pem 4096

# 2. Tạo CSR
openssl req -config intermediate/openssl.cnf -new -sha256 \
  -key intermediate/private/intermediate.key.pem \
  -out intermediate/csr/intermediate.csr.pem

# 3. Root CA ký CSR của Intermediate CA
openssl ca -config openssl.cnf -extensions v3_intermediate_ca \
  -days 1825 -notext -md sha256 \
  -in intermediate/csr/intermediate.csr.pem \
  -out intermediate/certs/intermediate.cert.pem
```

#### Cấp Chứng Chỉ Server
```bash
# 1. Tạo khóa riêng server
openssl genrsa -out server.key.pem 2048

# 2. Tạo CSR
openssl req -config openssl.cnf -key server.key.pem \
  -new -sha256 -out server.csr.pem \
  -subj "/C=VN/O=Example/CN=www.example.com"

# 3. Intermediate CA ký chứng chỉ server
openssl ca -config intermediate/openssl.cnf -extensions server_cert \
  -days 397 -notext -md sha256 \
  -in server.csr.pem -out server.cert.pem

# 4. Kiểm tra
openssl x509 -noout -text -in server.cert.pem
openssl verify -CAfile chain.pem server.cert.pem
```

### 1.4 Các Lệnh OpenSSL Thường Dùng

```bash
# Xem thông tin chứng chỉ
openssl x509 -in cert.pem -text -noout

# Kiểm tra kết nối TLS
openssl s_client -connect example.com:443 -showcerts

# Tạo self-signed certificate (nhanh)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
  -days 365 -nodes -subj "/CN=localhost"

# Convert PEM ↔ DER
openssl x509 -in cert.pem -outform DER -out cert.der
openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem

# Tạo PKCS#12 (PFX)
openssl pkcs12 -export -out cert.pfx -inkey key.pem \
  -in cert.pem -certfile chain.pem

# Kiểm tra CRL
openssl crl -in crl.pem -text -noout

# Tạo và ký OCSP response (giả lập)
openssl ocsp -port 9080 -index index.txt -CA ca.pem \
  -rkey ocsp.key -rsigner ocsp.crt
```

---

## 2. EJBCA (Enterprise JavaBeans Certificate Authority)

### 2.1 Giới Thiệu
- PKI đầy đủ tính năng dành cho doanh nghiệp, viết bằng Java
- Mã nguồn mở (LGPL), phiên bản Enterprise thương mại bởi PrimeKey
- Website: https://www.ejbca.org
- Hỗ trợ: X.509, CRL, OCSP, SCEP, EST, CMP, Kerberos

### 2.2 Kiến Trúc EJBCA
```
┌──────────────────────────────────────────────────┐
│                EJBCA                             │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Web UI  │  │  REST    │  │   CLI        │  │
│  │(Admin/RA)│  │  API     │  │ (ejbca.sh)   │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │           Core CA Engine                    │ │
│  │  CertificateFactory, CRLFactory,            │ │
│  │  KeyManagement, PolicyEnforcement           │ │
│  └─────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Database │  │   HSM    │  │   OCSP       │  │
│  │(MariaDB) │  │  PKCS#11 │  │  Responder   │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└──────────────────────────────────────────────────┘
```

### 2.3 Tính Năng Nổi Bật
- **Multi-CA:** Quản lý nhiều CA (Root, Intermediate, Cross-CA)
- **HSM Support:** Tích hợp Hardware Security Module (Luna SA, Thales...)
- **RA Module:** Quản lý đăng ký đầy đủ
- **Publisher:** Xuất bản cert/CRL tới LDAP, OCSP, database
- **Audit Logging:** Ghi nhật ký đầy đủ theo chuẩn
- **Role-based Access Control**
- **ACME Protocol** (Let's Encrypt compatible)

### 2.4 Triển Khai EJBCA Bằng Docker
```bash
# Chạy EJBCA Community với Docker
docker run -it --rm \
  -p 8080:8080 -p 8443:8443 \
  keyfactor/ejbca-ce

# Truy cập: https://localhost:8443/ejbca/adminweb
```

---

## 3. Let's Encrypt

### 3.1 Giới Thiệu
- CA miễn phí, tự động, mở — do **ISRG (Internet Security Research Group)**
- Ra mắt 2016, hiện cấp hơn **3 tỷ chứng chỉ**
- Tự động hóa hoàn toàn qua **ACME Protocol (RFC 8555)**
- Chỉ cấp **DV (Domain Validated)** certificates

### 3.2 ACME Protocol (Automated Certificate Management Environment)
```
Client (Certbot)          Let's Encrypt ACME Server
     │                              │
     │── POST /newAccount ─────────→│  Tạo tài khoản ACME
     │← response (accountURL) ──────│
     │                              │
     │── POST /newOrder ───────────→│  Yêu cầu cert cho domain
     │← {authorizations, finalize} ─│
     │                              │
     │── GET /authorization ───────→│  Lấy challenge
     │← {challenge: http-01/dns-01} │
     │                              │
     │  [Client thực hiện challenge] │
     │── POST /challenge ──────────→│  Thông báo đã sẵn sàng
     │← {status: valid} ────────────│
     │                              │
     │── POST /finalize (CSR) ─────→│  Gửi CSR
     │← {certificate URL} ──────────│
     │                              │
     │── GET /certificate ─────────→│  Tải chứng chỉ
     │← cert + chain ───────────────│
```

### 3.3 Các Loại Challenge
| Challenge | Mô tả | Yêu cầu |
|---|---|---|
| **http-01** | Đặt file tại `/.well-known/acme-challenge/` | Port 80 accessible |
| **dns-01** | Thêm TXT record vào DNS | Quyền quản lý DNS |
| **tls-alpn-01** | Xác minh qua TLS | Port 443 accessible |

### 3.4 Certbot – Tự Động Hóa Let's Encrypt
```bash
# Cài đặt Certbot
sudo apt install certbot python3-certbot-nginx

# Cấp chứng chỉ Nginx tự động
sudo certbot --nginx -d example.com -d www.example.com

# Gia hạn tự động (cron)
sudo certbot renew --dry-run

# Cấp cert manual (dns-01)
sudo certbot certonly --manual --preferred-challenges dns \
  -d *.example.com
```

### 3.5 Let's Encrypt Trust Chain
```
ISRG Root X1 (RSA 4096)
    └── R3 (Intermediate CA, RSA 2048)
            └── *.example.com (end-entity)

ISRG Root X2 (ECDSA P-384) — backup root
    └── E1 (Intermediate CA, ECDSA P-384)
```

---

## 4. Dogtag / FreeIPA PKI

### 4.1 Dogtag Certificate System
- PKI đầy đủ do Red Hat/Fedora phát triển
- Là thành phần PKI trong **FreeIPA** (Identity, Policy, Audit)
- Mã nguồn mở (GPL)
- Website: https://www.dogtagpki.org

### 4.2 FreeIPA – Identity Management Tích Hợp PKI
```
FreeIPA = LDAP + Kerberos + DNS + PKI (Dogtag)
                                       │
                               Cấp cert cho:
                               - Users (email cert)
                               - Hosts (TLS cert)
                               - Services
```

### 4.3 Cài Đặt FreeIPA Server
```bash
# Trên RHEL/CentOS/Rocky Linux
sudo dnf install freeipa-server
sudo ipa-server-install \
  --domain=example.com \
  --realm=EXAMPLE.COM \
  --ds-password=xxx \
  --admin-password=yyy

# Thêm host và cấp certificate
ipa host-add web01.example.com
ipa-getcert request -k /etc/ipa/cert.key -f /etc/ipa/cert.crt \
  -N CN=web01.example.com
```

---

## 5. Vault by HashiCorp – PKI Secrets Engine

### 5.1 Giới Thiệu
- Vault là công cụ quản lý bí mật (secrets) của HashiCorp
- **PKI Secrets Engine**: Tích hợp CA đầy đủ vào Vault
- Ưu điểm: Tích hợp tốt với hạ tầng cloud (Kubernetes, AWS, GCP)

### 5.2 Sử Dụng Vault PKI
```bash
# Kích hoạt PKI engine
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

# Tạo Root CA
vault write -field=certificate pki/root/generate/internal \
  common_name="My Root CA" ttl=87600h > root_CA.crt

# Tạo Intermediate CA
vault secrets enable -path=pki_int pki
vault write pki_int/intermediate/generate/internal \
  common_name="My Int CA" | jq -r '.data.csr' > int_ca.csr
vault write pki/root/sign-intermediate csr=@int_ca.csr \
  format=pem_bundle | jq -r '.data.certificate' > intermediate.cert.pem
vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem

# Tạo role và cấp cert
vault write pki_int/roles/example-dot-com \
  allowed_domains="example.com" allow_subdomains=true max_ttl="720h"
vault write pki_int/issue/example-dot-com \
  common_name="www.example.com"
```

---

## 6. XCA – X Certificate and Key Management (GUI)

### 6.1 Giới Thiệu
- Ứng dụng GUI mã nguồn mở để quản lý CA, certs, keys
- Chạy trên Windows, Linux, macOS
- Lưu toàn bộ vào file database SQLite
- Phù hợp để học/test, lab PKI
- Download: https://hohnstaedt.de/xca

### 6.2 Tính Năng
- Tạo Root CA, Intermediate CA, end-entity certificates
- Import/Export PEM, DER, PKCS#12
- Hỗ trợ RSA, DSA, ECDSA
- Template cho các loại cert (TLS server, S/MIME, code signing...)

---

## 7. CFSSL – Cloudflare's PKI Toolkit

### 7.1 Giới Thiệu
- Viết bằng Go, dễ nhúng vào hệ thống
- CLI và REST API
- Phù hợp cho microservices, Kubernetes internal PKI

```bash
# Tạo Root CA
cfssl gencert -initca csr.json | cfssljson -bare ca

# Cấp chứng chỉ server
cfssl gencert -ca ca.pem -ca-key ca-key.pem \
  -config config.json -profile server server-csr.json | \
  cfssljson -bare server
```

---

## 8. So Sánh Các Hệ Thống PKI Mã Nguồn Mở

| Công cụ | Độ phức tạp | Tính năng | Phù hợp |
|---|---|---|---|
| **OpenSSL CA** | Thấp | Cơ bản | Lab, học tập, nhỏ |
| **XCA** | Thấp | Trung bình (GUI) | Lab, nội bộ nhỏ |
| **Let's Encrypt + Certbot** | Thấp | DV cert tự động | Web public |
| **Dogtag/FreeIPA** | Trung bình | Cao | Doanh nghiệp Red Hat |
| **EJBCA** | Cao | Rất cao | Doanh nghiệp lớn, tài chính |
| **HashiCorp Vault PKI** | Trung bình | Cao (cloud-native) | Cloud, K8s, DevOps |
| **CFSSL** | Thấp | Trung bình | Microservices, Go stack |

---

## 9. Hardware Security Module (HSM)

### 9.1 Vai Trò Của HSM Trong PKI
**HSM (Hardware Security Module)** là thiết bị phần cứng chuyên biệt:
- Lưu trữ và bảo vệ **khóa riêng của CA** an toàn tuyệt đối
- Thực hiện các phép ký số **trong phần cứng** (khóa không bao giờ rời HSM)
- FIPS 140-2 / FIPS 140-3 Level 3 hoặc Level 4

### 9.2 Các HSM Phổ Biến
| Sản phẩm | Nhà sản xuất |
|---|---|
| Luna Network HSM | Thales Group |
| PayShield | Thales Group |
| nShield HSM | Entrust |
| CloudHSM | AWS |
| Key Protect | IBM Cloud |
| Azure Dedicated HSM | Microsoft |

### 9.3 Giao Diện PKCS#11 (Cryptoki)
```c
// Giao thức chuẩn để ứng dụng (CA, TLS) truy cập HSM
CK_FUNCTION_LIST *p11;
C_Initialize(NULL);
C_OpenSession(slotID, CKF_RW_SESSION, NULL, NULL, &hSession);
C_Login(hSession, CKU_USER, pin, pinLen);
C_Sign(hSession, data, dataLen, signature, &sigLen);
```
