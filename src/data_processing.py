import pandas as pd

def read_input(path='Data/sample_data.xlsx'):
    return pd.read_excel(path)

def compute_totals_and_percentage(df, subjects=None):
    df = df.copy()
    if subjects is None:
        subjects = [c for c in df.columns if c not in ('Roll_No','Name','Attendance(%)')]
    for s in subjects:
        df[s] = pd.to_numeric(df[s], errors='coerce').fillna(0)
    df['Total'] = df[subjects].sum(axis=1)
    max_total = len(subjects) * 100
    df['Percentage'] = (df['Total']/max_total)*100
    df['Percentage'] = df['Percentage'].round(2)
    df['Grade'] = df['Percentage'].apply(lambda p: 'A+' if p>=90 else 'A' if p>=75 else 'B' if p>=60 else 'C' if p>=40 else 'F')
    return df

def save_processed(df, out_path='Data/processed_sample_data.xlsx'):
    df.to_excel(out_path, index=False)

if __name__ == '__main__':
    df = read_input()
    df2 = compute_totals_and_percentage(df)
    save_processed(df2)
    print('Processed file saved')