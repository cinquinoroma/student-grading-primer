# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation

    # edge cases
    if student_data.get("name") is None:
        abort(404, "Student cannot be created without a name")
    if student_data.get("course") is None:
        abort(404, "Student cannot be created without a course")

    # if empty edge case no students try to retrieve stats and get division by 0 
    if count == 0:
        return jsonify({"count": 0, "average": None, "min": None, "max": None}), 200

        # since mark is optional field 
    marks = [s["mark"] for s in students if s["mark"] is not None]