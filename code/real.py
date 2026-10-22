from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Set

class AttendanceStatus(Enum):
    PRESENT = "присутствовал"
    LATE = "опоздал"
    EXCUSED = "уважительный пропуск"
    ABSENT = "отсутствовал"

@dataclass
class StudentAttendance:
    student_id: str
    name: str
    # Словарь: дата/номер занятия -> статус
    records: Dict[str, AttendanceStatus] = field(default_dict=dict) if hasattr(field, 'default_dict') else field(default_factory=dict)

    def add_record(self, lesson_id: str, status: AttendanceStatus):
        self.records[lesson_id] = status

    def calculate_percentage(self, total_lessons: int) -> float:
        if total_lessons == 0:
            return 100.0
        
        score = 0.0
        for status in self.records.values():
            if status == AttendanceStatus.PRESENT:
                score += 1.0
            elif status == AttendanceStatus.LATE:
                score += 0.8  # Опоздание учитывается с коэффициентом
            elif status == AttendanceStatus.EXCUSED:
                score += 1.0  # Уважительный пропуск не наказывается жестко
            # ABSENT дает 0 баллов
            
        return (score / total_lessons) * 100.0

# Абстрактная политика допуска
class AccessPolicy(ABC):
    @abstractmethod
    def check_access(self, percentage: float) -> bool:
        pass

# Стандартная политика (порог, например, 75%)
class StandardPolicy(AccessPolicy):
    def __init__(self, threshold: float = 75.0):
        self.threshold = threshold

    def check_access(self, percentage: float) -> bool:
        return percentage >= self.threshold

# Лояльная политика (порог ниже, например, 60%, мягче к пропускам)
class LenientPolicy(AccessPolicy):
    def __init__(self, threshold: float = 60.0):
        self.threshold = threshold

    def check_access(self, percentage: float) -> bool:
        return percentage >= self.threshold