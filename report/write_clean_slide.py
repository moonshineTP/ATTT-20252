import pathlib

code = r"""% !TEX program = pdflatex
% ============================================================
%  Slide Báo cáo: Hạ Tầng Khóa Công Khai (PKI)
%  Môn   : Nhập môn An toàn thông tin
%  Trường : ĐHBK Hà Nội – SOICT
%  Tác giả: Nhóm 8 (Kiến thức nền tảng & Thực nghiệm Python)
% ============================================================
\documentclass[10pt, aspectratio=169]{beamer}

% --- Encoding & Language ---
\usepackage[utf8]{inputenc}
\usepackage[T5]{fontenc}
\usepackage[vietnamese, english]{babel}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{colortbl}
\usepackage{tikz}
\usepackage{caption}

% --- Beamer Theme Customization ---
\usetheme{Boadilla}
\usecolortheme{default}
\usefonttheme{structurebold}

% Brand Color Scheme (Deep Blue & Accents)
\definecolor{pkiblue}{RGB}{12, 68, 124}     % #0C447C
\definecolor{pkigreen}{RGB}{30, 132, 73}    % #1E8449
\definecolor{pkiorange}{RGB}{211, 84, 0}    % #D35400
\definecolor{lightgray}{RGB}{245, 245, 245}

\setbeamercolor{structure}{fg=pkiblue}
\setbeamercolor{titlelike}{parent=structure,fg=pkiblue}
\setbeamercolor{title}{bg=pkiblue,fg=white}
\setbeamercolor{palette primary}{bg=pkiblue,fg=white}
\setbeamercolor{palette secondary}{bg=pkiblue!85!black,fg=white}
\setbeamercolor{palette tertiary}{bg=pkiblue!70!black,fg=white}
\setbeamercolor{block title}{bg=pkiblue!10!white,fg=pkiblue}
\setbeamercolor{block body}{bg=lightgray,fg=black}

% Remove navigation symbols
\setbeamertemplate{navigation symbols}{}

% Custom footer customization
\setbeamertemplate{footline}{
  \leavevmode%
  \hbox{%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{author in head/foot}%
    \usebeamerfont{author in head/foot}Đỗ Trường Giang, Phạm Gia Hưng
  \end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{title in head/foot}%
    \usebeamerfont{title in head/foot}Báo cáo PKI -- Nhóm 8
  \end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,right]{date in head/foot}%
    \usebeamerfont{date in head/foot}\insertframenumber{} / \inserttotalframenumber\hspace*{2ex} 
  \end{beamercolorbox}}%
  \vskip0pt%
}

% Section divider page template
\AtBeginSection[]{
  \begin{frame}
    \vfill
    \centering
    \begin{beamercolorbox}[sep=8pt,center,shadow=true,rounded=true]{title}
      \usebeamerfont{title}\insertsectionhead\par%
    \end{beamercolorbox}
    \vfill
  \end{frame}
}

% ============================================================
%  Slide Metadata
% ============================================================
\title[Hạ Tầng Khóa Công Khai (PKI)]{HẠ TẦNG KHÓA CÔNG KHAI (PKI)}
\subtitle{Báo cáo môn học: Nhập môn An toàn thông tin}
\author[Nhóm 8]{
    \textbf{Nhóm 8 -- Thành viên thực hiện:}\\
    \small
    Đỗ Trường Giang (20235066) \quad Phạm Gia Hưng (20230036)\\
    Hoàng Minh Khôi (20230042) \quad Nguyễn Thanh Tú (20230075)
}
\institute[SOICT -- HUST]{
    Trường Công nghệ Thông tin và Truyền thông (SOICT)\\
    Đại học Bách khoa Hà Nội
}
\date[2026]{Hà Nội, Tháng 6 Năm 2026}

% ============================================================
%  Main Document
% ============================================================
\begin{document}

% --- Title Page ---
\begin{frame}[plain]
    \titlepage
\end{frame}

% --- Agenda ---
\begin{frame}{Nội dung chương trình}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.5\textwidth}
            \begin{block}{Phần I: Kiến thức nền tảng của PKI (Trọng tâm)}
                \begin{itemize}
                    \item Đặt vấn đề \& Tiến hóa mật mã
                    \item Các thực thể PKI (RootCA, SubCA, RA, VA)
                    \item TLS, OCSP, OCSP Stapling \& Trusted Path
                    \item Cấu trúc chứng chỉ X.509 v3
                    \item Kịch bản áp dụng Extensions của X.509 v3
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.46\textwidth}
            \begin{block}{Phần II: Thực nghiệm \& Nguồn mở}
                \begin{itemize}
                    \item Khảo sát hệ sinh thái mã nguồn mở
                    \item Triển khai thử EJBCA trên Docker
                    \item Tương tác EJBCA bằng ngôn ngữ Python
                    \item Thách thức (PQC, Zero Trust)
                \end{itemize}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% ============================================================
%  PHẦN I: KIẾN THỨC NỀN TẢNG CỦA PKI
% ============================================================
\section{Phần I: Kiến thức nền tảng của PKI}

% --- 1.1 Vấn đề đặt ra ---
\begin{frame}{Đặt vấn đề: Mật mã bất đối xứng và Tấn công MITM}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            \textbf{Hạn chế của mật mã bất đối xứng:}
            \begin{itemize}
                \item Giải quyết tốt việc trao đổi khóa và ký số không cần gặp trước.
                \item Tuy nhiên, thiếu cơ chế \textbf{ràng buộc danh tính} (identity binding) với khóa công khai.
            \end{itemize}
            \vspace{0.2cm}
            \textbf{Tấn công Kẻ đứng giữa (Man-in-the-Middle - MITM):}
            \begin{itemize}
                \item Kẻ tấn công (Mallory) đánh chặn khóa công khai thật của Bob.
                \item Thay thế bằng khóa công khai giả mạo của mình.
                \item Alice mã hóa dữ liệu bằng khóa giả của Mallory $\rightarrow$ Bị lộ thông tin.
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=\textwidth,keepaspectratio]{assets/fig_mitm.png}
                \caption{Tấn công trung gian khi phân phối khóa thô}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% --- 1.2 Giải pháp CA ---
\begin{frame}{Giải pháp: Neo tín nhiệm qua CA}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            \textbf{Vai trò của Tổ chức Chứng thực (CA):}
            \begin{itemize}
                \item Hoạt động như bên thứ ba tin cậy (Trusted Third Party - TTP).
                \item Đóng vai trò là \textbf{Neo tín nhiệm (Trust Anchor)}.
                \item Xác minh danh tính và dùng khóa riêng của CA để ký xác thực cho khóa công khai của chủ thể.
            \end{itemize}
            \vspace{0.2cm}
            \textbf{Kết quả:}
            \begin{itemize}
                \item Client chỉ cần tin tưởng vào khóa công khai của Root CA (nằm trong Trust Store).
                \item Client tự động xác minh được mọi khóa công khai của máy chủ bằng cách lần chuỗi chữ ký về Root CA.
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=\textwidth,keepaspectratio]{assets/fig_pki_ca.png}
                \caption{Mô hình xác thực khóa công khai qua CA}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% --- 1.3 Mật mã đối xứng & Hạn chế ---
\begin{frame}{Tiến hóa mật mã: Mật mã đối xứng và hạn chế}
    \begin{block}{Nguyên lý hoạt động}
        Sử dụng chung khóa bí mật $K$: $C = \mathrm{E}(K, P)$ và $P = \mathrm{D}(K, C)$. Thuật toán tiêu biểu: \textbf{AES}, \textbf{DES}, \textbf{3DES}.
    \end{block}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.48\textwidth}
            \textbf{Ưu điểm vượt trội:}
            \begin{itemize}
                \item Tốc độ xử lý cực nhanh trên phần cứng.
                \item Đáp ứng truyền tải dữ liệu lớn thời gian thực (video streaming, mã hóa đĩa).
            \end{itemize}
        \end{column}
        \begin{column}{0.48\textwidth}
            \textbf{Hạn chế chí mạng:}
            \begin{itemize}
                \item \textbf{Phân phối khóa:} Catch-22 (cần kênh bảo mật để gửi khóa bí mật).
                \item \textbf{Độ phình khóa:} Mạng $n$ node cần $\frac{n(n-1)}{2} = O(n^2)$ khóa.
                \item \textbf{KDC (Kerberos) giới hạn:} Điểm lỗi tập trung (SPOF), tắc nghẽn hiệu năng, God-mode DB.
            \end{itemize}
        \end{column}
    \end{columns}
\end{frame}

% --- 1.4 Mật mã bất đối xứng ---
\begin{frame}{Mật mã bất đối xứng và Hàm cửa sập}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            \textbf{Nguyên lý Cặp khóa (Khóa công khai PU, Khóa riêng PR):}
            \begin{itemize}
                \item \textbf{Bảo mật (Secrecy):} Mã hóa bằng $PU$ người nhận $\rightarrow$ Chỉ $PR$ người nhận giải được.
                \item \textbf{Xác thực/Ký số:} Ký bằng $PR$ người gửi $\rightarrow$ Ai cũng giải được bằng $PU$ người gửi để xác nhận nguồn gốc.
                \item \textbf{Kết hợp:} Ký bằng $PR$ người gửi, mã hóa bằng $PU$ người nhận.
            \end{itemize}
            \vspace{0.2cm}
            \textbf{Toán học: Hàm một chiều có cửa sập (Trapdoor One-way):}
            \begin{itemize}
                \item Tính xuôi $Y = f(X)$ dễ dàng.
                \item Tính ngược $X = f^{-1}(Y)$ là bất khả thi trừ khi biết khóa riêng $PR$ đóng vai trò "cửa sập".
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=0.58\textwidth,keepaspectratio]{assets/EWPU.png}\\[0.05cm]
                \includegraphics[width=0.58\textwidth,keepaspectratio]{assets/EWPR.png}
                \caption{Mô hình mã hóa (trên) và ký số (dưới)}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% --- 1.5 Thuật toán RSA & DH ---
\begin{frame}{Thuật toán RSA và Trao đổi khóa Diffie-Hellman}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.48\textwidth}
            \begin{block}{Thuật toán RSA (Phân tích thừa số nguyên tố)}
                \begin{itemize}
                    \item $n = p \times q$ ($p, q$ là số nguyên tố lớn).
                    \item Khóa công khai $PU = \{e, n\}$, Khóa bí mật $PR = \{d, n\}$.
                    \item Mã hóa: $C = M^e \bmod n$.
                    \item Giải mã: $M = C^d \bmod n$.
                    \item \textbf{An toàn:} Chống Timing attack bằng \textit{Blinding} (nhân bản mã với $r^e$ ngẫu nhiên), chống CCA bằng \textit{đệm OAEP}.
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.48\textwidth}
            \begin{block}{Trao đổi khóa Diffie-Hellman}
                \begin{itemize}
                    \item Dựa trên \textbf{Logarit rời rạc} trên trường modulo số nguyên tố lớn $q$.
                    \item Alice tính: $Y_A = \alpha^{X_A} \bmod q$.
                    \item Bob tính: $Y_B = \alpha^{X_B} \bmod q$.
                    \item Khóa chung: $K = (Y_B)^{X_A} \bmod q = (Y_A)^{X_B} \bmod q = \alpha^{X_A \cdot X_B} \bmod q$.
                    \item \textbf{Lỗ hổng:} Không xác thực danh tính $\rightarrow$ dễ bị can thiệp và tráo đổi khóa (MITM).
                \end{itemize}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% --- 1.6 Chữ ký số ---
\begin{frame}{Chữ ký số và Chống chối cãi}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            \textbf{Giải quyết điểm yếu của Mật mã đối xứng:}
            \begin{itemize}
                \item Khóa đối xứng dùng chung có rủi ro người nhận tự sửa đổi nội dung giao dịch rồi đổ lỗi hoặc người gửi chối bỏ trách nhiệm gửi.
            \end{itemize}
            \vspace{0.2cm}
            \textbf{Nguyên lý hoạt động:}
            \begin{itemize}
                \item Ký số = Tính Hash của thông điệp + Mã hóa Hash bằng khóa riêng ($PR$) của người gửi.
                \item Đạt được \textbf{Tính chống chối cãi (Non-repudiation)}: Chỉ có người sở hữu khóa riêng mới tạo được chữ ký hợp lệ.
            \end{itemize}
            \vspace{0.2cm}
            \textbf{Các cấp độ giả mạo chữ ký:}
            \begin{itemize}
                \item Total break (lộ khóa $PR$).
                \item Universal / Selective / Existential forgery.
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=\textwidth,keepaspectratio]{assets/fig_digital_signature.png}
                \caption{Sơ đồ tạo và xác thực chữ ký số}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% ============================================================
%  CÁC THỰC THỂ CỦA PKI (RootCA, SubCA, RA, VA)
% ============================================================
\section{Các thực thể PKI: RootCA, SubCA, RA, VA}

% --- 2.1 Định nghĩa thực thể ---
\begin{frame}{Các thực thể trong hệ thống PKI}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.50\textwidth}
            \begin{block}{1. Root CA (Tổ chức phát hành chứng chỉ gốc)}
                \begin{itemize}
                    \item Neo tín nhiệm tối cao của toàn hệ thống.
                    \item Sử dụng \textbf{chứng chỉ tự ký (self-signed)}.
                    \item Cần được cách ly vật lý hoàn toàn (\textit{offline}, \textit{air-gapped}) để bảo mật tuyệt đối khóa riêng.
                \end{itemize}
            \end{block}
            \begin{block}{2. Sub CA / Intermediate CA (CA trung gian)}
                \begin{itemize}
                    \item Được Root CA ký ủy quyền.
                    \item Chịu trách nhiệm trực tiếp ký và cấp phát chứng chỉ cho thực thể cuối (\textit{leaf certificate}).
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.48\textwidth}
            \begin{block}{3. RA -- Registration Authority (Tổ chức đăng ký)}
                \begin{itemize}
                    \item Xác minh danh tính thực tế của đối tượng yêu cầu.
                    \item Duyệt/Từ chối CSR, nhưng \textbf{không trực tiếp ký phát hành} chứng chỉ.
                \end{itemize}
            \end{block}
            \begin{block}{4. VA -- Validation Authority (Tổ chức kiểm duyệt)}
                \begin{itemize}
                    \item Xác thực trạng thái chứng chỉ (còn hiệu lực, bị thu hồi, hay tạm dừng).
                    \item Triển khai qua dịch vụ thư mục công cộng, máy chủ CRL hoặc OCSP Responder.
                \end{itemize}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% --- 2.2 Mối quan hệ các thực thể ---
\begin{frame}{Mối quan hệ và luồng vận hành của các thực thể}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            \textbf{Phân quyền trách nhiệm (Separation of Duty):}
            \begin{itemize}
                \item \textbf{RA} lo khâu xác thực ngoài đời thực (giấy tờ, tên miền). Giúp CA tránh tiếp xúc trực tiếp mạng Internet.
                \item \textbf{CA} lo khâu ký số mật mã trong phân vùng an toàn cao (HSM).
                \item \textbf{VA} lo khâu phản hồi thông tin kiểm tra cho bên thứ ba nhanh chóng.
            \end{itemize}
            \vspace{0.2cm}
            \textbf{Mối quan hệ tương tác:}
            \begin{itemize}
                \item Root CA ký cho Sub CA $\rightarrow$ Sub CA ký cho Leaf Cert.
                \item Client nộp yêu cầu qua RA $\rightarrow$ RA duyệt $\rightarrow$ Sub CA ký cert $\rightarrow$ Sub CA đồng bộ thông tin thu hồi sang VA $\rightarrow$ Verifier truy vấn VA để kiểm duyệt cert của Client.
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=\textwidth,keepaspectratio]{assets/fig_pki_components.png}
                \caption{Quan hệ tương tác CA, RA, VA (Repository)}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% --- 2.3 Giao tiếp Client & RA ---
\begin{frame}{Quy trình giao tiếp: Client xin cấp chứng chỉ từ RA}
    \begin{block}{Các bước giao tiếp mật mã (CSR Flow)}
        \begin{enumerate}
            \item \textbf{Khởi tạo cục bộ:} Client tự tạo cặp khóa bí mật/công khai của mình trên máy.
            \item \textbf{Tạo CSR (PKCS\#10):} Client đóng gói thông tin định danh mong muốn + Khóa công khai, dùng khóa riêng ký lên gói này để chứng minh quyền sở hữu khóa (\textit{Proof-of-Possession}).
            \item \textbf{Gửi yêu cầu:} Client gửi CSR cùng các hồ sơ chứng minh danh tính pháp nhân đến \textbf{RA}.
            \item \textbf{RA Xác minh:} RA kiểm tra tính hợp lệ của CSR, thực hiện các thử thách kiểm soát tên miền (DNS/HTTP challenge) hoặc xác minh giấy tờ của Client.
            \item \textbf{Chuyển tiếp ký:} Sau khi xác minh thành công, RA ký phê duyệt và gửi yêu cầu đến \textbf{CA}.
            \item \textbf{Ký và Trả kết quả:} CA ký số tạo chứng chỉ X.509, lưu trữ vào Repository, và gửi lại cho Client sử dụng.
        \end{enumerate}
    \end{block}
\end{frame}

% --- 2.4 Cách VA xử lý yêu cầu ---
\begin{frame}{Cách VA xử lý yêu cầu kiểm duyệt trạng thái chứng chỉ}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.55\textwidth}
            Khi Verifier muốn kiểm tra trạng thái chứng chỉ, nó sẽ truy vấn \textbf{VA} (Validation Authority):
            \vspace{0.1cm}
            \begin{block}{Quy trình xử lý của VA (OCSP/CRL)}
                \begin{itemize}
                    \item \textbf{Bước 1: Tiếp nhận:} Nhận hash định danh CA và số serial từ Verifier.
                    \item \textbf{Bước 2: Tra cứu:} VA tìm kiếm serial trong danh sách thu hồi (từ CA).
                    \item \textbf{Bước 3: Tạo phản hồi:} Đóng gói trạng thái (\texttt{Good}, \texttt{Revoked}, \texttt{Unknown}) và ký số bằng khóa riêng của VA.
                    \item \textbf{Bước 4: Trả kết quả:} Gửi phản hồi về cho Verifier.
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.42\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=0.65\textwidth,keepaspectratio]{assets/fig_pki_validation.png}
                \caption{Kiểm tra chứng chỉ của Verifier}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% ============================================================
%  GIAO THỨC TLS, OCSP, OCSP STAPLING & TRUSTED PATH
% ============================================================
\section{Giao thức mạng: TLS, OCSP, OCSP Stapling \& Trusted Path}

% --- 3.1 Giao thức TLS ---
\begin{frame}{Giao thức bắt tay TLS (TLS 1.3 Handshake)}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            TLS 1.3 bảo mật kênh truyền web bằng cách rút ngắn thời gian bắt tay (1-RTT) và ép buộc xác thực chứng chỉ:
            \begin{itemize}
                \item \textbf{1. ClientHello:} Client gửi các bộ thuật toán mã hóa hỗ trợ + Key Share đàm phán khóa.
                \item \textbf{2. ServerHello:} Server chọn thuật toán và gửi Key Share của mình.
                \item \textbf{3. Server Certificate:} Server gửi chứng chỉ X.509 của mình kèm chuỗi CA.
                \item \textbf{4. CertificateVerify:} Server dùng khóa riêng của mình ký lên toàn bộ dữ liệu bắt tay trước đó để chứng minh quyền sở hữu khóa.
                \item \textbf{5. Client verify:} Client dựng chuỗi niềm tin, xác minh chữ ký trên chứng chỉ và bắt tay. Kênh mã hóa được thiết lập.
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=\textwidth,keepaspectratio]{assets/fig_tls_handshake.png}
                \caption{Sơ đồ bắt tay TLS 1.3}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% --- 3.2 Giao thức OCSP ---
\begin{frame}{Giao thức OCSP (Online Certificate Status Protocol)}
    \begin{block}{Khái niệm và Nguyên lý (RFC 6960)}
        OCSP là giao thức thay thế cho CRL để kiểm tra trạng thái thu hồi chứng chỉ theo thời gian thực (real-time) thông qua HTTP.
    \end{block}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            \textbf{Quy trình hoạt động:}
            \begin{itemize}
                \item Client gửi một truy vấn nhẹ chứa số serial của cert lên máy chủ OCSP của CA.
                \item OCSP Responder tra cứu cơ sở dữ liệu và trả về kết quả trạng thái chứng chỉ ngay lập tức.
            \end{itemize}
            \vspace{0.1cm}
            \textbf{Hạn chế lớn của OCSP truyền thống:}
            \begin{itemize}
                \item \textbf{Quyền riêng tư:} CA không biết Client đang duyệt web ở trang nào.
                \item \textbf{Hiệu năng:} Client phải tạo thêm một kết nối mạng HTTP phụ đến CA trước khi hoàn thành bắt tay TLS $\rightarrow$ tăng độ trễ tải trang.
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{table}
                \centering
                \tiny
                \begin{tabular}{lp{3.5cm}}
                    \toprule
                    \textbf{Trạng thái} & \textbf{Ý nghĩa} \\
                    \midrule
                    \texttt{Good} & Chứng chỉ còn hiệu lực và bình thường. \\
                    \texttt{Revoked} & Chứng chỉ đã bị thu hồi vĩnh viễn hoặc tạm dừng. \\
                    \texttt{Unknown} & VA/CA không có thông tin về số serial này. \\
                    \bottomrule
                \end{tabular}
                \caption{3 trạng thái phản hồi của OCSP}
            \end{table}
        \end{column}
    \end{columns}
\end{frame}

% --- 3.3 OCSP Stapling ---
\begin{frame}{Kỹ thuật OCSP Stapling}
    \begin{block}{Giải pháp tối ưu hóa Hiệu năng và Bảo mật (RFC 6066)}
        Thay vì Client tự liên hệ VA để hỏi trạng thái cert, \textbf{Máy chủ Web (Server)} sẽ đảm nhận việc này.
    \end{block}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.50\textwidth}
            \textbf{Quy trình vận hành:}
            \begin{enumerate}
                \item Máy chủ Web định kỳ tự kết nối đến máy chủ OCSP của VA để lấy phản hồi trạng thái cert của chính mình.
                \item VA gửi phản hồi OCSP đã được ký số và đóng dấu thời gian về cho Máy chủ Web. Máy chủ lưu cache kết quả này.
                \item Khi Client bắt tay TLS, Máy chủ Web "đính kèm" (staple) câu trả lời OCSP này gửi kèm chứng chỉ cho Client.
            \end{enumerate}
        \end{column}
        \begin{column}{0.48\textwidth}
            \textbf{Ưu điểm vượt trội:}
            \begin{itemize}
                \item \textbf{Tốc độ cực nhanh:} Client không cần kết nối mạng phụ đến VA, giảm 1-RTT.
                \item \textbf{Bảo vệ quyền riêng tư:} VA không hề biết Client đang duyệt web ở trang nào.
                \item \textbf{Đáng tin cậy:} Client vẫn tự xác minh được chữ ký của VA trên gói tin OCSP đính kèm.
            \end{itemize}
        \end{column}
    \end{columns}
\end{frame}

% --- 3.4 Trusted Path ---
\begin{frame}{Cơ chế Trusted Path (Xác thực đường dẫn chứng chỉ)}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            Dựng và xác minh chuỗi niềm tin từ chứng chỉ thực thể cuối (\textit{leaf}) về neo tín nhiệm (\textit{Root CA}):
            \vspace{0.1cm}
            \begin{block}{Quy trình kiểm tra đường dẫn (RFC 5280)}
                \begin{enumerate}
                    \item \textbf{Dựng chuỗi (Path Building):} Tìm kiếm các CA phát hành bằng cách khớp \texttt{AuthorityKeyID} và \texttt{SubjectKeyID}.
                    \item \textbf{Xác minh chữ ký:} Dùng khóa công khai của CA cấp trên xác minh chữ ký của CA cấp dưới (đi ngược từ dưới lên).
                    \item \textbf{Kiểm tra ràng buộc:} Hiệu lực thời gian, cờ \texttt{cA=true} (BasicConstraints), và mục đích sử dụng (KeyUsage, EKU).
                \end{enumerate}
            \end{block}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=0.7\textwidth,keepaspectratio]{assets/fig_pki_hierarchy.png}
                \caption{Chuỗi tin cậy từ Root CA đến Leaf}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% ============================================================
%  CHÚNG CHỈ X.509 V3 & KỊCH BẢN EXTENSIONS
% ============================================================
\section{Chứng chỉ số X.509 v3 \& Kịch bản áp dụng Extensions}

% --- 4.1 Cấu trúc X.509 v3 ---
\begin{frame}{Cấu trúc chứng chỉ X.509 v3}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            Định nghĩa bởi ITU-T và chuẩn hóa bởi IETF qua RFC 5280. Cấu trúc logic gồm 3 khối dữ liệu ASN.1 lớn:
            \vspace{0.1cm}
            \begin{block}{1. tbsCertificate (To Be Signed)}
                Chứa nội dung thông tin cốt lõi của cert:
                \begin{itemize}
                    \item \texttt{Version} (v3), \texttt{SerialNumber} (số seri duy nhất).
                    \item \texttt{Issuer}: Tên DN của CA phát hành.
                    \item \texttt{Validity}: Thời hạn (\texttt{notBefore} và \texttt{notAfter}).
                    \item \texttt{Subject}: Tên DN định danh chủ thể được cấp.
                    \item \texttt{subjectPublicKeyInfo}: Khóa công khai và thuật toán.
                    \item \texttt{Extensions}: Các trường mở rộng cấu hình.
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=0.95\textwidth,keepaspectratio]{assets/fig_x509.png}
                \caption{Cấu trúc logic phân lớp của X.509}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% --- 4.2 Kịch bản Extensions 1 ---
\begin{frame}{Kịch bản áp dụng Extensions X.509 v3 (Phần 1)}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.48\textwidth}
            \begin{block}{Kịch bản 1: HTTPS/TLS Server Auth}
                Dùng để xác thực danh tính Web Server công cộng.
                \begin{itemize}
                    \item \textbf{KeyUsage:} \texttt{digitalSignature} (xác thực bắt tay), \texttt{keyEncipherment} (mã hóa trao đổi khóa RSA) hoặc \texttt{keyAgreement} (Diffie-Hellman).
                    \item \textbf{ExtendedKeyUsage (EKU):} \texttt{serverAuth} (OID: 1.3.6.1.5.5.7.3.1) $\rightarrow$ Khống chế cert chỉ làm Web Server.
                    \item \textbf{SubjectAltName (SAN):} Bắt buộc chứa tên miền website (ví dụ: \texttt{DNS:www.hust.edu.vn}) để trình duyệt so khớp hostname.
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.48\textwidth}
            \begin{block}{Kịch bản 2: Client Auth (mTLS / VPN)}
                Xác thực người dùng/thiết bị kết nối hệ thống.
                \begin{itemize}
                    \item \textbf{KeyUsage:} \texttt{digitalSignature}.
                    \item \textbf{ExtendedKeyUsage (EKU):} \texttt{clientAuth} (OID: 1.3.6.1.5.5.7.3.2).
                    \item \textbf{SubjectAltName (SAN):} Chứa email (\texttt{rfc822Name:}\\\texttt{giang.dt235066@sis.hust.edu.vn}) hoặc URI nhận diện.
                \end{itemize}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% --- 4.3 Kịch bản Extensions 2 ---
\begin{frame}{Kịch bản áp dụng Extensions X.509 v3 (Phần 2)}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.48\textwidth}
            \begin{block}{Kịch bản 3: Ký mã nguồn (Code Signing)}
                Xác minh phần mềm sạch, chống giả mạo driver.
                \begin{itemize}
                    \item \textbf{KeyUsage:} \texttt{digitalSignature} (ký tệp tin thực thi, exe, dll, dmg).
                    \item \textbf{ExtendedKeyUsage (EKU):} \texttt{codeSigning} (OID: 1.3.6.1.5.5.7.3.3) $\rightarrow$ Ngăn chặn kẻ tấn công lấy chứng chỉ HTTPS đi ký cho mã độc.
                \end{itemize}
            \end{block}
        \end{column}
        \begin{column}{0.48\textwidth}
            \begin{block}{Kịch bản 4: Chứng chỉ CA (Ủy quyền ký)}
                Cấp cho các thực thể ký phát hành trong PKI.
                \begin{itemize}
                    \item \textbf{BasicConstraints:} Cờ \texttt{cA = True} (Bắt buộc). Nếu thiếu hoặc false, client từ chối mọi cert do khóa này ký.
                    \item \textbf{KeyUsage:} \texttt{keyCertSign} (quyền ký chứng chỉ) và \texttt{cRLSign} (quyền ký CRL).
                    \item \textbf{PathLenConstraint:} Giới hạn cấp CA con tối đa bên dưới.
                \end{itemize}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% --- 4.4 CSR & Chuẩn PKCS ---
\begin{frame}{CSR (PKCS\#10) và Họ chuẩn PKCS liên quan}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.50\textwidth}
            \textbf{CSR (PKCS\#10 - RFC 2986):}
            \begin{itemize}
                \item Gói tin chứa thông tin định danh DN, khóa công khai của Client.
                \item Được ký số bởi chính khóa riêng tương ứng để chứng minh quyền sở hữu khóa bí mật (\textit{Proof-of-Possession}), bảo vệ trước việc mạo danh.
            \end{itemize}
            \vspace{0.2cm}
            \textbf{Phân loại theo mức xác thực TLS:}
            \begin{itemize}
                \item \textbf{DV (Domain Validation):} Tự động xác minh quyền sở hữu tên miền.
                \item \textbf{OV (Organization Validation):} Xác minh pháp lý tổ chức thủ công.
                \item \textbf{EV (Extended Validation):} Xác minh nghiêm ngặt cao nhất.
            \end{itemize}
        \end{column}
        \begin{column}{0.48\textwidth}
            \begin{block}{Họ chuẩn mật mã PKCS phổ biến}
                \begin{itemize}
                    \item \textbf{PKCS\#7 (CMS):} Định dạng bao gói dữ liệu mã hóa/ký số (dùng trong chữ ký PDF, S/MIME).
                    \item \textbf{PKCS\#10:} Cấu trúc yêu cầu ký CSR.
                    \item \textbf{PKCS\#12 (PFX):} Định dạng chứa đồng thời khóa riêng, chứng chỉ cá nhân và chuỗi CA, được mã hóa bảo vệ bằng mật khẩu mã hóa mạnh (`.p12` / `.pfx`).
                \end{itemize}
            \end{block}
        \end{column}
    \end{columns}
\end{frame}

% --- 4.5 Ứng dụng PKI thực tế ---
\begin{frame}{Ứng dụng PKI trong thực tế}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.50\textwidth}
            \begin{itemize}
                \item \textbf{HTTPS / TLS 1.3:} Mã hóa kênh truyền web, xác thực máy chủ, tích hợp Certificate Transparency (CT).
                \item \textbf{Ký số văn bản:} Xác thực hóa đơn, văn bản hành chính điện tử. Sử dụng TSA timestamp làm bằng chứng độc lập thời gian.
                \item \textbf{S/MIME:} Ký số và mã hóa email đầu cuối.
                \item \textbf{VPN/IPSec \& Code Signing:} Xác thực gateway/client và xác thực phần mềm sạch.
                \item \textbf{eGovernment Việt Nam:} Trục liên thông quốc gia, NEAC Root CA, Cloud CA Remote Signing.
            \end{itemize}
        \end{column}
        \begin{column}{0.48\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=0.9\textwidth,keepaspectratio]{assets/fig_pki_validation.png}
                \caption{Bộ quy tắc kiểm tra và dựng chuỗi của Client}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% ============================================================
%  PHẦN II: THỰC NGHIỆM & HỆ THỐNG MÃ NGUỒN MỞ
% ============================================================
\section{Phần II: Thực nghiệm \& Hệ thống nguồn mở}

% --- 5.1 Tổng quan Nguồn mở ---
\begin{frame}{Tổng quan Hệ sinh thái PKI Mã nguồn mở}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.52\textwidth}
            \textbf{Phân lớp công cụ thực tiễn:}
            \begin{itemize}
                \item \textbf{Toolkit:} \texttt{OpenSSL} - can thiệp thủ công, tạo khóa, ký CSR. Thiếu quản trị RA và logs.
                \item \textbf{Local GUI:} \texttt{XCA} - quản trị CA trên file SQLite cục bộ (dành cho lab học tập).
                \item \textbf{Enterprise CA Platform:} \texttt{EJBCA} / \texttt{Dogtag} - quản lý profile, tích hợp thiết bị mã hóa cứng HSM (PKCS\#11).
                \item \textbf{Internal PKI:} \texttt{HashiCorp Vault PKI} - cấp cert API nội bộ vòng đời siêu ngắn (TTL tính bằng giờ) cho kiến trúc microservices.
            \end{itemize}
        \end{column}
        \begin{column}{0.45\textwidth}
            \centering
            \begin{figure}
                \centering
                \includegraphics[width=\textwidth,keepaspectratio]{assets/fig_pki_ecosystem.png}
                \caption{Phân lớp hệ sinh thái PKI mã nguồn mở}
            \end{figure}
        \end{column}
    \end{columns}
\end{frame}

% --- 5.2 Triển khai EJBCA trên Docker ---
\begin{frame}{Thực nghiệm: Khởi chạy EJBCA CE trên môi trường Docker}
    \begin{block}{Môi trường Container hóa cho Enterprise CA}
        EJBCA Enterprise / Community Edition chạy trên nền WildFly (Java) cực kỳ phức tạp để cài đặt trực tiếp. Docker cung cấp môi trường khép kín, sẵn sàng tích hợp:
    \end{block}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.54\textwidth}
            \textbf{Lệnh khởi chạy Docker container:}
            \begin{exampleblock}{Docker run EJBCA CE}
                \texttt{docker run -it -d --name ejbca-ce \\}
                \texttt{\quad -p 80:80 -p 443:443 -p 8443:8443 \\}
                \texttt{\quad -e EJBCA\_AUTO\_CREATE\_ADMIN=true \\}
                \texttt{\quad keyfactor/ejbca-ce}
            \end{exampleblock}
            \vspace{0.1cm}
            \textbf{Các cổng dịch vụ hoạt động:}
            \begin{itemize}
                \item \texttt{80 / 443:} Giao diện quản trị, cổng dịch vụ Enroll công cộng.
                \item \texttt{8443:} Cổng mTLS yêu cầu client certificate (quản trị viên cao cấp).
            \end{itemize}
        \end{column}
        \begin{column}{0.42\textwidth}
            \textbf{Kiến trúc triển khai:}
            \begin{itemize}
                \item \textbf{Cơ sở dữ liệu:} SQLite mặc định hoặc kết nối MySQL/PostgreSQL Docker.
                \item \textbf{Quản lý khóa (Crypto Token):} Sử dụng cấu hình SOFT Token mặc định. Hệ thống sinh và bảo vệ khóa mã hóa Root/SubCA trực tiếp bằng thư viện phần mềm tích hợp sẵn của EJBCA thay vì dùng HSM.
            \end{itemize}
        \end{column}
    \end{columns}
\end{frame}

% --- 5.3 Tương tác EJBCA bằng Python ---
\begin{frame}{Thực nghiệm: Tương tác EJBCA REST API bằng Python}
    \begin{block}{Luồng tự động hóa cấp phát chứng chỉ sử dụng Python Client}
        Client sử dụng ngôn ngữ Python giao tiếp trực tiếp với cổng EJBCA REST API để tự động sinh khóa và gửi CSR:
    \end{block}
    \begin{columns}[onlytextwidth]
        \begin{column}{0.50\textwidth}
            \textbf{Bước 1: Sinh khóa \& Tạo CSR trong Python}
            \begin{itemize}
                \item Sử dụng thư viện \texttt{cryptography.hazmat}.
                \item Sinh khóa ECC P-256 hoặc RSA 2048-bit.
                \item Đóng gói DN và ký tạo chuỗi CSR ở dạng PEM.
            \end{itemize}
            \vspace{0.1cm}
            \textbf{Bước 2: Giao tiếp REST API qua HTTP POST}
            \begin{itemize}
                \item Endpoint: \texttt{/ejbca/ejbca-rest-api/}\\\texttt{v1/certificate/pkcs10enroll}
                \item Body JSON chứa: \texttt{certificate\_request} (chuỗi CSR PEM), \texttt{username}, \texttt{password}, và \texttt{certificate\_profile\_name}.
            \end{itemize}
        \end{column}
        \begin{column}{0.48\textwidth}
            \textbf{Bước 3: Tiếp nhận và xử lý của EJBCA}
            \begin{itemize}
                \item EJBCA nhận request, xác thực quyền của End Entity qua API.
                \item Ánh xạ cấu hình Certificate Profile (ràng buộc KeyUsage, EKU, v3 Extensions).
                \item Ký số và trả về chứng chỉ X.509 PEM cho Client Python.
            \end{itemize}
            \vspace{0.1cm}
            \textbf{Bước 4: Sử dụng tại máy khách}
            \begin{itemize}
                \item Python nhận Cert, ghi vào file hoặc đóng gói thành PKCS\#12 phục vụ kết nối mTLS.
            \end{itemize}
        \end{column}
    \end{columns}
\end{frame}

% --- 5.4 Demo PKI Manager CLI & Kết luận ---
\begin{frame}{Thực nghiệm CLI và Kết luận}
    \begin{block}{Thực nghiệm qua PKI Manager CLI}
        Dự án cấu hình công cụ CLI \texttt{pki} trong virtualenv hỗ trợ kết nối API để quản trị CA trực tiếp:
        \begin{itemize}
            \item Tạo CA Root/Intermediate: \texttt{pki ca create --cn "My Root CA"}
            \item Yêu cầu cấp chứng chỉ: \texttt{pki cert issue --ca CA\_ID --cn "web.local" --type server}
            \item Thu hồi chứng chỉ: \texttt{pki cert revoke CERT\_ID --reason keyCompromise}
        \end{itemize}
    \end{block}
    \begin{block}{Kết luận \& Xu hướng mới}
        \begin{itemize}
            \item PKI là giao thoa giữa toán học mật mã, chính sách vận hành và tự động hóa.
            \item \textbf{Zero Trust:} Mutual TLS (mTLS) bắt buộc xác thực hai chiều cho mọi microservice.
            \item \textbf{Hậu lượng tử (Post-Quantum PQC):} NIST chuẩn hóa thuật toán hình học lưới \textbf{ML-KEM} và \textbf{ML-DSA} năm 2024. Đòi hỏi PKI hiện đại chuyển dịch sang tính \textbf{Crypto-Agility} (Linh hoạt mật mã).
        \end{itemize}
    \end{block}
\end{frame}

% --- Q&A ---
\begin{frame}[plain]
    \vfill
    \centering
    \begin{beamercolorbox}[sep=12pt,center,shadow=true,rounded=true]{title}
        \usebeamerfont{title}{\huge XIN CHÂN THÀNH CẢM ƠN!}\\[0.4cm]
        \usebeamerfont{subtitle}{\large PGS. TS. Nguyễn Linh Giang \& Hội đồng}\\
        \vspace{0.4cm}
        \large HỎI \& ĐÁP (Q\&A)
    \end{beamercolorbox}
    \vfill
\end{frame}

\end{document}
"""

pathlib.Path("slide.tex").write_text(code, encoding="utf-8")
print("Clean slide.tex written successfully.")
