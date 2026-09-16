import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Настройка генератора
np.random.seed(42)
start_date = datetime(2023, 1, 1)
days = 1100
date_list = [start_date + timedelta(days=x) for x in range(days)]

# Автоматическая генерация списка ID: [101, 102, 103, 104, 105, 106, 107, 108]
process_ids = list(range(101, 109))

# 1. Расширенный справочник систем и компонентов (8 процессов)
processes_data = {
    'ProcessID': process_ids,
    'ProcessName': [
        'Валидация кредитных рисков', 
        'Генерация ad-hoc отчетов', 
        'Проверка модельных гипотез', 
        'Парсинг документации',
        'Скоринг контрагентов', 
        'Мониторинг транзакций',
        'Анализ рыночных рисков', 
        'Оптимизация портфеля'
    ],
    'OwnerTeam': [
        'Risk Validation', 
        'BI Team', 
        'Data Science', 
        'Compliance',
        'Risk Validation', 
        'Security', 
        'Risk Validation', 
        'Asset Management'
    ],
    'Target_LLM_Accuracy': [95.0, 90.0, 92.0, 88.0, 94.0, 96.0, 91.0, 93.0]
}
df_processes = pd.DataFrame(processes_data)

# 2. Лог метрик (Факты активности с трендами и выходными днями)
metrics_log = []
for date in date_list:
    is_weekend = date.weekday() >= 5
    base_modifier = 0.3 if is_weekend else 1.0
    
    for pid in processes_data['ProcessID']:
        year_trend = (date.year - 2023) * 30
        dau = int((np.random.randint(50, 200) + year_trend) * base_modifier)
        if dau < 5: 
            dau = np.random.randint(5, 15)
        
        mau = int(dau * np.random.uniform(4.0, 6.0)) if not is_weekend else int(dau * 5)
        accuracy = float(np.random.uniform(88.0, 99.9) if pid != 104 else np.random.uniform(82.0, 94.0))
        saved_hours = float(round((dau * np.random.uniform(0.15, 0.35)), 1))
        
        metrics_log.append([
            date.strftime('%Y-%m-%d'), pid, dau, mau, round(accuracy, 2), saved_hours
        ])
df_metrics = pd.DataFrame(metrics_log, columns=['Date', 'ProcessID', 'DAU', 'MAU', 'LLM_Accuracy_Pct', 'Saved_Hours'])

# 3. Большой лог инцидентов (~350 записей для глубокой аналитики)
incidents_log = []
incident_types = [
    'Блокировка доступа к БД', 
    'Таймаут API (LLM)', 
    'Изменение структуры источника', 
    'Ошибка валидации данных'
]
statuses = ['Решено', 'В работе', 'Эскалировано']

for _ in range(350):
    inc_date = start_date + timedelta(days=int(np.random.randint(0, days)))
    pid = int(np.random.choice(processes_data['ProcessID']))
    inc_type = np.random.choice(incident_types)
    status = np.random.choice(statuses, p=[0.85, 0.10, 0.05])
    res_time = int(np.random.randint(1, 48) if status == 'Решено' else 0)
    
    incidents_log.append([
        inc_date.strftime('%Y-%m-%d'), pid, inc_type, status, res_time
    ])
df_incidents = pd.DataFrame(incidents_log, columns=['Date', 'ProcessID', 'IncidentType', 'Status', 'ResolutionTime_Hours'])

# Проверяем и создаем папку data, если её нет
os.makedirs('data', exist_ok=True)

# Сохраняем все файлы в папку data/
df_processes.to_csv('data/dim_processes.csv', index=False, encoding='utf-8-sig')
df_metrics.to_csv('data/fact_ai_metrics.csv', index=False, encoding='utf-8-sig')
df_incidents.to_csv('data/fact_incidents.csv', index=False, encoding='utf-8-sig')

print("Все три больших файла успешно сгенерированы и сохранены в папку data/!")
