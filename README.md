# 🧠 ThePredictor - Backend

A modular FastAPI backend for stock market analysis using price action and machine learning.
Supports real-time scanner execution, deep learning model training, prediction, and flexible stock-level insights.

---

## 🚀 Features
- 44MA, Fibonacci, RSI scanner APIs
- Historical data fetch (single/batch)
- Preprocessing with feature engineering + support/resistance detection
- Deep learning model training (per-stock or multi-stock)
- Flexible inference system with chart integration
- Full modular structure for future extension

---

## 🏗️ Folder Structure
```
backend/
├── data/                         # Contains instruments_nse.csv
├── raw_stock_data/              # Historical raw stock CSVs
├── processed_stock_dataset/     # Preprocessed stock files with features + labels
├── combined_dataset/            # Merged & encoded train-ready dataset
├── ml/
│   ├── data_collection/         # Data fetch logic
│   ├── data_preprocess/         # Feature engineering, labeling
│   ├── train/                   # Model training
│   ├── predict/                 # Inference logic
│   └── models/                  # Saved models per stock/global
├── route/                       # FastAPI routes
├── scanner/                     # Scanner utilities + logic
└── main.py                      # FastAPI entry point
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment setup
Create a `.env` file with:
```env
API_KEY=your_kiteconnect_key
API_SECRET=your_kiteconnect_secret
```

### 3. Start server
```bash
uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

---

## 🧪 Key Endpoints (Scanners)
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/scanner/run_all_scanners_on_all` | Run all scanners on pre-defined stock list |
| GET | `/scanner/run_all_scanners_on_stock/{symbol}` | Run all scanners for a specific stock |
| GET | `/scanner/run_single_scan_all/{scan_type}` | Run a specific scan (e.g., 44MA) on all stocks |
| GET | `/scanner/run_scan_on_all_nse/{scan_type}` | Run scan on all NSE stocks from CSV |

---

## 🤖 ML Endpoints
### 🔄 Data Collection
| Route | Description |
|-------|-------------|
| `/ml/fetch_single?symbol=TCS` | Fetch historical data for 1 stock |
| `/ml/fetch_batch` | Fetch for all pre-defined stocks |

### 🔧 Preprocessing
| Route | Description |
|-------|-------------|
| `/ml/preprocess_stock?symbol=TCS` | Preprocess single stock |
| `/ml/preprocess_all` | Preprocess all stocks |
| `/ml/merge_encode` | Merge all processed into final dataset |

### 🧠 Model Training
| Route | Description |
|-------|-------------|
| `/ml/train_single?symbol=TCS` | Train model only on TCS |
| `/ml/train_multi` | Train global model on all |
| `/ml/models` | List trained models & metadata |

### 📈 Prediction
| Route | Description |
|-------|-------------|
| `POST /ml/predict?symbol=TCS` | Predict using latest preprocessed data |
| `POST /ml/predict` (file upload) | Upload CSV and run prediction |

---

## 🐳 Docker (Optional)

### Dockerfile
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run
```bash
docker build -t predictor-backend .
docker run -p 8000:8000 predictor-backend
```

---

## 🧠 Notes
- You must log in with KiteConnect to get access token before fetching data.
- All scanner output CSVs are saved under `/scanner/output/`.
- Models are saved in `ml/models/{SYMBOL}/` or `ml/models/global/`

---

## ✨ Credits
Made with ❤️ and pure price action conviction by me + ChatGPT

---
