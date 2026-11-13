from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    # Use the highest existing ID plus one.
    new_id = max((event.id for event in events), default=0) + 1
    new_event = Event(new_id, title.strip())
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# Update an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    for event in events:
        if event.id == event_id:
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({"error": "JSON object required"}), 400

            title = data.get("title")

            if not isinstance(title, str) or not title.strip():
                return jsonify({"error": "Title is required"}), 400

            event.title = title.strip()
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404


# Delete an existing event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event.id == event_id:
            events.remove(event)
            return "", 204

    return jsonify({"error": "Event not found"}), 404