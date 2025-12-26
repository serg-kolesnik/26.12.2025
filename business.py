# save as: student_analysis.py
import csv
import statistics
import math

def load_student_data(file_path):
    """
    Загружает данные студентов из CSV-файла.
    Возвращает список словарей.
    """
    students_data = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            required_fields = ['student_id', 'study_hours', 'sleep_hours', 
                              'attendance_percent', 'exam_score']
            
            if not reader.fieldnames:
                print("Файл пустой или неверный формат.")
                return None
            
            for field in required_fields:
                if field not in reader.fieldnames:
                    print(f"Ошибка: отсутствует поле '{field}'")
                    return None
            
            for row in reader:
                student = {
                    'student_id': int(row['student_id']),
                    'study_hours': float(row['study_hours']),
                    'sleep_hours': float(row['sleep_hours']),
                    'attendance_percent': float(row['attendance_percent']),
                    'exam_score': float(row['exam_score'])
                }
                students_data.append(student)
            
            print(f"Загружено данных: {len(students_data)} студентов")
            return students_data
            
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    return None

def calculate_correlations(students):
    """
    Вычисляет корреляцию между баллами и другими показателями.
    """
    if len(students) < 2:
        return {}
    
    scores = [s['exam_score'] for s in students]
    study_hours = [s['study_hours'] for s in students]
    sleep_hours = [s['sleep_hours'] for s in students]
    attendance = [s['attendance_percent'] for s in students]
    
    def correlation(x, y):
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)

        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) * 
                               sum((yi - mean_y) ** 2 for yi in y))
        
        return numerator / denominator if denominator != 0 else 0
    
    return {
        'study': correlation(scores, study_hours),
        'sleep': correlation(scores, sleep_hours),
        'attendance': correlation(scores, attendance)
    }

def find_top_and_bottom_students(students, n=10):
    """
    Находит топ-N и анти-топ-N студентов.
    """
    top_students = sorted(students, key=lambda x: x['exam_score'], reverse=True)[:n]
    bottom_students = sorted(students, key=lambda x: x['exam_score'])[:n]
    
    return top_students, bottom_students

def analyze_habits_for_top20(students):
    """
    Анализирует привычки для топ-20% студентов.
    """
    if not students:
        return None
    
    top_count = max(1, int(len(students) * 0.2))
    top_students = sorted(students, key=lambda x: x['exam_score'], reverse=True)[:top_count]
    
    # Средние значения для топ-20%
    avg_study = statistics.mean(s['study_hours'] for s in top_students)
    avg_sleep = statistics.mean(s['sleep_hours'] for s in top_students)
    avg_attendance = statistics.mean(s['attendance_percent'] for s in top_students)
    
    # Средние значения для всех
    avg_study_all = statistics.mean(s['study_hours'] for s in students)
    avg_sleep_all = statistics.mean(s['sleep_hours'] for s in students)
    avg_attendance_all = statistics.mean(s['attendance_percent'] for s in students)
    
    # Рекомендации
    recommendations = {
        'study_hours': avg_study - avg_study_all,
        'sleep_hours': avg_sleep - avg_sleep_all,
        'attendance': avg_attendance - avg_attendance_all
    }
    
    return {
        'top_avg': {'study': avg_study, 'sleep': avg_sleep, 'attendance': avg_attendance},
        'all_avg': {'study': avg_study_all, 'sleep': avg_sleep_all, 'attendance': avg_attendance_all},
        'recommendations': recommendations
    }

def display_results(students, correlations, top_students, bottom_students, habits_analysis):
    """
    Выводит результаты анализа.
    """
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА ДАННЫХ СТУДЕНТОВ")
    print("="*60)
    
    # 1. Основная статистика
    print("\n1. ОСНОВНАЯ СТАТИСТИКА:")
    scores = [s['exam_score'] for s in students]
    print(f"   Всего студентов: {len(students)}")
    print(f"   Средний балл: {statistics.mean(scores):.2f}")
    print(f"   Медианный балл: {statistics.median(scores):.2f}")
    print(f"   Стандартное отклонение: {statistics.stdev(scores):.2f}")
    
    # 2. Корреляции
    print("\n2. КОРРЕЛЯЦИИ С ЭКЗАМЕНАЦИОННЫМ БАЛЛОМ:")
    print(f"   • Часы учёбы: {correlations['study']:+.3f}")
    print(f"   • Часы сна: {correlations['sleep']:+.3f}")
    print(f"   • Посещаемость: {correlations['attendance']:+.3f}")
    
    # Описание корреляций
    print("\n   Интерпретация корреляций:")
    for name, value in [("Учёба", correlations['study']), 
                       ("Сон", correlations['sleep']), 
                       ("Посещаемость", correlations['attendance'])]:
        abs_val = abs(value)
        if abs_val >= 0.7:
            strength = "очень сильная"
        elif abs_val >= 0.5:
            strength = "сильная"
        elif abs_val >= 0.3:
            strength = "умеренная"
        elif abs_val >= 0.1:
            strength = "слабая"
        else:
            strength = "очень слабая или отсутствует"
        
        direction = "положительная" if value > 0 else "отрицательная" if value < 0 else "нет связи"
        print(f"     {name}: {strength} {direction} связь")
    
    # 3. Топ-10 студентов
    print("\n3. 10 САМЫХ УСПЕШНЫХ СТУДЕНТОВ:")
    print("   ID  Учёба  Сон   Посещ.  Балл")
    print("   " + "-"*30)
    for student in top_students:
        print(f"   {student['student_id']:<4} "
              f"{student['study_hours']:<6.1f} "
              f"{student['sleep_hours']:<5.1f} "
              f"{student['attendance_percent']:<6.1f} "
              f"{student['exam_score']:<5.1f}")
    
    # 4. Анти-топ-10 студентов
    print("\n4. 10 НАИМЕНЕЕ УСПЕШНЫХ СТУДЕНТОВ:")
    print("   ID  Учёба  Сон   Посещ.  Балл")
    print("   " + "-"*30)
    for student in bottom_students:
        print(f"   {student['student_id']:<4} "
              f"{student['study_hours']:<6.1f} "
              f"{student['sleep_hours']:<5.1f} "
              f"{student['attendance_percent']:<6.1f} "
              f"{student['exam_score']:<5.1f}")
    
    # 5. Анализ привычек топ-20%
    print("\n5. АНАЛИЗ ПРИВЫЧЕК ТОП-20% СТУДЕНТОВ:")
    if habits_analysis:
        print("   Средние показатели топ-20% студентов:")
        print(f"     • Учёба: {habits_analysis['top_avg']['study']:.1f} ч/неделю")
        print(f"     • Сон: {habits_analysis['top_avg']['sleep']:.1f} ч/неделю")
        print(f"     • Посещаемость: {habits_analysis['top_avg']['attendance']:.1f}%")
        
        print("\n   Сравнение со средними по всем студентам:")
        print(f"     • Учёба: {habits_analysis['all_avg']['study']:.1f} ч/неделю")
        print(f"     • Сон: {habits_analysis['all_avg']['sleep']:.1f} ч/неделю")
        print(f"     • Посещаемость: {habits_analysis['all_avg']['attendance']:.1f}%")
        
        # Рекомендации
        print("\n6. РЕКОМЕНДАЦИИ ДЛЯ ПОПАДАНИЯ В ТОП-20%:")
        rec = habits_analysis['recommendations']
        
        if abs(rec['study_hours']) > 1:
            if rec['study_hours'] > 0:
                print(f"   • Увеличить учёбу на {rec['study_hours']:.1f} часов в неделю")
            else:
                print(f"   • Уменьшить учёбу на {-rec['study_hours']:.1f} часов в неделю")
        
        if abs(rec['sleep_hours']) > 1:
            if rec['sleep_hours'] > 0:
                print(f"   • Увеличить сон на {rec['sleep_hours']:.1f} часов в неделю")
            else:
                print(f"   • Уменьшить сон на {-rec['sleep_hours']:.1f} часов в неделю")
        
        if abs(rec['attendance']) > 2:
            if rec['attendance'] > 0:
                print(f"   • Повысить посещаемость на {rec['attendance']:.1f}%")
            else:
                print(f"   • Посещаемость уже выше среднего на {-rec['attendance']:.1f}%")
    
    print("\n" + "="*60)

def main():
    """
    Основная функция программы.
    """
    print("АНАЛИЗ ДАННЫХ СТУДЕНТОВ")
    print("="*40)
    
    # Загрузка данных из фиксированного файла
    file_path = "students_1000.csv"
    print(f"Загрузка данных из файла: {file_path}")
    
    students = load_student_data(file_path)
    
    if not students:
        print("Не удалось загрузить данные. Программа завершена.")
        return
    
    # Анализ данных
    print("\nАнализ данных...")
    
    # 1. Рассчитать корреляции
    correlations = calculate_correlations(students)
    
    # 2. Найти топ-10 и анти-топ-10 студентов
    top_students, bottom_students = find_top_and_bottom_students(students, 10)
    
    # 3. Анализ привычек для топ-20%
    habits_analysis = analyze_habits_for_top20(students)
    
    # 4. Вывести результаты
    display_results(students, correlations, top_students, bottom_students, habits_analysis)
    
if __name__ == "__main__":
    main()