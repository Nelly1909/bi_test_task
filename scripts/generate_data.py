import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Настройка генератора
np.random.seed(42)
start_date = datetime(2026, 6, 1)
days = 90
date_list = [start_date + timedelta(days=x) for x in range(days)]

# Автоматически создаем список ID, чтобы код не ломался при копировании
process_ids = [101, 102, 103, 104]

# 1. Таблица процессов (Директория / Справочник)
processes_data = {
    'ProcessID': process_ids,
    'ProcessName': [
        'Валидация кредитных рисков', 
        'Генерация ad-hoc отчетов', 
        'Проверка модельных гипотез', 
        'Парсинг документации'
    ],
    'OwnerTeam': [
        'Risk Validation', 
        'BI Team', 
        'Data Science', 
        'Compliance'
    ],
    'Target_LLM_Accuracy': [95.0, 90.0, 92.0, 88.0]
}
df_processes = pd.DataFrame(processes_data)

# 2. Таблица метрик ИИ-агентов (Факты)
metrics_log = []
for date in date_list:
    for pid in processes_data['ProcessID']:
        dau = int(np.random.randint(40, 180) if pid != 103 else np.random.randint(10, 50))
        mau = int(dau * np.random.uniform(3.5, 4.5))
        accuracy = float(np.random.uniform(85.0, 99.5))
        saved_hours = float(round((dau * np.random.uniform(0.1, 0.3)), 1))
        
        metrics_log.append([
            date.strftime('%Y-%m-%d'), pid, dau, mau, round(accuracy, 2), saved_hours
        ])

df_metrics = pd.DataFrame(metrics_log, columns=['Date', 'ProcessID', 'DAU', 'MAU', 'LLM_Accuracy_Pct', 'Saved_Hours'])

# 3. Таблица проектных зависимостей и инцидентов (Факты логов)
incidents_log = []
incident_types = [
    'Блокировка доступа к БД', 
    'Таймаут API (LLM)', 
    'Изменение структуры источника', 
    'Ошибка валидации данных'
]
statuses = ['Решено', 'В работе', 'Эскалировано']

# Генерация случайных инцидентов
for _ in range(40):
    inc_date = start_date + timedelta(days=int(np.random.randint(0, days)))
    pid = int(np.random.choice(processes_data['ProcessID']))
    inc_type = np.random.choice(incident_types)
    status = np.random.choice(statuses, p=[0.7, 0.2, 0.1])
    resolution_time = int(np.random.randint(1, 24) if status == 'Решено' else 0)
    
    incidents_log.append([
        inc_date.strftime('%Y-%m-%d'), pid, inc_type, status, resolution_time
    ])

df_incidents = pd.DataFrame(incidents_log, columns=['Date', 'ProcessID', 'IncidentType', 'Status', 'ResolutionTime_Hours'])

# Проверяем и создаем папку data
os.makedirs('data', exist_ok=True)

# Сохраняем в папку data/
df_processes.to_csv('data/dim_processes.csv', index=False, encoding='utf-8-sig')
df_metrics.to_csv('data/fact_ai_metrics.csv', index=False, encoding='utf-8-sig')
df_incidents.to_csv('data/fact_incidents.csv', index=False, encoding='utf-8-sig')

print("Все три файла успешно сгенерированы и сохранены в папку data/!")
