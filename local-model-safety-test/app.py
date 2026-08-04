from flask import Flask, jsonify, render_template, request

import db
import ollama_client
import templates_data

app = Flask(__name__)
db.init_db()


@app.route("/")
def index():
    return render_template("index.html", templates=templates_data.TEMPLATES)


@app.route("/api/session/new", methods=["POST"])
def new_session():
    session_id = db.create_session()
    return jsonify({"session_id": session_id})


@app.route("/api/send", methods=["POST"])
def send():
    data = request.get_json()
    session_id = data["session_id"]
    message = data["message"]
    template_id = data["template_id"]

    injected_message = templates_data.wrap_message(template_id, message)

    db.save_message(session_id, "baseline", "user", message)
    db.save_message(session_id, "injected", "user", injected_message, template_id=template_id)

    baseline_history = db.get_history(session_id, "baseline")
    injected_history = db.get_history(session_id, "injected")

    baseline_reply = ollama_client.chat(baseline_history)
    injected_reply = ollama_client.chat(injected_history)

    db.save_message(session_id, "baseline", "assistant", baseline_reply)
    db.save_message(session_id, "injected", "assistant", injected_reply, template_id=template_id)

    return jsonify(
        {
            "baseline_reply": baseline_reply,
            "injected_reply": injected_reply,
            "injected_message": injected_message,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
