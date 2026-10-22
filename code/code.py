from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class StudentAttendance:
    student_id: str
    name: str
    records: Dict[str, str] = field(default_factory=dict)  # lesson_id -> status


class AccessPolicy(ABC):
    @abstractmethod
    def is_allowed(self, percentage: float) -> bool:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass


class StandardPolicy(AccessPolicy):
    def __init__(self, threshold: float = 75.0):
        self.threshold = threshold  # Порог допуска по умолчанию 75%
        
    def is_allowed(self, percentage: float) -> bool:
        return percentage >= self.threshold
        
    def get_name(self) -> str:
        return f"StandardPolicy (Порог: {self.threshold}%)"


class LenientPolicy(AccessPolicy):
    def __init__(self, threshold: float = 60.0):
        self.threshold = threshold  # Лояльный порог 60%
        
    def is_allowed(self, percentage: float) -> bool:
        return percentage >= self.threshold
        
    def get_name(self) -> str:
        return f"LenientPolicy (Порог: {self.threshold}%)"


class AttendanceJournal:
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.students: Dict[str, StudentAttendance] = {}
        
    def add_student(self, student_id: str, name: str):
        self.students[student_id] = StudentAttendance(student_id, name)
        
    def mark_attendance(self, student_id: str, lesson_id: str, status: str):
        """Регистрация отметок: PRESENT, TARDY, EXCUSED, ABSENT"""
        if student_id in self.students:
            self.students[student_id].records[lesson_id] = status
            
    def calculate_percentage(self, student_id: str) -> float:
        """Расчёт процента присутствия (уважительные не ухудшают базу, опоздания идут с коэффициентом)"""
        student = self.students.get(student_id)
        if not student or not student.records:
            return 0.0
        
        total = len(student.records)
        score = 0.0
        for status in student.records.values():
            if status == 'PRESENT':
                score += 1.0
            elif status == 'TARDY':
                score += 0.8  # Частичный зачёт при опоздании
            elif status == 'EXCUSED':
                score += 1.0  # Уважительный пропуск не снижает балл
            elif status == 'ABSENT':
                score += 0.0
                
        return (score / total) * 100.0

    def get_attendance_rating(self) -> List[tuple]:
        """Рейтинг посещаемости группы по убыванию"""
        rating = []
        for s_id, student in self.students.items():
            pct = self.calculate_percentage(s_id)
            rating.append((student.name, pct))
        return sorted(rating, key=lambda x: x[1], reverse=True)

    def find_at_risk_students(self, policy: AccessPolicy) -> List[dict]:
        """Поиск студентов риска на основе заданной политики"""
        at_risk = []
        for s_id, student in self.students.items():
            pct = self.calculate_percentage(s_id)
            if not policy.is_allowed(pct):
                at_risk.append({
                    "student_id": s_id,
                    "name": student.name,
                    "percentage": pct,
                    "warning": f"⚠️ Студент {student.name} в зоне риска: посещаемость {pct:.1f}% ниже требуемого."
                })
        return at_risk

    def compare_policies(self, policies: List[AccessPolicy]) -> dict:
        """Сравнение результатов применения разных политик допуска"""
        comparison = {}
        for policy in policies:
            risk_list = self.find_at_risk_students(policy)
            comparison[policy.get_name()] = {
                "at_risk_count": len(risk_list),
                "students": [s["name"] for s in risk_list]
            }
        return comparison