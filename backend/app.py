# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import uuid
# from datetime import datetime

# from firebase_config import db 

# app = Flask(__name__)
# CORS(app)

# # Sample initial data
# students = [
#     {
#         "id": "1",
#         "name": "Alice Johnson",
#         "email": "alice@example.com",
#         "country": "USA",
#         "status": "Exploring",
#         "last_active": "2025-09-14",
#         "phone": "1234567890",
#         "grade": "12",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "2",
#         "name": "Rahul Sharma",
#         "email": "rahul@example.com",
#         "country": "India",
#         "status": "Applying",
#         "last_active": "2025-09-12",
#         "phone": "9876543210",
#         "grade": "12",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "3",
#         "name": "Sofia Martinez",
#         "email": "sofia@example.com",
#         "country": "Spain",
#         "status": "Enrolled",
#         "last_active": "2025-09-10",
#         "phone": "2345678901",
#         "grade": "11",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "4",
#         "name": "Liam O'Connor",
#         "email": "liam@example.com",
#         "country": "Ireland",
#         "status": "Exploring",
#         "last_active": "2025-09-15",
#         "phone": "3456789012",
#         "grade": "10",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "5",
#         "name": "Chloe Wang",
#         "email": "chloe@example.com",
#         "country": "China",
#         "status": "Applying",
#         "last_active": "2025-09-11",
#         "phone": "4567890123",
#         "grade": "12",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "6",
#         "name": "Ethan Brown",
#         "email": "ethan@example.com",
#         "country": "Canada",
#         "status": "Enrolled",
#         "last_active": "2025-09-13",
#         "phone": "5678901234",
#         "grade": "11",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "7",
#         "name": "Maria Rossi",
#         "email": "maria@example.com",
#         "country": "Italy",
#         "status": "Exploring",
#         "last_active": "2025-09-09",
#         "phone": "6789012345",
#         "grade": "12",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "8",
#         "name": "Noah Kim",
#         "email": "noah@example.com",
#         "country": "South Korea",
#         "status": "Applying",
#         "last_active": "2025-09-14",
#         "phone": "7890123456",
#         "grade": "12",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "9",
#         "name": "Emma Müller",
#         "email": "emma@example.com",
#         "country": "Germany",
#         "status": "Enrolled",
#         "last_active": "2025-09-12",
#         "phone": "8901234567",
#         "grade": "11",
#         "notes": [],
#         "communications": []
#     },
#     {
#         "id": "10",
#         "name": "Oliver Smith",
#         "email": "oliver@example.com",
#         "country": "UK",
#         "status": "Exploring",
#         "last_active": "2025-09-10",
#         "phone": "9012345678",
#         "grade": "10",
#         "notes": [],
#         "communications": []
#     }
# ]

# ref = db.reference("students")
# existing_data = ref.get()
# if not existing_data:
#     for s in students:
#         ref.child(s["id"]).set(s)

# # GET ALL STUDENTS
# @app.route("/students", methods=["GET"])
# def get_students():
#     students_ref = db.reference("students").get()
#     return jsonify(students_ref if students_ref else {})

# # GET ONE STUDENT
# @app.route("/students/<student_id>", methods=["GET"])
# def get_student(student_id):
#     student = db.reference(f"students/{student_id}").get()
#     if student:
#         return jsonify(student)
#     return jsonify({"error": "Student not found"}), 404

# # ADD NOTE TO STUDENT
# @app.route("/students/<student_id>/notes", methods=["POST"])
# def add_note(student_id):
#     data = request.get_json()
#     note = {
#         "id": str(uuid.uuid4()),
#         "text": data.get("text", ""),
#         "timestamp": datetime.now().isoformat()
#     }
#     student_ref = db.reference(f"students/{student_id}")
#     student = student_ref.get()

#     if student:
#         notes = student.get("notes", [])
#         notes.append(note)
#         student_ref.update({"notes": notes})
#         return jsonify(note), 201
#     return jsonify({"error": "Student not found"}), 404

# # ADD COMMUNICATION TO STUDENT
# @app.route("/students/<student_id>/communications", methods=["POST"])
# def add_communication(student_id):
#     data = request.get_json()
#     comm = {
#         "id": str(uuid.uuid4()),
#         "type": data.get("type", "email"),
#         "message": data.get("message", ""),
#         "timestamp": datetime.now().isoformat()
#     }
#     student_ref = db.reference(f"students/{student_id}")
#     student = student_ref.get()

#     if student:
#         communications = student.get("communications", [])
#         communications.append(comm)
#         student_ref.update({"communications": communications})
#         return jsonify(comm), 201
#     return jsonify({"error": "Student not found"}), 404


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from datetime import datetime, timedelta

from firebase_config import db  # must export firebase_admin.db reference

app = Flask(__name__)
CORS(app)


def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def student_ref(student_id):
    return db.reference(f"students/{student_id}")


def top_level_students_ref():
    return db.reference("students")


def safe_children_as_list(node_dict):
    """
    Converts a dict of children into a list, filtering out null/None.
    Returns [] if node_dict is None.
    """
    if not node_dict:
        return []
    out = []
    for k, v in (node_dict.items() if isinstance(node_dict, dict) else []):
        if v:
            out.append(v)
    return out


# ------------------------
# STUDENTS - CRUD & LIST
# ------------------------
@app.route("/students", methods=["GET"])
def get_students():
    """
    Optional query params:
      - q : text search (on name/email)
      - status : filter by status
      - not_contacted_days : int => students with last communication older than X days or no communications
    """
    q = request.args.get("q", "").lower()
    status_filter = request.args.get("status")
    not_contacted_days = request.args.get("not_contacted_days", type=int)

    all_students = top_level_students_ref().get()  # returns dict or None
    if not all_students:
        return jsonify([])

    students_list = []
    for sid, s in all_students.items():
        if not s:
            continue
        s_copy = s.copy()
        s_copy["id"] = sid
        # apply basic text search
        if q:
            if q not in (s_copy.get("name", "").lower() + s_copy.get("email", "").lower()):
                continue
        # status filter
        if status_filter and s_copy.get("status") != status_filter:
            continue
        # not_contacted_days filter
        if not_contacted_days is not None:
            comms = s_copy.get("communications", {})
            # if no communications => include
            if not comms:
                pass
            else:
                # find last communication timestamp
                latest = None
                for _, c in comms.items():
                    ts = c.get("timestamp")
                    if ts:
                        try:
                            t = datetime.fromisoformat(ts.replace("Z", ""))
                            if latest is None or t > latest:
                                latest = t
                        except Exception:
                            continue
                if latest:
                    cutoff = datetime.utcnow() - timedelta(days=not_contacted_days)
                    if latest > cutoff:
                        continue  # they've been contacted within window -> skip
        students_list.append(s_copy)

    return jsonify(students_list)


@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json() or {}
    new_id = data.get("id") or str(uuid.uuid4())
    student_payload = {
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "country": data.get("country", ""),
        "status": data.get("status", "Exploring"),
        "last_active": data.get("last_active") or now_iso(),
        "phone": data.get("phone", ""),
        "grade": data.get("grade", ""),
        "notes": {},
        "communications": {},
        "interactions": {},
        "tasks": {}
    }
    top_level_students_ref().child(new_id).set(student_payload)
    student_payload["id"] = new_id
    return jsonify(student_payload), 201


@app.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    s = student_ref(student_id).get()
    if not s:
        return jsonify({"error": "Student not found"}), 404
    s["id"] = student_id
    return jsonify(s)


@app.route("/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json() or {}
    ref = student_ref(student_id)
    if not ref.get():
        return jsonify({"error": "Student not found"}), 404
    # only update allowed fields
    allowed = ["name", "email", "country", "status", "last_active", "phone", "grade"]
    updates = {k: v for k, v in data.items() if k in allowed}
    if updates:
        ref.update(updates)
    updated = ref.get()
    updated["id"] = student_id
    return jsonify(updated)


@app.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    ref = student_ref(student_id)
    if not ref.get():
        return jsonify({"error": "Student not found"}), 404
    ref.delete()
    return jsonify({"message": f"Student {student_id} deleted"}), 200


# ------------------------
# NOTES
# ------------------------
@app.route("/students/<student_id>/notes", methods=["GET"])
def list_notes(student_id):
    s = student_ref(student_id).get()
    if not s:
        return jsonify({"error": "Student not found"}), 404
    notes = s.get("notes") or {}
    # return as list
    notes_list = [v for k, v in notes.items() if v]
    return jsonify(notes_list)


@app.route("/students/<student_id>/notes", methods=["POST"])
def add_note(student_id):
    data = request.get_json() or {}
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    nid = data.get("id") or str(uuid.uuid4())
    note = {
        "id": nid,
        "text": data.get("text", ""),
        "author": data.get("author", "team"),
        "timestamp": data.get("timestamp", now_iso())
    }
    existing = student.get("notes") or {}
    existing[nid] = note
    ref.update({"notes": existing})
    return jsonify(note), 201


@app.route("/students/<student_id>/notes/<note_id>", methods=["PUT"])
def edit_note(student_id, note_id):
    data = request.get_json() or {}
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    notes = student.get("notes") or {}
    if note_id not in notes:
        return jsonify({"error": "Note not found"}), 404
    note = notes[note_id]
    note["text"] = data.get("text", note.get("text"))
    note["author"] = data.get("author", note.get("author"))
    note["edited_at"] = now_iso()
    notes[note_id] = note
    ref.update({"notes": notes})
    return jsonify(note)


@app.route("/students/<student_id>/notes/<note_id>", methods=["DELETE"])
def delete_note(student_id, note_id):
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    notes = student.get("notes") or {}
    if note_id not in notes:
        return jsonify({"error": "Note not found"}), 404
    notes.pop(note_id)
    ref.update({"notes": notes})
    return jsonify({"message": "Note deleted"}), 200


# ------------------------
# COMMUNICATIONS
# ------------------------
@app.route("/students/<student_id>/communications", methods=["GET"])
def list_comms(student_id):
    s = student_ref(student_id).get()
    if not s:
        return jsonify({"error": "Student not found"}), 404
    comms = s.get("communications") or {}
    return jsonify([v for k, v in comms.items() if v])


@app.route("/students/<student_id>/communications", methods=["POST"])
def add_comm(student_id):
    data = request.get_json() or {}
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    cid = data.get("id") or str(uuid.uuid4())
    comm = {
        "id": cid,
        "type": data.get("type", "email"),
        "message": data.get("message", ""),
        "channel": data.get("channel", "email"),
        "timestamp": data.get("timestamp", now_iso()),
        "by": data.get("by", "team")
    }
    existing = student.get("communications") or {}
    existing[cid] = comm
    ref.update({"communications": existing})
    return jsonify(comm), 201


@app.route("/students/<student_id>/communications/<comm_id>", methods=["PUT"])
def edit_comm(student_id, comm_id):
    data = request.get_json() or {}
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    comms = student.get("communications") or {}
    if comm_id not in comms:
        return jsonify({"error": "Communication not found"}), 404
    comm = comms[comm_id]
    comm["message"] = data.get("message", comm.get("message"))
    comm["type"] = data.get("type", comm.get("type"))
    comm["edited_at"] = now_iso()
    comms[comm_id] = comm
    ref.update({"communications": comms})
    return jsonify(comm)


@app.route("/students/<student_id>/communications/<comm_id>", methods=["DELETE"])
def delete_comm(student_id, comm_id):
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    comms = student.get("communications") or {}
    if comm_id not in comms:
        return jsonify({"error": "Communication not found"}), 404
    comms.pop(comm_id)
    ref.update({"communications": comms})
    return jsonify({"message": "Communication deleted"}), 200


# ------------------------
# INTERACTIONS (timeline)
# ------------------------
@app.route("/students/<student_id>/interactions", methods=["GET"])
def list_interactions(student_id):
    s = student_ref(student_id).get()
    if not s:
        return jsonify({"error": "Student not found"}), 404
    interactions = s.get("interactions") or {}
    return jsonify([v for k, v in interactions.items() if v])


@app.route("/students/<student_id>/interactions", methods=["POST"])
def add_interaction(student_id):
    data = request.get_json() or {}
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    iid = data.get("id") or str(uuid.uuid4())
    interaction = {
        "id": iid,
        "type": data.get("type", "login"),  # login, doc_upload, ai_question, etc
        "payload": data.get("payload", {}),
        "timestamp": data.get("timestamp", now_iso())
    }
    existing = student.get("interactions") or {}
    existing[iid] = interaction
    ref.update({"interactions": existing})
    return jsonify(interaction), 201


# ------------------------
# INSIGHTS & FILTERS
# ------------------------
@app.route("/insights/summary", methods=["GET"])
def insights_summary():
    all_students = top_level_students_ref().get() or {}
    total = 0
    status_counts = {}
    for sid, s in all_students.items():
        if not s:
            continue
        total += 1
        status = s.get("status", "Unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    return jsonify({"total": total, "by_status": status_counts})


@app.route("/insights/filters", methods=["GET"])
def insights_filters():
    # currently supports: not_contacted_days and needs_essay flag (mock)
    not_contacted_days = request.args.get("not_contacted_days", type=int)
    needs_essay = request.args.get("needs_essay")  # expecting "true" / "false"
    all_students = top_level_students_ref().get() or {}
    out = []
    for sid, s in all_students.items():
        if not s:
            continue
        include = True
        if not_contacted_days is not None:
            comms = s.get("communications") or {}
            if not comms:
                include = True
            else:
                latest = None
                for _, c in comms.items():
                    ts = c.get("timestamp")
                    if ts:
                        try:
                            t = datetime.fromisoformat(ts.replace("Z", ""))
                            if latest is None or t > latest:
                                latest = t
                        except Exception:
                            continue
                if latest:
                    cutoff = datetime.utcnow() - timedelta(days=not_contacted_days)
                    if latest > cutoff:
                        include = False
        if needs_essay is not None:
            # mock: if student has "notes" where one contains "essay" tag, assume needs help
            wants = (needs_essay.lower() == "true")
            notes = s.get("notes") or {}
            has_essay_tag = any("essay" in (n.get("text", "").lower()) for n in notes.values())
            if wants != has_essay_tag:
                include = False
        if include:
            s_copy = s.copy()
            s_copy["id"] = sid
            out.append(s_copy)
    return jsonify(out)


# ------------------------
# MOCK ACTIONS: send_followup, tasks
# ------------------------
@app.route("/students/<student_id>/send_followup", methods=["POST"])
def send_followup(student_id):
    """
    Mock sending an email: just log a communication of type 'email' and return simulated result
    Request body: { "subject": "...", "body": "...", "by": "advisor name" }
    """
    data = request.get_json() or {}
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    cid = str(uuid.uuid4())
    comm = {
        "id": cid,
        "type": "followup_email",
        "channel": "email",
        "subject": data.get("subject", "Follow up from Undergraduation"),
        "message": data.get("body", ""),
        "timestamp": now_iso(),
        "by": data.get("by", "system")
    }
    comms = student.get("communications") or {}
    comms[cid] = comm
    ref.update({"communications": comms})
    # mock response: pretend we queued it
    return jsonify({"status": "queued", "comm": comm}), 200


@app.route("/students/<student_id>/tasks", methods=["POST"])
def add_task(student_id):
    """
    Schedule a task for internal team: { title, due_date, assignee }
    """
    data = request.get_json() or {}
    ref = student_ref(student_id)
    student = ref.get()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    tid = str(uuid.uuid4())
    task = {
        "id": tid,
        "title": data.get("title", "Follow-up"),
        "due_date": data.get("due_date"),
        "assignee": data.get("assignee"),
        "created_at": now_iso(),
        "status": "open",
        "notes": data.get("notes", "")
    }
    tasks = student.get("tasks") or {}
    tasks[tid] = task
    ref.update({"tasks": tasks})
    return jsonify(task), 201


if __name__ == "__main__":
    app.run(debug=True)
