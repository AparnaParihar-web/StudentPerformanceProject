0. cd StudentPerformanceProject

1. Activate venv:
```powershell
. .\.venv\Scripts\Activate.ps1
```

2. Quick read test:
```powershell
py -3 src/test_data_read.py
```

3. Process sample file (creates Data/processed_sample_data.xlsx):
```powershell
py -3 -c "from src.data_processing import read_input, compute_totals_and_percentage, save_processed; df=read_input(); save_processed(compute_totals_and_percentage(df))"
# or
py -3 src/data_processing.py
```

4. Launch Streamlit:
```powershell
streamlit run src/main.py
```
