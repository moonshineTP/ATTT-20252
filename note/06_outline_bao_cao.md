# Outline Báo Cáo – Hạ Tầng Khóa Công Khai PKI

**Môn:** Nhập môn An toàn thông tin  
**Dự kiến:** ~5000 từ, 15–20 trang (không tính tài liệu tham khảo)

---

## BỐ CỤC TỔNG QUAN

```
I.   Giới thiệu                              (~300 từ, 1 trang)
II.  Nền tảng mật mã khóa công khai          (~600 từ, 2 trang)
III. Cấu trúc hạ tầng khóa công khai PKI    (~1000 từ, 3 trang)
IV.  Chứng chỉ số và các chuẩn              (~900 từ, 2.5 trang)
V.   Triển khai và ứng dụng thực tế          (~1200 từ, 3.5 trang)
VI.  Các hệ thống PKI mã nguồn mở           (~700 từ, 2 trang)
VII. Thách thức và xu hướng                  (~400 từ, 1.5 trang)
VIII.Kết luận                               (~200 từ, 0.5 trang)
     Tài liệu tham khảo                     (0.5–1 trang)
```

---

## CHI TIẾT OUTLINE

### I. GIỚI THIỆU

**Vấn đề đặt ra:**
- Mật mã khóa công khai giải quyết trao đổi bí mật và chữ ký số nhưng chưa giải quyết được câu hỏi: "Làm sao xác thực khóa công khai thuộc về đúng người đó?"
- Tấn công Man-in-the-Middle trên kênh phân phối khóa công khai
- Sự cần thiết của bên thứ ba tin cậy trong giao dịch kỹ thuật số

**Phạm vi báo cáo:**
- Định nghĩa và mục tiêu PKI
- Các thành phần cấu trúc PKI
- Chuẩn X.509 và chứng chỉ số
- Ứng dụng thực tế
- Hệ thống mã nguồn mở

---

### II. NỀN TẢNG MẬT MÃ KHÓA CÔNG KHAI

**II.1 Mật mã đối xứng và hạn chế**
- Nguyên lý: cùng khóa dùng cho mã hóa và giải mã
- Vấn đề phân phối khóa bí mật (O(n²) khóa)
- Giải pháp KDC (Key Distribution Center) và hạn chế

**II.2 Mật mã khóa công khai**
- Nguyên lý: cặp khóa (KP, KR) bất đối xứng
- Sơ đồ mã hóa: dùng KP của người nhận
- Sơ đồ xác thực (chữ ký số): dùng KR của người gửi
- Thuật toán RSA: tạo khóa, mã hóa, giải mã
- Trao đổi khóa Diffie-Hellman

**II.3 Vai trò PKI**
- DH không xác thực danh tính → MITM
- Cần bên thứ ba tin cậy để ràng buộc danh tính với khóa công khai

---

### III. CẤU TRÚC HẠ TẦNG KHÓA CÔNG KHAI PKI

**III.1 Định nghĩa và khái niệm**
- PKI = tổ hợp phần cứng, phần mềm, con người, chính sách, quy trình
- Mục tiêu: xác thực, bảo mật, toàn vẹn, không chối cãi

**III.2 Các thành phần**

*III.2.1 CA – Certificate Authority*
- Vai trò: phát hành, thu hồi chứng chỉ, duy trì CRL
- Root CA vs Intermediate CA vs Leaf CA
- Quy trình cấp chứng chỉ (CSR → Verify → Sign → Publish)

*III.2.2 RA – Registration Authority*
- Vai trò trung gian xác minh danh tính
- Tách biệt giữa xác minh (RA) và cấp phát (CA)

*III.2.3 Repository – Kho lưu trữ*
- LDAP directory
- HTTP/HTTPS server
- Lưu chứng chỉ và CRL

*III.2.4 CRL – Certificate Revocation List*
- Khi nào cần thu hồi
- Cấu trúc CRL
- Reason codes (keyCompromise, cACompromise...)
- Hạn chế: CRL có thể lớn và cũ

*III.2.5 OCSP – Online Certificate Status Protocol*
- Kiểm tra realtime từng chứng chỉ
- OCSP Stapling: cải thiện hiệu năng

**III.3 Mô hình tin cậy**
- Mô hình phân cấp (Hierarchical): Root → Int → Leaf
- Web of Trust (PGP): phi tập trung
- Cross-Certification / Bridge CA: liên kết PKI
- So sánh ưu/nhược điểm

**III.4 Chu kỳ sống của chứng chỉ**
- Tạo khóa → CSR → Xác minh → Cấp → Sử dụng → Gia hạn / Thu hồi

---

### IV. CHỨNG CHỈ SỐ VÀ CÁC CHUẨN

**IV.1 Chứng chỉ số X.509**
- Lịch sử: v1 (1988) → v2 (1993) → v3 (1996)
- Định nghĩa: liên kết danh tính với khóa công khai, được CA ký

**IV.2 Cấu trúc X.509 v3**
- Version, SerialNumber, Signature Algorithm
- Issuer, Validity (notBefore/notAfter), Subject
- SubjectPublicKeyInfo
- Extensions: basicConstraints, keyUsage, extendedKeyUsage, SAN, CRL DP, AIA

**IV.3 Distinguished Name (DN)**
- C, ST, L, O, OU, CN, email

**IV.4 Certificate Signing Request (CSR)**
- Cấu trúc, quy trình tạo CSR
- Xác minh sở hữu khóa riêng qua chữ ký trong CSR

**IV.5 Phân loại chứng chỉ**
- Theo mức xác minh: DV / OV / EV
- Theo phạm vi: Single / Wildcard / Multi-SAN

**IV.6 Các chuẩn PKCS**
| Chuẩn | Nội dung |
|---|---|
| PKCS#10 | CSR |
| PKCS#12 | PFX – gói cert + key |
| PKCS#11 | Cryptoki (HSM interface) |
| PKCS#7/CMS | Định dạng dữ liệu ký |

**IV.7 RFC quan trọng**
- RFC 5280: X.509 certificate and CRL profile
- RFC 6960: OCSP
- RFC 8555: ACME Protocol

---

### V. TRIỂN KHAI VÀ ỨNG DỤNG THỰC TẾ

**V.1 HTTPS/TLS**
- Giao thức TLS (lịch sử SSL → TLS 1.0 → 1.2 → 1.3)
- TLS Handshake: xác minh chứng chỉ server
- Certificate chain validation
- Kiểm tra: domain, thời hạn, CRL/OCSP, trust anchor
- TLS 1.3: cải tiến (1-RTT, PFS, loại bỏ thuật toán yếu)

**V.2 Chữ ký số văn bản**
- Nguyên lý: Hash + Encrypt(KR)
- Ứng dụng ở Việt Nam: Luật GDDT 2023, Nghị định 130/2018
- Ký số văn bản hành chính, hóa đơn điện tử, khai báo hải quan
- CA nhà nước: NEAC, VNPT-CA, Viettel-CA

**V.3 S/MIME – Email bảo mật**
- Ký số và mã hóa email
- Tích hợp trong Outlook, Thunderbird
- Quy trình mã hóa email (Hybrid encryption: AES + RSA)

**V.4 VPN và IPSec**
- IKEv2 dùng chứng chỉ X.509 để xác thực VPN gateway/client
- OpenVPN với PKI đầy đủ

**V.5 Code Signing**
- Ký phần mềm: Windows Authenticode, macOS notarization, Android APK
- EV Code Signing: bỏ qua SmartScreen

**V.6 PKI trong eGovernment Việt Nam**
- Cổng DVCQG, Cổng thông tin một cửa, E-invoice, eTax
- Kiến trúc PKI quốc gia (NEAC Root CA)

---

### VI. CÁC HỆ THỐNG PKI MÃ NGUỒN MỞ

**VI.1 OpenSSL**
- Thư viện mật mã phổ biến nhất
- Dùng làm CA đơn giản: tạo Root CA, Int CA, cấp cert
- Các lệnh chính: genrsa, req, x509, ca, verify, s_client
- Demo nhỏ (self-signed cert, custom CA)

**VI.2 EJBCA**
- PKI doanh nghiệp đầy đủ (Java)
- Multi-CA, HSM, RA, OCSP, CMP, SCEP, EST
- Triển khai Docker đơn giản
- Phù hợp cho tổ chức lớn, tài chính, nhà nước

**VI.3 Let's Encrypt & Certbot**
- CA miễn phí, tự động (ACME Protocol)
- Certbot: tự động cấp, gia hạn chứng chỉ DV
- Được sử dụng bởi hàng trăm triệu website
- Giới hạn: chỉ DV, không offline

**VI.4 Các công cụ khác**
- XCA (GUI tool cho lab)
- HashiCorp Vault PKI (cloud-native)
- Dogtag / FreeIPA (Red Hat ecosystem)
- CFSSL (Cloudflare, Golang)

**VI.5 Hardware Security Module (HSM)**
- Vai trò bảo vệ khóa riêng CA
- PKCS#11 interface
- Các sản phẩm: Thales Luna, nShield, AWS CloudHSM

---

### VII. THÁCH THỨC VÀ XU HƯỚNG

**VII.1 Thách thức**
- CA Compromise: DigiNotar (2011) → 500 chứng chỉ giả mạo
- Certificate Transparency (CT): RFC 6962 — log công khai mọi cert TLS
- Quản lý vòng đời chứng chỉ (certificate expiry gây gián đoạn)
- PKI cho IoT: hàng tỷ thiết bị, tài nguyên giới hạn
- Quantum Computing: RSA/ECC sẽ bị phá bởi máy tính lượng tử

**VII.2 Xu Hướng Mới**
- **Post-Quantum PKI:** CRYSTALS-Dilithium, FALCON, SPHINCS+ (NIST PQC 2024)
- **Certificate lifecycle automation (ACME, EST):** Rút ngắn thời hạn cert (398 → 90 ngày)
- **Certificate Transparency (CT Logs):** Phát hiện cert giả mạo
- **ACME for Enterprise:** Tự động hóa cert doanh nghiệp
- **Decentralized PKI (DID):** W3C Decentralized Identifiers

---

### VIII. KẾT LUẬN

- Tóm tắt vai trò thiết yếu của PKI trong hạ tầng bảo mật hiện đại
- PKI giải quyết bài toán tin cậy trong môi trường mạng mở
- Xu hướng tự động hóa và chống lương tử cho PKI tương lai
- Việt Nam đang tích cực phát triển PKI quốc gia

---

### TÀI LIỆU THAM KHẢO (Gợi ý)

**Sách/Giáo trình:**
1. W. Stallings, "Cryptography and Network Security: Principles and Practice," 8th Ed., Pearson, 2022
2. D. Stinson & M. Paterson, "Cryptography: Theory and Practice," 4th Ed., CRC Press, 2018

**RFC:**
3. D. Cooper et al., "Internet X.509 PKI Certificate and CRL Profile," RFC 5280, IETF, 2008
4. S. Chokhani et al., "Internet X.509 PKI – OCSP," RFC 6960, IETF, 2013
5. R. Barnes et al., "ACME: Automatic Certificate Management Environment," RFC 8555, IETF, 2019

**Tiêu chuẩn:**
6. ITU-T Recommendation X.509, "Information Technology – Directory Authentication Framework," 2019
7. NIST SP 800-32, "Introduction to Public Key Technology and the Federal PKI Infrastructure," 2001

**Nguồn trực tuyến:**
8. Let's Encrypt Documentation: https://letsencrypt.org/docs/
9. EJBCA Documentation: https://doc.primekey.com/ejbca
10. Certificate Transparency: https://certificate.transparency.dev

**Nghị định/Luật Việt Nam:**
11. Chính phủ, Nghị định số 130/2018/NĐ-CP về chữ ký số và dịch vụ chứng thực chữ ký số
12. Quốc hội, Luật Giao dịch điện tử số 20/2023/QH15

---

## GỢI Ý PHÂN CÔNG NHÓM (4 người)

| Thành viên | Phần phụ trách | File note tham khảo |
|---|---|---|
| 1 | I + II (Intro + Nền tảng mật mã) | 01_co_so_mat_ma.md |
| 2 | III (Cấu trúc PKI + Trust Models) | 02_pki_tong_quan.md |
| 3 | IV + V (X.509 + Ứng dụng) | 03_chung_chi_so_x509.md + 04_ung_dung_trien_khai.md |
| 4 | VI + VII + VIII (Mã nguồn mở + Xu hướng + Kết luận) | 05_he_thong_mo.md |

> **Lưu ý chung:** Mỗi phần cần có ít nhất 1-2 hình minh họa/sơ đồ.  
> Tổng hợp tài liệu tham khảo chung vào cuối báo cáo.
