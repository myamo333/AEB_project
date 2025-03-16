# 🚗 AEB Project (Automatic Emergency Braking with CARLA)

このプロジェクトは、CARLA シミュレーターを用いた **自動緊急ブレーキ（AEB: Automatic Emergency Braking）** の実装です。  

---

## 🛠️ 環境構築

### 1️⃣ **必要なソフトウェア**
- [CARLA Simulator](https://carla.org/)（バージョン 0.9.x 推奨）
- Python 3.7 以上
- `pip`（Python パッケージマネージャ）

### 2️⃣ **Python ライブラリのインストール**
以下のコマンドを実行して、必要な Python ライブラリをインストールしてください。

```sh
pip install -r requirements.txt
```

> **⚠️ 注意**: `requirements.txt` がない場合は、手動で以下のライブラリをインストールしてください。
```sh
pip install numpy opencv-python carla
```

### 3️⃣ **CARLA サーバーの起動**
CARLA シミュレーターを実行するために、以下のコマンドをターミナルで実行してください。

```sh
./CarlaUE4.sh -opengl  # Linux/macOS
CarlaUE4.exe           # Windows
```

---

## 🚀 実行方法

1. CARLA シミュレーターを起動
2. 別のターミナルで、プロジェクトのルートディレクトリに移動し、以下のコマンドを実行

```sh
python main.py
```

> `work/output.mp4` にドライブの様子が録画されます。  

---

## 📁 プロジェクト構成

```
AEB_project/
│── main.py                 # メインスクリプト
├── src/                     # モジュール（サブスクリプト）
    ├── camera.py            # カメラ処理
    ├── radar.py             # レーダー処理
    ├── vehicle_control.py    # 車両制御
```

---

## ⚙️ モジュール説明

### **📷 camera.py**
- カメラセンサーをセットアップし、画像を取得
- `output.mp4` に映像を保存

### **📡 radar.py**
- レーダーセンサーをセットアップ
- 前方の車両との距離を測定し、`main.py` に情報を提供

### **🚗 vehicle_control.py**
- 車両の速度を制御
- **AEB（自動緊急ブレーキ）** を適用

---

## 📝 TODO（今後の改善点）
- ✅ コードをモジュール化（`camera.py`, `radar.py`, `vehicle_control.py`）
- 📌 カメラでのオブジェクト検知
- 📌 走行ログを保存し、分析可能にする

---