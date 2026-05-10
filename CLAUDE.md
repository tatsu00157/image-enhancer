# PhotoTune - CLAUDE.md

## 開発ルール（必ず守ること）

- **作業前に必ず説明する**：何をするのかを先に日本語で説明し、ユーザーの確認を得てから実行する
- **1機能ずつ進める**：1つの機能をブラウザで動作確認できるところまでまとめて作る。ファイル単位ではなく機能単位で区切る
- **動作確認を挟む**：1機能実装したらブラウザで確認してもらい、OKが出てから次へ進む
- **問題の特定をしやすくする**：変更を機能単位に保ち、どこで問題が起きたか追いやすくする
- **コード修正後は必ずCLAUDE.mdを更新してgit commit & pushする**：CLAUDE.mdの開発フェーズの進捗を最新状態に保ち、コミットとプッシュをセットで行う

---

## プロジェクト概要

ぼやけた画像・写真（スクリーンショット含む）を補正して見やすくするWebアプリ。
画像をアップロードし、補正をプレビューで確認後にダウンロードできる。

---

## 技術スタック

| 役割 | 技術 |
|---|---|
| バックエンド | Python / Flask |
| 画像処理（基本） | OpenCV / Pillow |
| 画像処理（AI超解像） | Real-ESRGAN |
| フロントエンド | HTML / CSS / JavaScript |
| 本番環境 | VPS（GPU無し） |
| 開発環境 | Mac（CPU環境） |

---

## ディレクトリ構成

```
image-enhancer/
├── CLAUDE.md
├── requirements.txt
├── app.py                  # Flaskエントリーポイント
├── config.py               # 設定ファイル
├── extensions.py           # Flask-Limiter初期化
├── create_ogp.py           # OGP画像生成スクリプト（再生成用）
├── core/
│   ├── __init__.py
│   ├── brightness.py       # 明るさ・コントラスト補正
│   ├── color.py            # 色調・ホワイトバランス補正
│   ├── sharpen.py          # シャープネス・ぼやけ改善
│   ├── shadow.py           # 影・照明補正
│   └── noise.py            # ノイズ除去
├── api/
│   ├── __init__.py
│   └── routes.py           # APIエンドポイント定義
├── templates/
│   ├── base.html           # 共通レイアウト（ヘッダー・フッター）
│   ├── index.html          # メインページ
│   ├── privacy.html        # プライバシーポリシー
│   ├── terms.html          # 利用規約
│   ├── contact.html        # お問い合わせ
│   └── 404.html            # カスタムエラーページ
├── static/
│   ├── favicon.svg         # ファビコン（魔法の杖）
│   ├── ogp.png             # OGP画像（1200×630px）
│   ├── css/
│   └── js/
└── uploads/                # アップロード一時保存（gitignore対象、起動時自動作成）
```

---

## 機能一覧

### コア補正機能

| 機能 | モジュール | 説明 |
|---|---|---|
| 明るさ・コントラスト調整 | brightness.py | 暗い・明るすぎる写真を補正 |
| 色調・ホワイトバランス | color.py | 蛍光灯・電球の色かぶりを補正 |
| シャープネス強調 | sharpen.py | 輪郭をくっきりさせる |
| 影・照明補正 | shadow.py | CLAHE・HDRトーンマッピング |
| ノイズ除去 | noise.py | ざらつきを滑らかにする |
| AI超解像（オプション） | enhance.py | Real-ESRGANによる画質向上 |

### UI機能

- 画像アップロード（ドラッグ&ドロップ対応）
- 補正前後のプレビュー表示（並べて比較 / スライダー比較の切り替え）
- 各補正のリアルタイムスライダー調整・一括リセット
- ローディングスピナー表示
- 画像の回転・反転
- 出力形式選択（JPG / PNG）
- 補正済み画像のフル解像度ダウンロード
- 使い方説明セクション
- フッター（プライバシーポリシー・利用規約リンク）
- ピンクテーマデザイン（ヘッダーグラデーション + グレー背景 + 白カード）
- サイト名「PhotoTune」・魔法の杖SVGロゴ（ヘッダー左・フッター左）

---

## APIエンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | / | メインページ |
| GET | /privacy | プライバシーポリシー |
| GET | /terms | 利用規約 |
| GET | /contact | お問い合わせ |
| POST | /api/upload | 画像アップロード |
| POST | /api/preview | 補正プレビュー生成（長辺1000px以下にリサイズ） |
| POST | /api/download | 補正済み画像のダウンロード（フル解像度） |
| GET | /uploads/\<filename\> | アップロード済みファイルの配信 |
| GET | /robots.txt | クローラー制御ファイル |
| GET | /sitemap.xml | サイトマップ |

---

## 補正パラメータ仕様

```json
{
  "brightness": 0,        // -100 〜 100
  "contrast": 0,          // -100 〜 100
  "sharpness": 0,         // 0 〜 100
  "noise_reduction": 0,   // 0 〜 100
  "shadow_correction": 0, // 0 〜 100
  "white_balance": "none",// "none" | "auto" | "daylight" | "fluorescent" | "incandescent"
  "rotation": 0,          // 0 | 90 | 180 | 270
  "flip_h": false,        // 左右反転
  "flip_v": false,        // 上下反転
  "format": "jpg"         // "jpg" | "png"（downloadのみ）
}
```

---

## 対応ファイル形式

- 入力：JPG / JPEG / PNG / WEBP
- 出力：JPG / PNG（選択可能）
- 最大ファイルサイズ：20MB

---

## 設計方針・注意点

### パフォーマンス
- CPU環境前提のため、Real-ESRGANはオプション扱い
- プレビューは解像度を落として高速化（長辺1000px以下にリサイズ）
- ダウンロード時にフル解像度で処理

### セキュリティ
- アップロードファイルの拡張子・MIMEタイプを必ず検証
- 一時ファイルはセッション終了後に自動削除
- ファイル名はUUIDに変換して保存

### 商用利用ライセンス確認
- OpenCV：MITライセンス ✅
- Pillow：PILライセンス ✅
- Real-ESRGAN：BSD-3-Clause ✅（商用利用可）
- Flask：BSDライセンス ✅

---

## 開発フェーズ

### Phase 1（最初に作る）✅ 完了
- [x] Flask基本構成
- [x] 画像アップロード・保存
- [x] 明るさ・コントラスト・色調（ホワイトバランス）補正
- [x] プレビュー表示（補正前後の並べて比較・リアルタイム更新）
- [x] ダウンロード機能（フル解像度）

### Phase 2（追加機能）✅ 完了
- [x] 影・照明補正（CLAHE）
- [x] ノイズ除去
- [x] シャープネス強調
- [x] スライダーUIの改善（一括リセット・ローディングスピナー）

### 追加機能 ✅ 完了
- [x] 出力形式の選択（JPG / PNG）
- [x] 画像の回転・反転
- [x] 比較スライダー（補正前後を1枚でドラッグ比較）

### デザイン・ページ整備
- [x] ピンクテーマデザイン（ビジネスイメージカラー）
- [x] 使い方説明セクション（4ステップ）
- [x] ヘッダー・フッター（中央揃え）
- [x] プライバシーポリシーページ（/privacy）
- [x] 利用規約ページ（/terms）
- [x] お問い合わせページ（/contact）：mailto:リンクで開く、件名固定（【PhotoTune】お問い合わせ）、本文に件名削除禁止の案内を記載
- [x] SEO対策：metaディスクリプション・OGPタグ・Twitter Cardを全ページに設定
- [x] OGP画像生成（static/ogp.png、1200×630px、create_ogp.pyで生成）
- [x] robots.txt（/robots.txt）・sitemap.xml（/sitemap.xml）をFlaskルートで配信
- [x] カスタム404ページ（templates/404.html）
- [x] Flaskシークレットキーを環境変数化（SECRET_KEY）
- [x] デバッグモードを環境変数で制御（FLASK_DEBUG=false）
- [x] Gunicorn追加（requirements.txt）
- [x] アップロードファイルの自動削除（30分経過で削除・ダウンロードファイルは即削除）
- [x] MIMEタイプ検証（Pillowのverify()で画像ファイルの内容を検証）
- [x] レートリミット（Flask-Limiter：アップロード10回/分、プレビュー60回/分、ダウンロード10回/分、全体200回/時）
- [x] 429エラーを日本語表示・制限中はリクエスト停止・60秒後に自動解除
- [x] uploads/フォルダを起動時に自動作成（VPS初回デプロイ対応）
- [x] python-dotenv導入（.envを自動読み込み）
- [x] Jinja2テンプレート継承（base.html）
- [x] スライダーパネルとプレビューエリアの高さ統一（object-fit: contain）
- [x] 補正機能の説明をエディタ下にカードグリッド形式で表示
- [x] アップロード前のプレースホルダー表示
- [x] ダウンロードボタンをアップロード前は無効化
- [x] サイト名「PhotoTune」の決定・全テンプレートへの反映
- [x] 魔法の杖SVGロゴをヘッダー・フッターに追加
- [x] ボディ背景をグレー（#f4f4f6）に変更、カードを白（#fff）で統一
- [x] プライバシー・利用規約ページを白カードで囲みメインページと統一
- [x] ファビコン設定（static/favicon.svg、魔法の杖ロゴと同デザイン）
- [x] レスポンシブ対応（スマホ表示）
  - 768px以下でスライダーパネル・プレビューを縦並びに切り替え
  - スマホではプレビューエリアを画面上部にスティッキー固定（スクロールしながら調整可能）
  - 比較スライダーはobject-fitを使わずコンテナ側でクリップ（非正方形画像のズレを防止）

### Phase 3（将来対応）
- [ ] Real-ESRGAN超解像の組み込み（GPU環境必要）
- [ ] 動画対応（フレーム単位で画像補正を適用）
- [ ] VPSデプロイ対応

---

## 開発環境セットアップ

```bash
# 仮想環境作成
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# 依存関係インストール
pip install -r requirements.txt

# 開発サーバー起動
python3 app.py
```

---

## requirements.txt

```
Flask==3.0.3
gunicorn==22.0.0
python-dotenv==1.0.1
Flask-Limiter==3.8.0
opencv-python==4.9.0.80
Pillow==10.3.0
numpy==1.26.4
```
