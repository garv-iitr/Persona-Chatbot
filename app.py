import os
import gradio as gr
from huggingface_hub import InferenceClient
import sys

sys.path.insert(0, os.path.dirname(__file__))
try:
    from config.persona import persona_identity, PERSONAS
except ImportError:
    persona_identity = "Ethan_Hunt"
    PERSONAS = {
        "Ethan_Hunt": {
            "name": "Ethan Hunt",
            "source": "Mission: Impossible",
            "avatar": "🕵️",
            "greeting": "Agent. I wasn't expecting contact through this channel. This line may be compromised — make it quick. What do you need?",
            "system_prompt": "You are Ethan Hunt, IMF agent. You are professional, intense, and focused on the mission."
        },
        "Yoda": {
            "name": "Yoda",
            "source": "Star Wars",
            "avatar": "🌿",
            "greeting": "Hmm. Arrived, you have. Speak, you must. Listen, I will.",
            "system_prompt": "You are Yoda. Speak in his signature inverted style."
        },
        "Sherlock_Holmes": {
            "name": "Sherlock Holmes",
            "source": "BBC Sherlock",
            "avatar": "🔍",
            "greeting": "Ah. A visitor. Sit down — I've already deduced three things about you.",
            "system_prompt": "You are Sherlock Holmes. Arrogant, brilliant, and observant."
        }
    }

client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct")

current_persona = PERSONAS.get(persona_identity, PERSONAS["Ethan_Hunt"])


def chat(user_message: str, history: list[dict]):
    if not user_message.strip():
        return history, ""

    messages = [{"role": "system", "content": current_persona["system_prompt"]}]

    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=1200,
            temperature=0.8,
            stream=False
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"⚠️ [TRANSMISSION ERROR]: {str(e)}"

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": bot_reply})

    return history, ""


def switch_persona(persona_name):
    global current_persona
    for k, v in PERSONAS.items():
        if v["name"] == persona_name:
            current_persona = v
            break

    new_history = [{"role": "assistant", "content": current_persona["greeting"]}]
    return new_history, f"🕵️ {current_persona['name'].upper()} LINK", f"ENCRYPTED CHANNEL · {current_persona['source'].upper()} · CLASSIFIED"


MISSION_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg: #05070b;
    --surface: rgba(255,255,255,0.04);
    --surface-strong: rgba(255,255,255,0.07);
    --border: rgba(255,255,255,0.12);
    --accent: #7dd3fc;
    --accent-soft: rgba(125,211,252,0.25);
    --text: #e6edf3;
    --muted: #8b949e;
}

/* Global */
body, .gradio-container {
    background: radial-gradient(circle at top, #0b1220, #05070b 60%) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

/* App container */
#app-container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}

/* Header */
.header-title {
    font-size: 1.6rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    color: var(--accent);
}

.header-sub {
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.18em;
}

/* Chat panel */
#chatbot {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(14px);
    padding: 10px;
}

/* Messages */
#chatbot .message.user {
    background: rgba(125,211,252,0.08) !important;
    border-radius: 14px !important;
    border: 1px solid var(--accent-soft) !important;
}

#chatbot .message.bot {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
}

/* Textbox */
#msg-input textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Buttons */
#send-btn {
    background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
    color: #001018 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 0 18px rgba(56,189,248,0.35);
}

#send-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 22px rgba(56,189,248,0.5);
}

#clear-btn {
    background: transparent !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
}

/* Dropdown */
#persona-select {
    background: var(--surface) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* Footer */
.footer {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    margin-top: 12px;
    display: flex;
    justify-content: space-between;
}
"""


with gr.Blocks(css=MISSION_CSS, title="Persona Chatbot") as demo:
    with gr.Column(elem_id="app-container"):
        header_title = gr.HTML(
            f"<div class='header-title'>◈ {current_persona['name'].upper()} LINK</div>")
        header_sub = gr.HTML(
            f"<div class='header-sub'>SECURE CHANNEL · {current_persona['source'].upper()} · AUTHORIZED ACCESS</div>")

        persona_dropdown = gr.Dropdown(
            choices=[p["name"] for p in PERSONAS.values()],
            value=current_persona["name"],
            label="ACTIVE AGENT ▸",
            elem_id="persona-select"
        )

        # noinspection PyTypeChecker
        chatbot = gr.Chatbot(
            value=[{"role": "assistant", "content": current_persona["greeting"]}],
            elem_id="chatbot",
            # type="messages",
            height=450,
            show_label=False
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Send a message... this channel is monitored.",
                show_label=False,
                elem_id="msg-input",
                scale=4
            )
            clear_btn = gr.Button("CLEAR", elem_id="clear-btn", scale=1)
            send_btn = gr.Button("TRANSMIT ▶", elem_id="send-btn", scale=1)

        gr.HTML("""
            <div class='footer'>
             <span>ENCRYPTION: AES-256</span>
             <span>STATUS: SECURE</span>
            </div>
        """)

    send_btn.click(chat, [msg, chatbot], [chatbot, msg])
    msg.submit(chat, [msg, chatbot], [chatbot, msg])
    clear_btn.click(lambda: [{"role": "assistant", "content": current_persona["greeting"]}], None, chatbot)

    persona_dropdown.change(
        switch_persona,
        persona_dropdown,
        [chatbot, header_title, header_sub]
    )

if __name__ == "__main__":
    demo.launch(server_name="localhost", server_port=7860)