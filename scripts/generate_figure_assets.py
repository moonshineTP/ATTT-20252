"""
Generate clean PNG diagrams for the PKI report (report/assets/).
Run:  C:\\Users\\ADMIN\\miniconda3\\python.exe scripts\\generate_figure_assets.py
"""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BASE = pathlib.Path(__file__).parent.parent
ASSETS = BASE / "report" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

BLUE = "#0C447C"
LIGHT = "#F4F8FC"
GRAY = "#666666"
RED = "#C0392B"
GREEN = "#1E8449"
ORANGE = "#D35400"

# Layout rhythm — keep spacing consistent across all figures.
BOX_PAD = 0.04          # inner text padding in rounded boxes
ARROW_GAP = 0.10        # gap between arrow tip and box edge
LABEL_GAP = 0.14        # offset for edge labels on arrows
ROW_GAP = 0.45          # vertical gap between stacked boxes
COL_GAP = 0.55          # horizontal gap between adjacent boxes
MARGIN = 0.55           # canvas margin


def _setup(figsize, x_max, y_max, equal_aspect=False):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    if equal_aspect:
        ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    return fig, ax


def _box(ax, xy, w, h, text, fc=LIGHT, ec=BLUE, fs=9, weight="normal"):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad={BOX_PAD},rounding_size=0.10",
        linewidth=1.3,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        weight=weight,
        linespacing=1.25,
    )
    return (x, y, w, h)


def _edge(box, side, gap=0.0):
    x, y, w, h = box
    if side == "top":
        return (x + w / 2, y + h + gap)
    if side == "bottom":
        return (x + w / 2, y - gap)
    if side == "left":
        return (x - gap, y + h / 2)
    if side == "right":
        return (x + w + gap, y + h / 2)
    raise ValueError(side)


def _arrow(
    ax,
    p1,
    p2,
    text="",
    color=GRAY,
    style="-|>",
    rad=0.0,
    lw=1.3,
    label_pos=0.5,
    label_offset=(0, 0.08),
):
    arr = FancyArrowPatch(
        p1,
        p2,
        arrowstyle=style,
        mutation_scale=13,
        linewidth=lw,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_patch(arr)
    if text:
        mx = p1[0] + (p2[0] - p1[0]) * label_pos + label_offset[0]
        my = p1[1] + (p2[1] - p1[1]) * label_pos + label_offset[1]
        ax.text(mx, my, text, ha="center", va="center", fontsize=7.5, color=color)


def _link(
    ax,
    b1,
    side1,
    b2,
    side2,
    text="",
    color=GRAY,
    rad=0.0,
    gap=ARROW_GAP,
    **kwargs,
):
    _arrow(ax, _edge(b1, side1, gap), _edge(b2, side2, gap), text, color, rad=rad, **kwargs)


def _row(ax, y, boxes_spec, gap=COL_GAP):
    """Place boxes in a horizontal row, centered on canvas width x_max."""
    widths = [spec[0] for spec in boxes_spec]
    total = sum(widths) + gap * (len(boxes_spec) - 1)
    x = MARGIN
    placed = []
    for w, text, kw in boxes_spec:
        kw.setdefault("fs", 9)
        placed.append(_box(ax, (x, y), w, kw.pop("h", 0.78), text, **kw))
        x += w + gap
    return placed, total


def _stack(ax, x, w, labels, y_top, h=0.72, gap=ROW_GAP, **box_kw):
    """Vertical stack of equal-width boxes."""
    boxes = []
    y = y_top
    for label in labels:
        boxes.append(_box(ax, (x, y - h), w, h, label, **box_kw))
        y -= h + gap
    return boxes


def _save(fig, name: str) -> None:
    path = ASSETS / name
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white", pad_inches=0.25)
    plt.close(fig)
    print(f"  OK  {name} ({path.stat().st_size:,} bytes)")


def fig_mitm() -> None:
    fig, ax = _setup((9.0, 2.8), 11, 3.2)
    h = 0.85
    y = 1.15
    alice = _box(ax, (0.8, y), 1.7, h, "Alice", fc="#E8F5E9", ec=GREEN)
    mallory = _box(ax, (4.35, y), 2.0, h, "Mallory", fc="#FDEDEC", ec=RED)
    bob = _box(ax, (8.3, y), 1.7, h, "Bob", fc="#E8F5E9", ec=GREEN)
    _link(ax, alice, "right", mallory, "left", "KP giả", RED, label_offset=(0, 0.12))
    _link(ax, mallory, "right", bob, "left", "KP giả", RED, label_offset=(0, 0.12))
    _arrow(
        ax,
        _edge(alice, "bottom", 0.05),
        _edge(bob, "bottom", 0.05),
        "kênh thật bị chặn",
        GRAY,
        style="-",
        rad=-0.22,
        label_offset=(0, -0.18),
    )
    _save(fig, "fig_mitm.png")


def fig_pki_ca() -> None:
    fig, ax = _setup((8.5, 3.8), 10, 4.2)
    ca = _box(ax, (3.4, 2.85), 3.2, 0.85, "Root / Int CA", fc=LIGHT, ec=BLUE, weight="bold")
    client = _box(ax, (0.7, 0.55), 2.0, 0.85, "Client")
    server = _box(ax, (7.3, 0.55), 2.0, 0.85, "Máy chủ")
    _link(ax, ca, "bottom", server, "top", "ký chứng chỉ", rad=-0.08, label_offset=(0.35, 0))
    _link(ax, client, "right", server, "left", "cert + kiểm tra chuỗi", label_offset=(0, 0.12))
    _link(ax, client, "top", ca, "bottom", "trust anchor", rad=0.12, label_offset=(-0.35, 0))
    _save(fig, "fig_pki_ca.png")


def fig_pki_hierarchy() -> None:
    fig, ax = _setup((10.0, 4.2), 11.2, 4.5)
    root = _box(ax, (4.1, 3.35), 3.0, 0.82, "Root CA (trust anchor)", fc=LIGHT, ec=BLUE, weight="bold")
    ia1 = _box(ax, (1.2, 2.05), 2.5, 0.78, "Intermediate CA")
    ia2 = _box(ax, (7.5, 2.05), 2.5, 0.78, "Intermediate CA")
    l1 = _box(ax, (0.65, 0.55), 2.0, 0.68, "Leaf cert", fs=8)
    l2 = _box(ax, (2.95, 0.55), 2.0, 0.68, "Leaf cert", fs=8)
    l3 = _box(ax, (6.95, 0.55), 2.0, 0.68, "Leaf cert", fs=8)
    l4 = _box(ax, (9.25, 0.55), 1.7, 0.68, "Leaf cert", fs=8)
    _link(ax, root, "bottom", ia1, "top", rad=0.08)
    _link(ax, root, "bottom", ia2, "top", rad=-0.08)
    _link(ax, ia1, "bottom", l1, "top")
    _link(ax, ia1, "bottom", l2, "top", rad=-0.06)
    _link(ax, ia2, "bottom", l3, "top", rad=0.06)
    _link(ax, ia2, "bottom", l4, "top")
    _save(fig, "fig_pki_hierarchy.png")


def fig_digital_signature() -> None:
    fig, ax = _setup((10.5, 3.4), 11.5, 3.2)
    sign_y = 1.85
    verify_y = 0.45
    h = 0.72
    ax.text(MARGIN, 2.75, "Ký số", fontsize=10, weight="bold", color=BLUE)
    ax.text(MARGIN, 1.35, "Xác thực", fontsize=10, weight="bold", color=BLUE)
    m = _box(ax, (MARGIN, sign_y), 1.55, h, "Thông điệp M")
    hash_m = _box(ax, (2.55, sign_y), 1.65, h, "H = Hash(M)")
    sig = _box(ax, (4.7, sign_y), 2.15, h, "Sig = E(KR, H)", fc=LIGHT, ec=BLUE)
    m2 = _box(ax, (MARGIN, verify_y), 1.55, h, "Nhận M'")
    hash_m2 = _box(ax, (2.55, verify_y), 1.65, h, "H' = Hash(M')")
    verify = _box(ax, (4.7, verify_y), 2.55, h, "H' = D(KP, Sig)?", fc="#E8F8F5", ec=GREEN)
    _link(ax, m, "right", hash_m, "left")
    _link(ax, hash_m, "right", sig, "left")
    _link(ax, m2, "right", hash_m2, "left")
    _link(ax, hash_m2, "right", verify, "left")
    _link(ax, sig, "bottom", verify, "top", "gửi kèm Sig", label_offset=(0.25, 0))
    _save(fig, "fig_digital_signature.png")


def fig_pki_components() -> None:
    fig, ax = _setup((9.5, 4.0), 10.5, 4.0)
    y_main = 2.05
    h = 0.82
    ee = _box(ax, (0.4, y_main), 1.65, h, "End entity")
    ra = _box(ax, (2.55, y_main), 1.35, h, "RA", fc=LIGHT, ec=BLUE)
    ca = _box(ax, (4.45, y_main), 1.35, h, "CA", fc=LIGHT, ec=BLUE)
    ocsp = _box(ax, (6.85, 2.75), 2.05, h, "OCSP / CRL", fs=8)
    repo = _box(ax, (6.85, 0.55), 2.25, h, "Repository\n(LDAP/HTTP)", fs=8)
    _link(ax, ee, "right", ra, "left", "CSR", label_offset=(0, 0.12))
    _link(ax, ra, "right", ca, "left", "đã xác minh", label_offset=(0, 0.12))
    _link(ax, ca, "right", repo, "left", "publish", rad=0.10, label_offset=(0, -0.05))
    _link(ax, ca, "right", ocsp, "left", "revocation", rad=-0.10, label_offset=(0, 0.05))
    _link(ax, ee, "bottom", repo, "left", "truy vấn", rad=0.18, label_offset=(-0.1, 0))
    _save(fig, "fig_pki_components.png")


def fig_cert_lifecycle() -> None:
    steps = [
        ("1. Tạo khóa", LIGHT, BLUE),
        ("2. CSR", LIGHT, BLUE),
        ("3. Xác minh", LIGHT, BLUE),
        ("4. Cấp cert", LIGHT, BLUE),
        ("5. Sử dụng", LIGHT, BLUE),
        ("6. Gia hạn /\nThu hồi", "#FDEBD0", ORANGE),
    ]
    fig, ax = _setup((11.0, 2.0), 13.0, 1.7)
    x = MARGIN
    h = 0.72
    y = 0.55
    gap = 0.42
    boxes = []
    for i, (label, fc, ec) in enumerate(steps):
        w = 1.55 if i < 5 else 2.05
        boxes.append(_box(ax, (x, y), w, h, label, fc=fc, ec=ec, fs=8))
        x += w + gap
    for i in range(len(boxes) - 1):
        _link(ax, boxes[i], "right", boxes[i + 1], "left", gap=0.06)
    _save(fig, "fig_cert_lifecycle.png")


def fig_x509() -> None:
    fig, ax = _setup((8.5, 3.4), 8.5, 3.8)
    w = 7.0
    x = 0.75
    h1, h2 = 0.95, 0.72
    gap = ROW_GAP
    sig = _box(ax, (x, 0.45), w, h2, "signatureValue (chữ ký CA lên tbs)", fs=8)
    alg = _box(ax, (x, 0.45 + h2 + gap), w, h2, "signatureAlgorithm (vd. sha256WithRSA)", fs=8)
    tbs = _box(
        ax,
        (x, 0.45 + h2 + gap + h2 + gap),
        w,
        h1,
        "tbsCertificate: version, serial, issuer, validity, subject,\n"
        "subjectPublicKeyInfo, extensions",
        fc=LIGHT,
        ec=BLUE,
        fs=8,
    )
    _arrow(
        ax,
        (x - 0.35, _edge(tbs, "bottom", 0.02)[1]),
        (x - 0.35, _edge(sig, "top", 0.02)[1]),
        color=BLUE,
        lw=1.6,
    )
    ax.text(
        x - 0.58,
        (tbs[1] + sig[1] + sig[3]) / 2,
        "CA\nký",
        fontsize=7.5,
        color=BLUE,
        ha="center",
        va="center",
    )
    _save(fig, "fig_x509.png")


def fig_tls() -> None:
    msgs = [
        ("1. ClientHello", "#EEEEEE", GRAY),
        ("2. ServerHello + Certificate (+ chain)", LIGHT, BLUE),
        ("3. Client: kiểm tra chuỗi, SAN, thời hạn, thu hồi", "#EEEEEE", GRAY),
        ("4. Hoàn tất bắt tay TLS", LIGHT, BLUE),
    ]
    fig, ax = _setup((8.5, 4.0), 8.5, 4.2)
    w = 7.0
    x = 0.75
    h = 0.62
    gap = 0.38
    boxes = []
    y = 3.35
    for txt, fc, ec in msgs:
        boxes.append(_box(ax, (x, y - h), w, h, txt, fc=fc, ec=ec, fs=8))
        y -= h + gap
    for i in range(len(boxes) - 1):
        _link(ax, boxes[i], "bottom", boxes[i + 1], "top", gap=0.08)
    _save(fig, "fig_tls_handshake.png")


def fig_validation() -> None:
    fig, ax = _setup((8.5, 4.2), 9.0, 4.5)
    chain_x = 2.55
    cw = 2.6
    h = 0.78
    gap = ROW_GAP
    root = _box(ax, (chain_x, 3.35), cw, h, "Root CA (trust store)", fc=LIGHT, ec=BLUE, weight="bold")
    inter = _box(ax, (chain_x + 0.15, 3.35 - h - gap), cw - 0.3, h, "Intermediate CA")
    leaf = _box(ax, (chain_x + 0.15, 3.35 - 2 * (h + gap)), cw - 0.3, h, "Leaf cert (dịch vụ)")
    client = _box(ax, (6.35, 1.95), 1.85, 1.05, "Client\n(kiểm tra)", fs=8)
    _link(ax, root, "bottom", inter, "top", "ký", label_offset=(0.22, 0))
    _link(ax, inter, "bottom", leaf, "top", "ký", label_offset=(0.22, 0))
    _link(ax, client, "left", inter, "right", "dựng chuỗi", label_offset=(0, 0.1))
    _link(ax, client, "left", leaf, "right", "SAN, EKU,\nthời hạn", rad=-0.12, label_offset=(-0.12, 0))
    _save(fig, "fig_pki_validation.png")


def fig_ct() -> None:
    fig, ax = _setup((9.5, 3.6), 10.5, 3.6)
    h = 0.85
    y = 1.35
    ca = _box(ax, (0.6, y), 1.55, h, "CA", fc=LIGHT, ec=BLUE)
    log = _box(ax, (3.15, y), 2.25, h, "CT Log\n(append-only)", fc="#FFF9E6", ec=ORANGE)
    monitor = _box(ax, (6.85, 0.45), 2.15, h, "Monitor / SCT", fs=8)
    owner = _box(ax, (6.85, 2.35), 2.35, h, "Chủ miền /\nTrình duyệt", fs=8)
    _link(ax, ca, "right", log, "left", "ghi cert", label_offset=(0, 0.12))
    _link(ax, log, "right", monitor, "left", "Merkle proof", rad=0.12, label_offset=(0, -0.05))
    _link(ax, log, "right", owner, "left", "cảnh báo", rad=-0.12, label_offset=(0, 0.05))
    _save(fig, "fig_ct.png")


def fig_ecosystem() -> None:
    layers = [
        ("Lớp 1 — OpenSSL, CFSSL: cryptographic toolkit", "#E8F8F5"),
        ("Lớp 2 — XCA: quản trị cục bộ / lab", "#FFFDE7"),
        ("Lớp 3 — Let's Encrypt + Certbot: ACME / Web PKI", LIGHT),
        ("Lớp 4 — EJBCA, Dogtag: CA doanh nghiệp", "#FDEBD0"),
        ("Lớp 5 — Vault PKI: internal / mTLS", "#F4ECF7"),
    ]
    fig, ax = _setup((8.5, 4.2), 8.5, 4.0)
    w = 7.2
    x = 0.65
    h = 0.58
    gap = 0.32
    boxes = []
    y = 3.35
    for txt, fc in layers:
        boxes.append(_box(ax, (x, y - h), w, h, txt, fc=fc, ec=BLUE, fs=8))
        y -= h + gap
    for i in range(len(boxes) - 1):
        _link(ax, boxes[i], "bottom", boxes[i + 1], "top", gap=0.06)
    _save(fig, "fig_pki_ecosystem.png")


def main() -> None:
    print(f"Writing to {ASSETS}")
    fig_mitm()
    fig_pki_ca()
    fig_pki_hierarchy()
    fig_digital_signature()
    fig_pki_components()
    fig_cert_lifecycle()
    fig_x509()
    fig_tls()
    fig_validation()
    fig_ct()
    fig_ecosystem()
    print("Done.")


if __name__ == "__main__":
    main()
