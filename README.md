# 🕵️ Persona Chatbot

A spy-themed AI chatbot that lets you have conversations with your favorite fictional characters.


# 🎭 Available Personas

| Character                  | Source              | Style                           |
| -------------------------- | ------------------- | ------------------------------- |
| **Ethan Hunt** *(default)* | Mission: Impossible | Tactical, tense, spy-speak      |
| **Yoda**                   | Star Wars           | Inverted syntax, ancient wisdom |
| **Sherlock Holmes**        | BBC/Conan Doyle     | Deductive, arrogant, brilliant  |


# 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/garv-iitr/Persona-Chatbot 
cd Persona-Chatbot
pip install -r requirements.txt
```
Repo link :- ([garv-iitr/Persona-Chatbot](https://github.com/garv-iitr/Persona-Chatbot))

### 2. Set your API Key

```bash
# Windows (PowerShell)
$env=HF_TOKEN"hf_..."
```

### 3. Run

```bash
python app.py
```

Open `http://localhost:7860` in your browser.

---

## 🗂 Project Structure

```
Persona-Chatbot/
├── app.py                  # Main Gradio app (UI + chat logic)
├── config/
│   └── persona.py          # Persona definitions & system prompts
├── requirements.txt
└── README.md
```

---

## ✏️ Adding a Custom Persona

Open `config/persona.py` and add a new entry to the `PERSONAS` dict:

```python
"Tony_Stark": {
    "name": "Tony Stark",
    "source": "Marvel / Iron Man",
    "avatar": "🦾",
    "system_prompt": """You are Tony Stark — genius, billionaire, playboy, philanthropist...""",
    "greeting": "JARVIS told me someone wanted to talk. Make it interesting."
}
```

Then set `persona_identity = "Tony_Stark"` as the default, or just select it from the dropdown in the UI.

---

## 🔧 Configuration

| Variable            | Location            | Purpose                    |
| ------------------- | ------------------- | -------------------------- |
| `persona_identity`  | `config/persona.py` | Default persona on startup |
| `HF_TOKEN` | Environment         | API authentication         |
| `server_port`       | `app.py` L157       | Change port (default 7860) |

---

## 💡 How It Works

1. Each persona has a **system prompt** that defines personality, speech patterns, and example dialogue.
2. The full conversation history is passed to LLM Model on Hugging Face (meta-llama in this project) on every turn for coherent multi-turn chat.
3. Gradio provides the UI with a spy-themed CSS skin.
4. Switching personas resets the conversation with a character-appropriate greeting.


