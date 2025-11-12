import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")["Name"].values
n_students = len(students)
days = 30

prob_present = np.concatenate([np.full(n_students//2, 0.8), np.full(n_students - n_students//2, 0.4)])
att = np.array([np.random.choice(['P','A'], p=[p, 1-p], size=days) for p in prob_present])

dates = pd.date_range(start='2025-09-01', periods=days).strftime('%d-%m-%Y')

df = pd.DataFrame(att, index=students, columns=dates)

total_present = (att=='P').sum(axis=1)
total_absent  = (att=='A').sum(axis=1)
percent = total_present / days * 100
status = np.where(percent >= 75, 'Qualified', 'Disqualified')

df['Total_Present'] = total_present
df['Total_Absent'] = total_absent
df['Percent_Attendance'] = percent
df['Status'] = status

daily_info = pd.DataFrame({
    'Presentees': [', '.join(df.index[att[:,i]=='P']) for i in range(days)],
    'Absentees': [', '.join(df.index[att[:,i]=='A']) for i in range(days)],
    'Total_Presentees': (att=='P').sum(axis=0),
    'Total_Absentees': (att=='A').sum(axis=0)
}, index=dates)

print("\n--- All Students Attendance ---\n", df)
print("\n--- Daily Presentees & Absentees with Counts ---\n", daily_info)

df.to_csv("students_attendance.csv")
daily_info.to_csv("daily_attendance_summary.csv")
