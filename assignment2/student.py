from student_analysis import get_toppers, enrich_student_data, export_summary_stats

# 1) Find eligible toppers
toppers = get_toppers('student_scores.csv')
print(toppers)

# 2) Get enriched DataFrame
df_enriched = enrich_student_data('student_scores.csv')
print(df_enriched.head())

# 3) Export summary stats
export_summary_stats('student_scores.csv', 'summary_stats.csv')
