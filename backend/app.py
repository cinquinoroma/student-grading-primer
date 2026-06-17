from flask import Flask, jsonify, request, abort
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
    student_data = request.json

    # edge cases
    if student_data.get("name") is None:
        abort(404, "Student cannot be created without a name")
    if student_data.get("course") is None:
        abort(404, "Student cannot be created without a course")

    student_name = student_data.get("name")
    student_course = student_data.get("course")

    # mark is optional
    result = db.insert_student(student_name, student_course, student_data.get("mark"))
    return jsonify(result), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """

    student_data = request.json
    student_name = student_data.get("name")
    student_course = student_data.get("course")

    result = db.update_student(student_id, student_name, student_course, student_data.get("mark"))

    if result is None:
        abort(404, "Student id does not exist")

    return jsonify(result), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """

    result = db.delete_student(student_id)

    if result is None:
        abort(404, "Student was not found")

    return jsonify(result), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    # since mark is optional field 
    marks = [s["mark"] for s in students if s["mark"] is not None]

    count = len(marks)
    
    # if empty edge case
    if count == 0:
        return jsonify({"count": 0, "average": None, "min": None, "max": None}), 200

    total = sum(marks)
    min_mark = min(marks)
    max_mark = max(marks)
    avg_mark = total / count

    return jsonify({"count": count, "average": avg_mark, "min": min_mark, "max": max_mark}), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
