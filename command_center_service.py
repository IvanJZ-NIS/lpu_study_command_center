"""
LYCEUM OF THE PHILIPPINES UNIVERSITY - CAVITE
CSCN02C - Object-Oriented Programming
Midterm Laboratory Activity 2: Service Layer & Design Patterns
Project: Philosophically Themed Student Academic Command Center & Planner
Domain: Grade Calculator & Academic Standing Service
"""
import mysql.connector
from abc import ABC, abstractmethod
from typing import List, Dict

# ============================================================================
# 1. ENCAPSULATION & DATA PROTECTION (Domain Model)
# ============================================================================

class Assessment:
    """
    Represents an academic assessment (quiz, exam, project).
    Encapsulates raw score and weight attributes to prevent invalid state changes.
    """
    def __init__(self, name: str, score: float, max_score: float, weight: float = 1.0):
        self.name = name
        self._max_score = max_score  # Triggers property setters for defensive validation
        self.score = score
        self.weight = weight

    @property
    def score(self) -> float:
        """Getter for the protected score attribute."""
        return self._score

    @score.setter
    def score(self, value: float):
        """
        Validates that score is a non-negative number and does not exceed max_score.
        Rejects invalid state changes with a descriptive ValueError.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Score for '{self.name}' must be a numeric value.")
        if value < 0 or value > self._max_score:
            raise ValueError(
                f"Validation Error: Score {value} is invalid. "
                f"Must be between 0 and {self._max_score}."
            )
        self._score = float(value)

    @property
    def weight(self) -> float:
        """Getter for the assessment weight percentage."""
        return self._weight

    @weight.setter
    def weight(self, value: float):
        """Validates that assessment weight is strictly greater than 0."""
        if value <= 0:
            raise ValueError(f"Validation Error: Weight {value} must be greater than 0.")
        self._weight = float(value)

    @property
    def percentage(self) -> float:
        """Read-only property calculating the percentage score."""
        return (self._score / self._max_score) * 100.0

    def __str__(self) -> str:
        return f"{self.name}: {self._score}/{self._max_score} ({self.percentage:.1f}%) [Weight: {self._weight}]"


# ============================================================================
# 2. ABSTRACTION & INTERFACE CONTRACT (Abstract Base Class)
# ============================================================================

class GradeCalculator(ABC):
    """
    Abstract Base Class defining the behavioral contract for all grade calculators.
    Concrete subclasses must implement the calculate_standing method.
    """
    @abstractmethod
    def calculate_standing(self, assessments: List[Assessment]) -> Dict[str, float]:
        """Calculates final numerical average and grade point equivalence."""
        pass


class WeightedGradeCalculator(GradeCalculator):
    """
    Concrete Implementation A: Calculates final grade using weighted category percentages (e.g., Syllabus weights).
    """
    def calculate_standing(self, assessments: List[Assessment]) -> Dict[str, float]:
        if not assessments:
            return {"final_percentage": 0.0, "gpa": 5.0}
        
        total_weight = sum(a.weight for a in assessments)
        weighted_sum = sum(a.percentage * a.weight for a in assessments)
        final_percentage = weighted_sum / total_weight
        
        return {
            "final_percentage": round(final_percentage, 2),
            "gpa": self._convert_to_lpu_grading_scale(final_percentage)
        }

    def _convert_to_lpu_grading_scale(self, percentage: float) -> float:
        """Converts percentage to standard Philippine collegiate grading scale."""
        if percentage >= 97.0: return 1.00
        elif percentage >= 93.0: return 1.25
        elif percentage >= 89.0: return 1.50
        elif percentage >= 85.0: return 1.75
        elif percentage >= 80.0: return 2.00
        elif percentage >= 75.0: return 2.25
        elif percentage >= 70.0: return 2.50
        elif percentage >= 65.0: return 2.75
        elif percentage >= 60.0: return 3.00
        else: return 5.00  # Failed class


class SimpleAverageGradeCalculator(GradeCalculator):
    """
    Concrete Implementation B: Calculates final standing using simple arithmetic mean across raw percentages.
    """
    def calculate_standing(self, assessments: List[Assessment]) -> Dict[str, float]:
        if not assessments:
            return {"final_percentage": 0.0, "gpa": 5.0}
        
        avg_percentage = sum(a.percentage for a in assessments) / len(assessments)
        
        # Standard collegiate scale
        if avg_percentage >= 75.0:
            gpa = round(3.0 - ((avg_percentage - 75.0) / 25.0) * 2.0, 2)
        else:
            gpa = 5.00
            
        return {
            "final_percentage": round(avg_percentage, 2),
            "gpa": max(1.0, gpa)
        }


# ============================================================================
# 3. CREATIONAL DESIGN PATTERN (Factory Method Pattern)
# ============================================================================

class GradeCalculatorFactory:
    """
    Factory Method Pattern: Decouples client service code from concrete calculator instantiation.
    Selects and instantiates the proper calculator based on runtime configuration.
    """
    @staticmethod
    def create_calculator(strategy_type: str) -> GradeCalculator:
        strategy_type_clean = strategy_type.strip().lower()
        if strategy_type_clean in ["weighted", "syllabus"]:
            return WeightedGradeCalculator()
        elif strategy_type_clean in ["simple", "average", "raw"]:
            return SimpleAverageGradeCalculator()
        else:
            raise ValueError(f"Factory Error: Unknown grading strategy '{strategy_type}'.")


# ============================================================================
# 4. BEHAVIORAL DESIGN PATTERN (Strategy Pattern) & SERVICE LAYER
# ============================================================================

class AcademicStandingService:
    """
    Service Layer Context Class: Coordinates assessments and uses a GradeCalculator Strategy at runtime.
    Hides internal calculation mechanics behind high-level business operations.
    """
    def __init__(self, student_name: str, course_code: str, strategy: GradeCalculator):
        self.student_name = student_name
        self.course_code = course_code
        self._strategy = strategy  # Strategy reference
        self._assessments: List[Assessment] = []

    def set_strategy(self, strategy: GradeCalculator):
        """Allows swapping the grading calculation strategy at runtime."""
        self._strategy = strategy

    def add_assessment(self, assessment: Assessment):
        """Adds a validated assessment entity to the student's records."""
        self._assessments.append(assessment)

    def generate_academic_report(self) -> Dict:
        """Executes the calculation strategy and formats output for dashboard view."""
        results = self._strategy.calculate_standing(self._assessments)
        return {
            "student": self.student_name,
            "course": self.course_code,
            "strategy_used": self._strategy.__class__.__name__,
            "assessment_count": len(self._assessments),
            "final_percentage": results["final_percentage"],
            "calculated_gpa": results["gpa"],
            "status": "PASSED" if results["final_percentage"] >= 75.0 else "RE-EVALUATE"
        }


# ============================================================================
# 5. WORKFLOW DEMONSTRATION & REJECTED OPERATION (Main Execution)
# ============================================================================

def main():
    print("=" * 70)
    print("🎓 LPU-CAVITE STUDENT ACADEMIC COMMAND CENTER - SERVICE LAYER DEMO")
    print("=" * 70)

    # Step A: Instantiate Service Layer via Factory Pattern
    print("\n[STEP 1] Initializing Course Service via Factory Pattern...")
    calculator_strategy = GradeCalculatorFactory.create_calculator("weighted")
    service = AcademicStandingService(
        student_name="Ivan Joseph Zara",
        course_code="CSCN02C (Object-Oriented Programming)",
        strategy=calculator_strategy
    )
    print(f"✓ Initialized service with strategy: {calculator_strategy.__class__.__name__}")

    # Step B: Add Valid Domain Entities with Encapsulated Data
    print("\n[STEP 2] Adding Valid Assessment Records to Domain Layer...")
    valid_tasks = [
        Assessment("Prelim Exam", score=92, max_score=100, weight=0.30),
        Assessment("OOP Domain Model (Act 1)", score=96, max_score=100, weight=0.20),
        Assessment("Midterm Hands-on Exam", score=88, max_score=100, weight=0.30),
        Assessment("Quiz Hub Reviewer Deck", score=100, max_score=100, weight=0.20),
    ]

    for task in valid_tasks:
        service.add_assessment(task)
        print(f"  + Added: {task}")

    # Step C: Compute and Display Standing via Strategy Pattern
    print("\n[STEP 3] Processing Academic Standing Report (Weighted Strategy)...")
    report = service.generate_academic_report()
    print(f"  Student Name     : {report['student']}")
    print(f"  Subject          : {report['course']}")
    print(f"  Calculation Mode : {report['strategy_used']}")
    print(f"  Final Percentage : {report['final_percentage']}%")
    print(f"  Grade Rating     : {report['calculated_gpa']:.2f}")
    print(f"  Academic Status  : {report['status']}")

    # Step D: Demonstrate Runtime Strategy Switching
    print("\n[STEP 4] Switching Calculation Strategy to 'Simple Average' at Runtime...")
    simple_strategy = GradeCalculatorFactory.create_calculator("simple")
    service.set_strategy(simple_strategy)
    new_report = service.generate_academic_report()
    print(f"  New Strategy     : {new_report['strategy_used']}")
    print(f"  Final Percentage : {new_report['final_percentage']}% (GPA: {new_report['calculated_gpa']:.2f})")

    # Step E: Demonstrate Rejected Invalid Operation (Encapsulation Guard)
    print("\n" + "=" * 70)
    print("🛡️ [STEP 5] TESTING DEFENSIVE ENCAPSULATION & INVALID STATE REJECTION")
    print("=" * 70)

    # Test 1: Rejecting Out-of-Bounds Score
    try:
        print("\nAttempting to record invalid exam score: 105 / 100 (Exceeds maximum score)...")
        Assessment("Final Defense", score=105, max_score=100, weight=0.40)
    except ValueError as error:
        print(f"❌ Operation Rejected by System: {error}")

    # Test 2: Rejecting Negative Score State Mutation
    try:
        print("\nAttempting to mutate existing assessment score to a negative value (-15)...")
        valid_tasks[0].score = -15  # FIXED: Accessing an individual Assessment item in the list
    except ValueError as error:
        print(f"❌ State Mutation Rejected by System: {error}")

    # Test 3: Rejecting Invalid Factory Strategy Type
    try:
        print("\nAttempting to request invalid strategy type from Factory ('hyperbolic')...")
        GradeCalculatorFactory.create_calculator("hyperbolic")
    except ValueError as error:
        print(f"❌ Factory Instantiation Rejected: {error}")

    print("\n" + "=" * 70)
    print("✅ Complete workflow finished with all validation guards functioning.")
    print("=" * 70)


if __name__ == "__main__":
    main()