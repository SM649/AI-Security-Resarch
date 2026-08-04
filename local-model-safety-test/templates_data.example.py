import base64


def _roleplay_override(message):
    return f"{message}"


def _hypothetical_fictional(message):
    return f"{message}"


def _instruction_override(message):
    return f"{message}"


def _encoding_trick(message):
    encoded = base64.b64encode(message.encode("utf-8")).decode("ascii")
    return f"{encoded}"


def _authority_framing(message):
    return f"{message}"


TEMPLATES = {
    "roleplay_override": {
        "label": "Role-play override (DAN-style)",
        "wrap": _roleplay_override,
    },
    "hypothetical_fictional": {
        "label": "Hypothetical / fictional framing",
        "wrap": _hypothetical_fictional,
    },
    "instruction_override": {
        "label": "Instruction override",
        "wrap": _instruction_override,
    },
    "encoding_trick": {
        "label": "Encoding trick (base64)",
        "wrap": _encoding_trick,
    },
    "authority_framing": {
        "label": "Authority framing",
        "wrap": _authority_framing,
    },
}


def wrap_message(template_id, message):
    template = TEMPLATES[template_id]
    return template["wrap"](message)
