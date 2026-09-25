# European Banking Churn Analytics

Streamlit dashboard split into separate modules.

## Structure

```text
project_root/
├── app.py
├── European_Bank.csv
└── dashboard/
    ├── __init__.py          # optional, if using a regular Python package
    ├── config.py
    ├── data.py
    ├── filters.py
    ├── metrics.py
    └── tabs/
        ├── __init__.py      # optional, if using a regular Python package
        ├── overall.py
        ├── geography.py
        ├── age_tenure.py
        └── high_value.py
```

Put `European_Bank.csv` beside `app.py`, then run:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```
## Research paper
https://drive.google.com/file/d/1OZiu6YCVc-Zmpw6vGPqtMdWE7zgeJ4a_/view?usp=drive_link
