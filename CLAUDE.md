# 画像補正Webアプリ - CLAUDE.md

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
├── README.md
├── requirements.txt
├── app.py                  # Flaskエントリーポイント
├── config.py               # 設定ファイル
├── core/
│   ├── __init__.py
│   ├── brightness.py       # 明るさ・コントラスト補正
│   ├── color.py            # 色調・ホワイトバランス補正
│   ├── sharpen.py          # シャープネス・ぼやけ改善
│   ├── shadow.py           # 影・照明補正
│   ├── noise.py            # ノイズ除去
│   └── enhance.py          # Real-ESRGAN超解像（オプション）
├── api/
│   ├── __init__.py
│   └── routes.py           # APIエンドポイント定義
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
└── uploads/                # アップロード一時保存（gitignore対象）
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
- 補正前後のプレビュー表示（並べて比較）
- 各補正のスライダー調整
- 補正済み画像のダウンロード

---

## APIエンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| POST | /api/upload | 画像アップロード |
| POST | /api/preview | 補正プレビュー生成 |
| POST | /api/download | 補正済み画像のダウンロード |
| DELETE | /api/cleanup | 一時ファイル削除 |

---

## 補正パラメータ仕様

```json
{
  "brightness": 0,        // -100 〜 100
  "contrast": 0,          // -100 〜 100
  "sharpness": 0,         // 0 〜 100
  "noise_reduction": 0,   // 0 〜 100
  "shadow_correction": 0, // 0 〜 100
  "white_balance": "auto" // "auto" | "daylight" | "fluorescent" | "incandescent"
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

### Phase 2（追加機能）
- [x] 影・照明補正（CLAHE）
- [x] ノイズ除去
- [x] シャープネス強調
- [x] スライダーUIの改善（一括リセット・ローディングスピナー）

### Phase 3（将来対応）
- [ ] Real-ESRGAN超解像の組み込み
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

## requirements.txt（予定）

```
Flask==3.0.0
opencv-python==4.9.0.80
Pillow==10.2.0
numpy==1.26.4
```
