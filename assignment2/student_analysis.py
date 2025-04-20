# student_analysis.py

import pandas as pd
from collections import defaultdict

def _load_and_preprocess(path):

    df = pd.read_csv(path)
    df = df.rename(columns={'Attendance (%)': 'Attendance'})
    df['Attendance'] = pd.to_numeric(df['Attendance'], errors='coerce')
    df['Project Submitted'] = (
        df['Project Submitted']
          .astype(str)
          .str.strip()
          .str.upper()
          .eq('TRUE')
    )
    return df

def get_toppers(path):
    df = _load_and_preprocess(path)
    # eligibility filter
    eligible = df[(df['Attendance'] >= 60) & (df['Project Submitted'])]
    
    subjects = ['Math', 'Science', 'English']
    toppers = {}
    
    # subject-wise
    for sub in subjects:
        max_sc = eligible[sub].max()
        names = eligible.loc[eligible[sub] == max_sc, 'Name'].tolist()
        toppers[sub] = {'score': float(max_sc), 'students': names}
    
    # overall by average of the three
    eligible = eligible.copy()
    eligible['__avg__'] = eligible[subjects].mean(axis=1)
    max_avg = eligible['__avg__'].max()
    names = eligible.loc[eligible['__avg__'] == max_avg, 'Name'].tolist()
    toppers['Overall'] = {'average_score': float(max_avg), 'students': names}
    
    return toppers

def enrich_student_data(path):
    df = _load_and_preprocess(path)
    
    # average
    df['Average Score'] = df[['Math','Science','English']].mean(axis=1)
    
    # grade
    def _grade(avg):
        if avg >= 90:     return 'A'
        elif avg >= 75:   return 'B'
        elif avg >= 60:   return 'C'
        else:             return 'D'
    df['Grade'] = df['Average Score'].apply(_grade)
    
    # performance
    def _perf(row):
        if row['Grade']=='A' and row['Attendance'] > 90 and row['Project Submitted']:
            return 'Excellent'
        if row['Grade']=='D' or not row['Project Submitted'] or row['Attendance'] < 60:
            return 'Needs Attention'
        return 'Satisfactory'
    
    df['Performance'] = df.apply(_perf, axis=1)
    return df

def export_summary_stats(path, output_csv):
    df = _load_and_preprocess(path)
    stats = df[['Math','Science','English','Attendance']].describe()
    stats.to_csv(output_csv)
    return output_csv
