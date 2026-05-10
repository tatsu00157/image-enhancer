from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)

# 左上(#e91e8c) → 右下(#f48cbf) の135degグラデーション
for y in range(H):
    for x in range(W):
        t = (x / W + y / H) / 2
        r = int(233 + (244 - 233) * t)
        g = int(30  + (140 - 30)  * t)
        b = int(140 + (191 - 140) * t)
        draw.point((x, y), fill=(r, g, b))

# 半透明の白い装飾円
overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
od.ellipse([820, -160, 1360, 380], fill=(255, 255, 255, 20))
od.ellipse([900, 300, 1300, 700], fill=(255, 255, 255, 15))
od.ellipse([-100, 400, 300, 800], fill=(255, 255, 255, 12))
img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
draw = ImageDraw.Draw(img)

# フォント候補（日本語対応）
font_candidates = [
    '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/Library/Fonts/Arial Bold.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
]

def load_font(size):
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_logo    = load_font(110)
font_tagline = load_font(42)
font_sub     = load_font(30)

# ロゴ「PhotoTune」
logo_text = 'PhotoTune'
bbox = draw.textbbox((0, 0), logo_text, font=font_logo)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) / 2, 180), logo_text, font=font_logo, fill=(255, 255, 255))

# タグライン
tag_text = '写真・画像をかんたんに補正・ダウンロード'
bbox2 = draw.textbbox((0, 0), tag_text, font=font_tagline)
tw2 = bbox2[2] - bbox2[0]
draw.text(((W - tw2) / 2, 330), tag_text, font=font_tagline, fill=(255, 255, 255, 220))

# サブテキスト
sub_text = 'JPG / PNG / WEBP 対応 — 無料で使えるWebツール'
bbox3 = draw.textbbox((0, 0), sub_text, font=font_sub)
tw3 = bbox3[2] - bbox3[0]
draw.text(((W - tw3) / 2, 415), sub_text, font=font_sub, fill=(255, 255, 255, 180))

# 下部に細い白ライン
draw.rectangle([80, 510, W - 80, 513], fill=(255, 255, 255, 120))

out_path = os.path.join(os.path.dirname(__file__), 'static', 'ogp.png')
img.save(out_path, 'PNG')
print(f'OGP画像を保存しました: {out_path}')
