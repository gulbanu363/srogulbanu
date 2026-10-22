# Инициализация журнала
journal = AttendanceJournal()

# Добавление студентов
journal.add_student("S01", "Алексей Иванов")
journal.add_student("S02", "Мария Петрова")
journal.add_student("S03", "Иван Смирнов")

# Регистрация отметок за занятия
lessons = ["Лекция 1", "Лекция 2", "Лекция 3", "Лекция 4"]

# Алексей ходит отлично
for l in lessons:
    journal.mark_attendance("S01", l, AttendanceStatus.PRESENT)

# Мария часто опаздывает или пропускает по уважительной причине
journal.mark_attendance("S02", "Лекция 1", AttendanceStatus.PRESENT)
journal.mark_attendance("S02", "Лекция 2", AttendanceStatus.LATE)
journal.mark_attendance("S02", "Лекция 3", AttendanceStatus.EXCUSED)
journal.mark_attendance("S02", "Лекция 4", AttendanceStatus.ABSENT)

# Иван часто прогуливает
for l in lessons:
    journal.mark_attendance("S03", l, AttendanceStatus.ABSENT)

# Политики
standard = StandardPolicy(threshold=75.0)
lenient = LenientPolicy(threshold=60.0)

print("--- РЕЙЙТИНГ ПОСЕЩАЕМОСТИ ---")
for name, score in journal.get_rating():
    print(f"{name}: {score}%")

print("\n--- СПИСОК ПРЕДУПРЕЖДЕНИЙ (Стандартная политика) ---")
print(journal.filter_at_risk(standard))

print("\n--- СРАВНЕНИЕ ПОЛИТИК ДОПУСКА ---")
print(journal.compare_policies(standard, lenient))