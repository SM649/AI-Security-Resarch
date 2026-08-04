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


@app.route("/api/sessions")
def sessions():
    return jsonify(db.list_sessions())


@app.route("/api/sessions/<int:session_id>")
def session_detail(session_id):
    return jsonify(
        {
            "baseline": db.get_history(session_id, "baseline"),
            "injected": db.get_history(session_id, "injected"),
        }
    )


@app.route("/api/send", methods=["POST"])
def send():
    data = request.get_json()
    session_id = data["session_id"]
    message = data["message"]
    template_id = data["template_id"]
    target = data.get("target", "both")

    result = {}

    if target in ("both", "baseline"):
        db.save_message(session_id, "baseline", "user", message)
        baseline_history = db.get_history(session_id, "baseline")
        baseline_reply = ollama_client.chat(baseline_history)
        db.save_message(session_id, "baseline", "assistant", baseline_reply)
        result["baseline_reply"] = baseline_reply

    if target in ("both", "injected"):
        injected_message = templates_data.wrap_message(template_id, message)
        db.save_message(session_id, "injected", "user", injected_message, template_id=template_id)
        injected_history = db.get_history(session_id, "injected")
        injected_reply = ollama_client.chat(injected_history)
        db.save_message(session_id, "injected", "assistant", injected_reply, template_id=template_id)
        result["injected_reply"] = injected_reply
        result["injected_message"] = injected_message

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
