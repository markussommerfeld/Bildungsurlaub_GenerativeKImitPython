#%% packages
import os
from autogen import ConversableAgent
from dotenv import load_dotenv, find_dotenv
 
load_dotenv(find_dotenv())
 
#%% LLM config
llm_config = {
    "config_list": [
        {
            "model": "llama-3.3-70b-versatile",
            "api_key": os.getenv("GROQ_API_KEY"),
            "base_url": "https://api.groq.com/openai/v1",
        }
    ]
}
 
#%% Agent Jack: Text-Ersteller
jack = ConversableAgent(
    name="Jack",
    llm_config=llm_config,
    system_message=(
        "Dein Name ist Jack. "
        "Du bist ein spezialisierter KI-Textexperte für Longform-Content. "
        "Dein Zielpublikum sind KI-interessierte Personen ohne viele Vorkenntnisse. "
        "Schreibe klar, verständlich und strukturiert auf Deutsch."
    ),
    human_input_mode="NEVER",
)
 
#%% Agent Alice: Reviewer
alice = ConversableAgent(
    name="Alice",
    llm_config=llm_config,
    system_message=(
        "Dein Name ist Alice. "
        "Du prüfst Jacks Entwürfe und gibst freundliches, kurzes und bündiges Feedback. "
        "Deine Prüfkriterien sind: "
        "- Rechtschreibung ist korrekt. "
        "- Struktur ist für Verständlichkeit optimiert. "
        "- Der Text ist für KI-Einsteiger mit wenig Vorkenntnissen geeignet. "
        "Gib konkrete, stichpunktartige Verbesserungsvorschläge und, wenn nötig, eine kurze überarbeitete Beispielpassage."
    ),
    human_input_mode="NEVER",
)
 
#%% Iterativer Verbesserungsprozess: 1 Text, 4 Runden
current_text = None
num_iterations = 4
 
for i in range(num_iterations):
    if i == 0:
        # 1. Iteration: Jack erstellt einen neuen Text
        prompt_for_jack = (
            "Bitte schreibe einen verständlichen Einführungsartikel "
            "zum Thema 'KI-Tools für Einsteiger'. "
            "Zielgruppe sind interessierte Personen ohne viele Vorkenntnisse. "
            "Strukturiere den Text mit klaren Abschnitten."
        )
    else:
        # Ab der 2. Iteration: Jack überarbeitet den bisherigen Text basierend auf Alice' Feedback
        prompt_for_jack = (
            "Hier ist der aktuelle Entwurf des Artikels, den du verbessern sollst:\n\n"
            f"{current_text}\n\n"
            "Bitte überarbeite diesen Text basierend auf dem Feedback von Alice, "
            "ohne den Inhalt komplett zu ändern. "
            "Verbessere Struktur, Verständlichkeit und Rechtschreibung, "
            "bleibe bei der Zielgruppe KI-Einsteiger. "
            "Gib nur den überarbeiteten Artikel aus, ohne zusätzliche Erklärungen."
        )
 
    # Jack generiert/überarbeitet den Text
    jack_result = jack.initiate_chat(
        recipient=alice,
        message=prompt_for_jack,
        max_turns=1,
        silent=True,          # keine Konversationsausgabe nach außen
        clear_history=True,   # jede Iteration sauber starten
    )
    current_text = jack_result.chat_history[-1]["content"]
 
    # Alice gibt Feedback auf den aktuellen Text (nur intern genutzt)
    feedback_prompt = (
        "Bitte prüfe den folgenden Artikel von Jack und gib Feedback "
        "gemäß deiner Rolle und Kriterien. "
        "Artikel:\n\n"
        f"{current_text}"
    )
    alice_result = alice.initiate_chat(
        recipient=jack,
        message=feedback_prompt,
        max_turns=1,
        silent=True,
        clear_history=True,
    )
    alice_feedback = alice_result.chat_history[-1]["content"]
 
    # Für die nächste Iteration wird nur implizit angenommen,
    # dass Jack das Feedback kennt (über sein Rollenprompt / Kontext).
    # Wenn du es explizit einbauen willst, kannst du es im prompt_for_jack ergänzen.
 
#%% Ausgabe für Endnutzer: fertiger Artikel ohne Konversation
print("\n===== FINALER ARTIKEL FÜR ENDNUTZER =====\n")
print(current_text)