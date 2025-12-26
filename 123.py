# save as: generate_students_extreme.py
import csv
import random
import math

def generate_student_data(num_students=1000):
    """Генерирует данные для студентов с большим разбросом."""
    
    students = []
    random.seed(42)  # Для воспроизводимости
    
    print(f"Генерация данных для {num_students} студентов...")
    
    for student_id in range(1, num_students + 1):
        # СЛУЧАЙ 1: Экстремальные значения (10% студентов)
        if random.random() < 0.1:
            study_hours = random.choice([random.uniform(5, 15),  # Очень мало
                                        random.uniform(70, 90)]) # Очень много
            sleep_hours = random.choice([random.uniform(25, 35),  # Очень мало
                                        random.uniform(65, 80)]) # Очень много
            attendance = random.choice([random.uniform(30, 50),   # Очень низкая
                                       random.uniform(95, 100)])  # Идеальная
        else:
            # СЛУЧАЙ 2: Нормальный разброс, но с большей дисперсией
            study_hours = random.normalvariate(35, 15)  # Увеличенная дисперсия
            sleep_hours = random.normalvariate(48, 12)  # Больший разброс
            attendance = random.normalvariate(75, 20)   # От 35% до 115% теоретически
        
        # Ограничения (но с очень широкими границами)
        study_hours = max(2, min(100, study_hours))      # От 2 до 100 часов
        sleep_hours = max(20, min(85, sleep_hours))      # От 20 до 85 часов
        attendance = max(15, min(100, attendance))       # От 15% до 100%
        
        # СЛУЧАЙ 1: Парадоксальные зависимости (20% студентов)
        if random.random() < 0.2:
            # Инвертируем логику для некоторых студентов
            if study_hours > 60:
                study_multiplier = random.uniform(0.1, 0.5)  # Переутомление -> низкая эффективность
            else:
                study_multiplier = random.uniform(0.8, 1.5)
            
            if sleep_hours > 60:
                sleep_multiplier = random.uniform(-0.5, 0.3)  # Пересып -> негативный эффект
            else:
                sleep_multiplier = random.uniform(0.5, 1.2)
        else:
            # СЛУЧАЙ 2: Нормальные, но слабые зависимости
            study_multiplier = random.uniform(0.3, 1.0)
            sleep_multiplier = random.uniform(0.4, 1.1)
        
        # ОЧЕНЬ СИЛЬНЫЙ случайный фактор
        random_factor = random.uniform(-25, 25)  # От -25 до +25 баллов!
        
        # НЕПРЕДСКАЗУЕМЫЕ дополнительные факторы
        hidden_factors = random.uniform(-20, 20)  # Скрытые переменные
        
        # Формула с МАЛЕНЬКИМИ и НЕОДНОЗНАЧНЫМИ зависимостями
        base_score = random.uniform(30, 70)  # Базовый уровень тоже случайный!
        
        # СЛАБАЯ зависимость от учебы (может быть даже отрицательной)
        study_effect = study_hours * study_multiplier * random.uniform(0.1, 0.3)
        
        # СЛАБАЯ и НЕЛИНЕЙНАЯ зависимость от сна
        if sleep_hours < 30:
            sleep_effect = sleep_hours * sleep_multiplier * 0.2
        elif sleep_hours < 50:
            sleep_effect = 6 + (sleep_hours - 30) * sleep_multiplier * 0.15
        elif sleep_hours < 70:
            sleep_effect = 9 + (sleep_hours - 50) * sleep_multiplier * 0.1
        else:
            sleep_effect = 11 - (sleep_hours - 70) * 0.2  # После 70 часов сон вредит
        
        # ПОСЕЩАЕМОСТЬ: иногда важна, иногда нет
        if attendance < 40:
            attendance_effect = attendance * 0.1
        elif attendance < 80:
            attendance_effect = 4 + (attendance - 40) * 0.15
        else:
            attendance_effect = 10 + (attendance - 80) * 0.05  # Убывающая отдача
        
        # ВЗАИМОДЕЙСТВИЯ между факторами (могут быть как положительными, так и отрицательными)
        interaction = 0
        if study_hours > 50 and sleep_hours < 40:
            interaction -= random.uniform(5, 15)  # Переутомление
        if attendance > 90 and study_hours < 20:
            interaction -= random.uniform(3, 10)  # Ходит, но не учится
        
        # ИТОГОВЫЙ БАЛЛ с ОГРОМНЫМ влиянием случайности
        exam_score = (
            base_score +
            study_effect +
            sleep_effect +
            attendance_effect +
            random_factor +
            hidden_factors +
            interaction
        )
        
        # АНОМАЛИИ: 15% студентов с совершенно необъяснимыми результатами
        if random.random() < 0.15:
            anomaly_type = random.choice(['super_high', 'super_low', 'inverse', 'random'])
            
            if anomaly_type == 'super_high':
                exam_score = random.uniform(85, 100)  # Всегда отлично
            elif anomaly_type == 'super_low':
                exam_score = random.uniform(25, 40)   # Всегда плохо
            elif anomaly_type == 'inverse':
                # Инвертируем: много учится -> плохо, мало -> хорошо
                exam_score = 100 - (study_hours * 0.8)
            else:  # random
                exam_score = random.uniform(25, 100)  # Совершенно случайно
        
        # Ограничиваем, но оставляем экстремальные значения
        exam_score = max(10, min(105, exam_score))  # Может быть и 105!
        
        students.append({
            'student_id': student_id,
            'study_hours': round(study_hours, 1),
            'sleep_hours': round(sleep_hours, 1),
            'attendance_percent': round(attendance, 1),
            'exam_score': round(exam_score, 1)
        })
        
        # Прогресс
        if student_id % 200 == 0:
            print(f"  Создано {student_id} студентов...")
    
    return students

def save_to_csv(students, filename='students_1000.csv'):
    """Сохраняет данные в CSV файл."""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['student_id', 'study_hours', 'sleep_hours', 
                     'attendance_percent', 'exam_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for student in students:
            writer.writerow(student)
    
    return filename

def show_extreme_cases(students):
    """Показывает экстремальные случаи из данных."""
    
    print("\n🔥 ЭКСТРЕМАЛЬНЫЕ СЛУЧАИ:")
    print("=" * 70)
    
    # Самые необычные комбинации
    print("\n1. ПАРАДОКСЫ (много учится, но плохой балл):")
    paradox_students = sorted(
        [s for s in students if s['study_hours'] > 60 and s['exam_score'] < 50],
        key=lambda x: x['study_hours'],
        reverse=True
    )[:3]
    
    for s in paradox_students:
        print(f"   ID {s['student_id']}: Учёба {s['study_hours']}ч → Балл {s['exam_score']}")
    
    print("\n2. ФЕНОМЕНЫ (мало учится, но отличный балл):")
    fenomen_students = sorted(
        [s for s in students if s['study_hours'] < 20 and s['exam_score'] > 85],
        key=lambda x: x['exam_score'],
        reverse=True
    )[:3]
    
    for s in fenomen_students:
        print(f"   ID {s['student_id']}: Учёба {s['study_hours']}ч → Балл {s['exam_score']}")
    
    print("\n3. ЭКСТРЕМАЛЬНЫЕ ЗНАЧЕНИЯ:")
    
    # Минимумы и максимумы
    min_study = min(students, key=lambda x: x['study_hours'])
    max_study = max(students, key=lambda x: x['study_hours'])
    
    min_sleep = min(students, key=lambda x: x['sleep_hours'])
    max_sleep = max(students, key=lambda x: x['sleep_hours'])
    
    min_attend = min(students, key=lambda x: x['attendance_percent'])
    max_attend = max(students, key=lambda x: x['attendance_percent'])
    
    min_score = min(students, key=lambda x: x['exam_score'])
    max_score = max(students, key=lambda x: x['exam_score'])
    
    print(f"   Учёба: {min_study['study_hours']}ч (min) ←→ {max_study['study_hours']}ч (max)")
    print(f"   Сон: {min_sleep['sleep_hours']}ч (min) ←→ {max_sleep['sleep_hours']}ч (max)")
    print(f"   Посещаемость: {min_attend['attendance_percent']}% (min) ←→ {max_attend['attendance_percent']}% (max)")
    print(f"   Баллы: {min_score['exam_score']} (min) ←→ {max_score['exam_score']} (max)")

def main():
    """Основная функция."""
    
    # Генерация данных
    num_students = 1000
    students = generate_student_data(num_students)
    
    # Сохранение
    filename = save_to_csv(students)
    
    # Статистика
    print(f"\n✅ Данные сохранены в: {filename}")
    print(f"📊 Всего студентов: {len(students)}")
    
    # Примеры данных
    print("\n📋 ПЕРВЫЕ 10 СТУДЕНТОВ (для примера):")
    print("ID  Учёба    Сон     Посещ.   Балл")
    print("-" * 35)
    for student in students[:10]:
        print(f"{student['student_id']:<4} "
              f"{student['study_hours']:<8.1f} "
              f"{student['sleep_hours']:<7.1f} "
              f"{student['attendance_percent']:<8.1f} "
              f"{student['exam_score']:<6.1f}")
    
    # Экстремальные случаи
    show_extreme_cases(students)
if __name__ == "__main__":
    main()