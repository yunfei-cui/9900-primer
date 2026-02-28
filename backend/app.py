from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch students"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    try:
        student_data = request.json
        
        # Validate required fields
        if not student_data or "name" not in student_data or "course" not in student_data:
            return jsonify({"error": "Missing required fields: name and course"}), 404
        
        # Validate that name and course are not empty
        name = student_data.get("name", "").strip()
        course = student_data.get("course", "").strip()
        
        if not name or not course:
            return jsonify({"error": "Name and course cannot be empty"}), 404
        
        # Mark is optional, default to 0
        mark = student_data.get("mark", 0)
        
        # Validate mark is an integer
        if not isinstance(mark, int) or mark < 0 or mark > 100:
            return jsonify({"error": "Mark must be an integer between 0 and 100"}), 404
        
        # Insert student
        new_student = db.insert_student(name, course, mark)
        return jsonify(new_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        # Check if student exists
        existing_student = db.get_student_by_id(student_id)
        if not existing_student:
            return jsonify({"error": "Student not found"}), 404
        
        student_data = request.json
        if not student_data:
            return jsonify({"error": "Request body is empty"}), 404
        
        # Extract optional fields
        name = student_data.get("name")
        course = student_data.get("course")
        mark = student_data.get("mark")
        
        # Validate non-empty strings if provided
        if name is not None and isinstance(name, str) and not name.strip():
            return jsonify({"error": "Name cannot be empty"}), 404
        
        if course is not None and isinstance(course, str) and not course.strip():
            return jsonify({"error": "Course cannot be empty"}), 404
        
        # Validate mark if provided
        if mark is not None and (not isinstance(mark, int) or mark < 0 or mark > 100):
            return jsonify({"error": "Mark must be an integer between 0 and 100"}), 404
        
        # Update student
        updated_student = db.update_student(student_id, name, course, mark)
        return jsonify(updated_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        # Check if student exists
        existing_student = db.get_student_by_id(student_id)
        if not existing_student:
            return jsonify({"error": "Student not found"}), 404
        
        # Delete student
        db.delete_student(student_id)
        return jsonify(existing_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        
        if not students:
            return jsonify({
                "count": 0,
                "average": 0,
                "min": None,
                "max": None
            }), 200
        
        marks = [student["mark"] for student in students]
        count = len(marks)
        average = sum(marks) / count
        min_mark = min(marks)
        max_mark = max(marks)
        
        return jsonify({
            "count": count,
            "average": round(average, 2),
            "min": min_mark,
            "max": max_mark
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
