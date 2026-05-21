# 🎓 University Student Analytics Dashboard

**Data Mining · Activity I — Data Visualization and Dashboard Deployment**  
Universidad de la Costa · Department of Computer Science and Electronics  
Prof. José Escorcia-Gutierrez, Ph.D.

---

## 👥 Team Members

- Antwan Davis Ramos Amador
- Jhonny Cala Ardila

---

## 📌 Purpose

This dashboard provides an interactive analytical view of student admission, enrollment, retention, and satisfaction data from a university across academic years 2015–2024.

It was built as part of Activity I for the Data Mining course, covering:
- Exploratory data analysis in Python
- Interactive visualizations with Plotly and Streamlit
- Dashboard deployment via Streamlit Cloud

---

## 📊 Features

- **KPI Cards** — average applications, enrollment, retention rate, satisfaction, and admission rate
- **Line Charts** — retention and satisfaction trends over time
- **Bar Charts** — applications vs. enrolled by year, Spring vs. Fall comparison
- **Donut Chart** — department enrollment share
- **Scatter Plot** — correlation between satisfaction and retention
- **Interactive Filters** — filter by year, term, and department

---

## 📁 Repository Structure

```
├── app.py                  # Main Streamlit dashboard
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── university_student_data.csv   # Dataset (optional, embedded in app.py)
```

---

## 🔍 Key Findings

1. **Retention** improved steadily from 85% (2015) to 90% (2024).
2. **Student satisfaction** rose from 78% to 88% over the same period.
3. **Engineering** is the fastest-growing department; **Science** shows a declining trend post-2019.
4. **Spring and Fall** terms show identical enrollment figures, suggesting stable semester-to-semester planning.
5. A strong **positive correlation** exists between retention rate and student satisfaction.
