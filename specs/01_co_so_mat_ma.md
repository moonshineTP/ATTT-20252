# Cơ Sở Mật Mã – Nền Tảng Cho PKI

> Trích từ giáo trình chap1, chap2, chap3 – PGS. Nguyễn Linh Giang

---

## 1. Tổng Quan An Toàn Thông Tin

### 1.1 Ba Mục Tiêu Cơ Bản (CIA Triad)

| Mục tiêu | Tiếng Việt | Mô tả |
|---|---|---|
| **Confidentiality** | Tính bí mật | Chỉ những người được ủy quyền mới được truy cập thông tin |
| **Integrity** | Tính toàn vẹn | Thông tin không bị sửa đổi trái phép |
| **Availability** | Tính sẵn sàng | Hệ thống hoạt động đúng lúc, dịch vụ không bị từ chối |

### 1.2 Các Dạng Tấn Công (Kiến trúc OSI X.800)

#### Tấn công thụ động (Passive Attack)
- **Chặn giữ thông tin (Interception):** Nghe trộm, theo dõi quá trình truyền tin — tấn công vào **tính bí mật (Confidentiality)**
- Khó phát hiện vì không làm thay đổi dữ liệu
- **Phân tích luồng truyền tải:** Phân tích mẫu truyền thông dù không đọc được nội dung

#### Tấn công chủ động (Active Attack)
| Dạng tấn công | Mô tả | Ảnh hưởng |
|---|---|---|
| **Gián đoạn (Interruption)** | Phá hủy, làm không dùng được | Availability |
| **Chặn giữ (Interception)** | Truy cập trái phép | Confidentiality |
| **Sửa đổi (Modification)** | Thay đổi nội dung thông tin | Integrity |
| **Làm giả (Fabrication)** | Đưa thông tin giả mạo vào hệ thống | Authenticity |

---

## 2. Mật Mã Khóa Đối Xứng

### 2.1 Nguyên Lý
- Cùng một khóa K dùng cho cả **mã hóa** và **giải mã**
- Sơ đồ: `C = E_K(P)`, `P = D_K(C)`
- **Vấn đề cốt lõi:** Cần kênh bí mật để phân phối khóa

### 2.2 Phân Loại Thuật Toán

#### Mã Dòng (Stream Cipher)
- Mã từng bit/byte riêng lẻ
- Ví dụ: Vernam cipher (One-time pad) — `Cᵢ = Pᵢ ⊕ Kᵢ`
- One-time pad: **lý thuyết là hoàn toàn an toàn** nhưng khó triển khai thực tế (cần khóa dài bằng bản rõ)

#### Mã Khối (Block Cipher)
- Mã từng khối bit (64/128 bit) theo từng khối
- Ví dụ điển hình: **DES**, **AES**

### 2.3 Thuật Toán DES (Data Encryption Standard)
- Khóa 56 bit; khối 64 bit
- Phát triển bởi IBM, công bố năm 1977
- Không gian khóa: 2⁵⁶ ≈ 7.2 × 10¹⁶ khóa
- **Điểm yếu:** Khóa quá ngắn, có thể bị brute-force
- **Giải pháp:** 3DES (Triple DES) với khóa 112 hoặc 168 bit

### 2.4 Vấn Đề Phân Phối Khóa Đối Xứng
- Hai bên A và B cần chia sẻ khóa trước khi truyền tin
- Với N người dùng: cần **N(N-1)/2** cặp khóa — **không mở rộng được**
- Giải pháp cổ điển: Trung tâm phân phối khóa **(KDC – Key Distribution Center)**

#### Sơ đồ KDC:
```
A → KDC: Yêu cầu || N₁
KDC → A: E_Ka[Ks || Yêu cầu || N₁ || E_Kb[Ks || ID_A]]
A → B: E_Kb[Ks || ID_A]
B → A: E_Ks[N₂]
A → B: E_Ks[f(N₂)]
```
- `Ka`, `Kb`: khóa chính của A, B (chỉ mình A/B và KDC biết)
- `Ks`: khóa phiên tạm thời

---

## 3. Mật Mã Khóa Công Khai (Bất Đối Xứng)

### 3.1 Động Lực Ra Đời
Giải quyết hai vấn đề của mã hóa đối xứng:
1. **Bài toán phân phối khóa** (Diffie-Hellman, 1976)
2. **Bài toán chữ ký số** (RSA, 1977)

### 3.2 Nguyên Lý Cơ Bản
- Mỗi người dùng có một **cặp khóa (KP, KR)**:
  - `KP` (Public Key): Khóa công khai — công bố rộng rãi
  - `KR` (Private Key): Khóa riêng — giữ bí mật tuyệt đối
- Một khóa dùng để **mã hóa**, khóa kia dùng để **giải mã**

### 3.3 Hai Sơ Đồ Ứng Dụng Cơ Bản

#### Sơ đồ Bảo Mật (Mã hóa):
```
A muốn gửi bí mật cho B:
  C = E(KPB, M)    ← A mã hóa bằng khóa công khai của B
  M = D(KRB, C)    ← B giải mã bằng khóa riêng của mình
→ Đảm bảo CHỈ B đọc được
```

#### Sơ đồ Xác Thực (Chữ ký số):
```
A muốn gửi thông điệp có xác thực:
  S = E(KRA, M)    ← A ký bằng khóa riêng của mình
  M = D(KPA, S)    ← Bất kỳ ai cũng có thể xác thực bằng KPA
→ Đảm bảo thông điệp do ĐÚNG A tạo ra
```

### 3.4 Yêu Cầu Toán Học
1. `E(KP, M)` và `D(KR, C)` phải **dễ tính** (đa thức thời gian)
2. Không thể suy ra `KR` từ `KP` trong thời gian đa thức
3. Tính đối xứng: `M = D(KP, E(KR, M))` và `M = D(KR, E(KP, M))`

---

## 4. Thuật Toán RSA

### 4.1 Xuất Xứ
- Ron **R**ivest, Adi **S**hamir, Leonard **A**dleman — 1977
- Cơ sở: **Bài toán phân tích thừa số nguyên tố** (khó tính toán)

### 4.2 Tạo Khóa
```
1. Chọn 2 số nguyên tố lớn p, q (giữ bí mật)
2. Tính n = p × q  (modulus — công khai)
3. Tính φ(n) = (p-1)(q-1)
4. Chọn e: gcd(e, φ(n)) = 1, 1 < e < φ(n)  ← khóa công khai
5. Tính d: d ≡ e⁻¹ (mod φ(n))               ← khóa riêng

Khóa công khai:  (e, n)
Khóa riêng:      (d, n)
```

**Ví dụ nhỏ:** p=7, q=17 → n=119, φ(n)=96, e=5, d=77

### 4.3 Mã Hóa / Giải Mã
```
Mã hóa:   C = Mᵉ mod n
Giải mã:  M = Cᵈ mod n
Tính đúng vì: (Mᵉ)ᵈ = M^(ed) ≡ M (mod n)  [Định lý Euler]
```

### 4.4 Bảo Mật RSA — Các Dạng Tấn Công
| Dạng tấn công | Mô tả | Đối phó |
|---|---|---|
| Vét cạn (Brute force) | Thử toàn bộ không gian khóa riêng | Tăng độ dài khóa (≥2048 bit) |
| Tấn công toán học | Phân tích n = p×q | Chọn p, q đủ lớn (1075~10100) |
| Tấn công thời gian | Đo thời gian thực thi để suy ra khóa | Thêm trễ ngẫu nhiên, làm mù (blinding) |

**Yêu cầu chọn p, q:**
- p, q phải lớn (độ dài từ 1024—2048 bit mỗi số)
- `(p-1)` và `(q-1)` phải có thừa số nguyên tố lớn
- `gcd(p-1, q-1)` phải nhỏ
- Hiện tại RSA-2048 bit được coi là đủ an toàn (đến ~2030+)

---

## 5. Trao Đổi Khóa Diffie-Hellman

### 5.1 Ý Tưởng
- Cho phép 2 bên tạo **khóa phiên dùng chung** qua kênh **không bảo mật** mà không cần gặp nhau trước
- Cơ sở: **Bài toán logarit rời rạc** (khó tính)

### 5.2 Thuật Toán
```
Thống nhất công khai: p (số nguyên tố lớn), g (phần tử sinh mod p)

Alice:               Bob:
Chọn a bí mật        Chọn b bí mật
A = gᵃ mod p  ←→    B = gᵇ mod p  (trao đổi công khai)

Alice tính: s = Bᵃ mod p = g^(ab) mod p
Bob tính:   s = Aᵇ mod p = g^(ab) mod p
→ s là khóa phiên chung dùng để mã hóa đối xứng
```

### 5.3 Điểm Yếu: Man-in-the-Middle
- DH không xác thực danh tính — dễ bị tấn công **MITM**
- **Giải pháp:** Kết hợp với **xác thực danh tính** → đây là lý do cần **PKI**

---

## 6. Lý Thuyết Số Cơ Bản (Nền Tảng Toán Học)

### 6.1 Số Học Modun
- `a ≡ b (mod n)` khi a và b có cùng số dư khi chia cho n
- `[(a mod n) × (b mod n)] mod n = (a × b) mod n`

### 6.2 Định Lý Fermat
- Nếu p là số nguyên tố, gcd(a, p) = 1: `aᵖ⁻¹ ≡ 1 (mod p)`

### 6.3 Hàm Euler φ(n)
- `φ(n)` = số nguyên dương < n, nguyên tố cùng nhau với n
- Với p nguyên tố: `φ(p) = p - 1`
- Với n = pq (p, q nguyên tố): `φ(n) = (p-1)(q-1)`

### 6.4 Định Lý Euler
- Nếu gcd(a, n) = 1: `a^φ(n) ≡ 1 (mod n)` — cơ sở chứng minh đúng đắn của RSA

### 6.5 Thuật Toán Euclid mở rộng
- Tính `gcd(a, b)` và nghịch đảo modular `d ≡ e⁻¹ (mod φ(n))`
