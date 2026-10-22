class AttendanceJournal:
    def __init__(self):
        self.students: Dict[str, StudentAttendance] = {}
        self.all_lessons: Set[str] = set()

    def add_student(self, student_id: str, name: str):
        self.students[student_id] = StudentAttendance(student_id=student_id, name=name)

    def mark_attendance(self, student_id: str, lesson_id: str, status: AttendanceStatus):
        if student_id in self.students:
            self.students[student_id].add_record(lesson_id, status)
            self.all_lessons.add(lesson_id)

    def get_rating(self) -> List[tuple]:
        """Возвращает рейтинг посещаемости (от большего к меньшему)."""
        total_lessons = len(self.all_lessons)
        ratings = []
        for student in self.students.values():
            perc = student.calculate_percentage(total_lessons)
            ratings.append((student.name, round(perc, 2)))
        return sorted(ratings, key=lambda x: x[1], reverse=True)

    def filter_at_risk(self, policy: AccessPolicy) -> List[str]:
        """Фильтр студентов группы риска (кому грозит недопуск по политике)."""
        total_lessons = len(self.all_lessons)
        at_risk = []
        for student in self.students.values():
            perc = student.calculate_percentage(total_lessons)
            if not policy.check_access(perc):
                at_risk.append(f"{student.name} ({round(perc, 1)}%)")
        return at_risk

    def compare_policies(self, standard_policy: AccessPolicy, lenient_policy: AccessPolicy) -> dict:
        """Сравнение результатов применения разных политик."""
        total_lessons = len(self.all_lessons)
        passed_standard = 0
        passed_lenient = 0

        for student in self.students.values():
            perc = student.calculate_percentage(total_lessons)
            if standard_policy.check_access(perc):
                passed_standard += 1
            if lenient_policy.check_access(perc):
                passed_lenient += 1

        return {
            "Total Students": len(self.students),
            "Passed under Standard": passed_standard,
            "Passed under Lenient": passed_lenient
        }