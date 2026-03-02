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
    students = db.get_all_students()
    return jsonify(students), 200

def _bad_request(msg):
    """
    When you make a bad request, terminate it.
    """
    return jsonify({"error": msg}), 400

@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    course = data.get("course")

    # mark is optional
    mark = data.get("mark", None)

    if not isinstance(name, str) or not name.strip():
        return _bad_request("name must be a non-empty string")
    if not isinstance(course, str) or not course.strip():
        return _bad_request("course must be a non-empty string")

    if mark is not None:
        if not isinstance(mark, int):
            return _bad_request("mark must be an integer")
        if mark < 0 or mark > 100:
            return _bad_request("mark must be between 0 and 100")

    created = db.insert_student(name.strip(), course.strip(), mark)
    return jsonify(created), 200



@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    data = request.get_json(silent=True) or {}
    name = data.get("name", None)
    course = data.get("course", None)
    mark = data.get("mark", None)

    if name is not None and (not isinstance(name, str) or not name.strip()):
        return _bad_request("name must be a non-empty string when provided")
    if course is not None and (not isinstance(course, str) or not course.strip()):
        return _bad_request("course must be a non-empty string when provided")
    if mark is not None:
        if not isinstance(mark, int):
            return _bad_request("mark must be an integer when provided")
        if mark < 0 or mark > 100:
            return _bad_request("mark must be between 0 and 100")

    updated = db.update_student(
        student_id,
        name.strip() if isinstance(name, str) else name,
        course.strip() if isinstance(course, str) else course,
        mark,
    )

    if updated is None:
        return jsonify({"error": "student not found"}), 404

    return jsonify(updated), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted = db.delete_student(student_id)

    if deleted is None:
        return jsonify({"error": "student not found"}), 404
    return jsonify(deleted), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [s.get("mark") for s in students if isinstance(s.get("mark"), int)]

    if not marks:
        return jsonify({"count": 0, "average": None, "min": None, "max": None}), 200

    avg = round(sum(marks) / len(marks), 2)
    return jsonify(
        {"count": len(marks), "average": avg, "min": min(marks), "max": max(marks)},
    ), 200



@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
