from flask import Flask, render_template, request, jsonify
from command_center_service import (
    Assessment,
    GradeCalculatorFactory,
    AcademicStandingService
)

app = Flask(__name__)

# Initialize global service instance
calculator_strategy = GradeCalculatorFactory.create_calculator("weighted")
service = AcademicStandingService(
    student_name="Ivan Joseph Zara",
    course_code="CSCN02C - Object-Oriented Programming",
    strategy=calculator_strategy
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/add-assessment", methods=["POST"])
def add_assessment():
    try:
        data = request.json
        name = data.get("name")
        score = float(data.get("score"))
        max_score = float(data.get("max_score"))
        weight = float(data.get("weight"))

        # Triggers encapsulation & property validation in command_center_service.py
        assessment = Assessment(name=name, score=score, max_score=max_score, weight=weight)
        service.add_assessment(assessment)
        
        return jsonify({"status": "success", "message": f"Added '{name}' successfully!"})
    except (ValueError, TypeError) as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/set-strategy", methods=["POST"])
def set_strategy():
    try:
        data = request.json
        strategy_type = data.get("strategy", "weighted")
        new_strategy = GradeCalculatorFactory.create_calculator(strategy_type)
        service.set_strategy(new_strategy)
        return jsonify({"status": "success", "message": f"Switched strategy to {strategy_type}"})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/report", methods=["GET"])
def get_report():
    report = service.generate_academic_report()
    assessments_data = [
        {
            "name": a.name,
            "score": a.score,
            "max_score": a._max_score,
            "percentage": round(a.percentage, 1),
            "weight": a.weight
        }
        for a in service._assessments
    ]
    return jsonify({
        "report": report,
        "assessments": assessments_data
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)