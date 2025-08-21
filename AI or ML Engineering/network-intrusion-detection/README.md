    ## Network Intrusion Detection (CyberGuard)

    Flask web app with a two-stage ML pipeline:
    - Binary classifier (Normal vs Attack)
    - Multiclass classifier (9 attack categories) when an attack is detected

    Optionally integrates an LLM (Groq) to generate mitigation guidance; falls back to curated templates when no API key is provided.

    ## Project Structure

    ```
    network-intrusion-detection/
    ├── app.py                 # Flask app bootstrap (loads models, registers routes)
    ├── routes.py              # UI + API endpoints
    ├── config.py              # App and model configuration
    ├── models_utils.py        # Encoders, model loading, preprocessing
    ├── models/
    │   ├── binary/
    │   │   ├── binary_classifiers_model.joblib
    │   │   ├── target_encoder.pkl
    │   │   └── feature_config.json
    │   └── multiclass/
    │       ├── multiclass_gradientboosting_model.joblib
    │       ├── multiclass_target_encoder.pkl
    │       ├── feature_config.json
    │       └── preprocessor.joblib           # optional
    ├── static/ templates/                    # frontend
    └── requirements.txt
    ```

    Model file names are enforced by `models_utils.load_model_ecosystem`.

    ## Requirements
    - Python 3.10+
    - Packages in `requirements.txt`

    ## Setup (Windows PowerShell)
    1) Create venv and install deps
    ```
    python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
    ```
    2) Place model artifacts
    - Binary: `models/binary/binary_classifiers_model.joblib`, `models/binary/target_encoder.pkl`, `models/binary/feature_config.json`
    - Multiclass: `models/multiclass/multiclass_gradientboosting_model.joblib`, `models/multiclass/multiclass_target_encoder.pkl`, `models/multiclass/feature_config.json` (+ optional `preprocessor.joblib`)

    3) (Optional) Configure Groq API for mitigation text
    ```
    $env:GROQ_API_KEY = "your_groq_api_key"
    ```

    4) Run the app
    ```
    python app.py
    ```
    Open http://localhost:5000

    ## Routes
    - GET `/` → landing page (`pages/cyberguard-landing.html`)
    - GET `/predict` → prediction UI
    - GET `/instructions` → instructions page
    - GET `/metodologi` → methodology page
    - GET `/inovasi` → innovation page
    - GET `/get_sample_data/<normal|attack>` → sample JSON payloads
    - POST `/predict` → prediction API

    ### Prediction API
    Accepts form-encoded or JSON. Minimally requires the feature set expected by the model configs.

    Numeric fields include (subset):
    `dur, rate, spkts, dpkts, sbytes, dbytes, sttl, dttl, sload, dload, dloss, sinpkt, dinpkt, sjit, djit, swin, dwin, stcpb, dtcpb, tcprtt, synack, ackdat, smean, dmean, trans_depth, response_body_len, ct_srv_src, ct_state_ttl, ct_dst_ltm, ct_src_dport_ltm, ct_dst_sport_ltm, ct_dst_src_ltm, ct_src_ltm, ct_srv_dst, is_ftp_login, ct_ftp_cmd, ct_flw_http_mthd, is_sm_ips_ports`

    Categorical fields:
    `proto` (target-encoded), `service`, `state`

    Response example:
    ```
    {
        "binary_prediction": "Attack",
        "binary_confidence": 92.4,
        "is_attack": true,
        "multiclass_prediction": "Exploits",
        "multiclass_confidence": 81.2,
        "attack_type": "Exploits",
        "mitigation": { ... },
        "pipeline_status": "complete",
        "timestamp": "2025-08-20T12:34:56Z"
    }
    ```

    ## Notes on Preprocessing
    - `proto` is encoded via custom TargetEncoder/MulticlassTargetEncoder.
    - Binary config excludes `sloss`; multiclass may require categorical preprocessing (uses `preprocessor.joblib` when present, otherwise falls back to simple encoding).
    - Missing features are auto-filled with safe defaults where possible; best results require matching `feature_config.json`.

    ## Troubleshooting
    - Models not loading: verify exact filenames and paths under `models/binary` and `models/multiclass`.
    - Feature mismatch: ensure request fields align with `feature_config.json` and required categorical fields exist.
    - Groq unavailable: app uses template-based mitigations from `Config.FALLBACK_MITIGATIONS`.
    - Port conflict: edit `app.py` to change port.

    ## License
    Educational use.
