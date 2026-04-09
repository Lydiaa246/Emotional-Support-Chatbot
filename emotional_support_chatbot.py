"""
Emotional Support Chatbot - CLI
A keyword-based emotional support assistant with structured intake,
empathetic responses, coping advice, exercises, and a 5-minute action plan.
"""

from __future__ import annotations

import random
import re
import sys
from typing import Any

# ---------------------------------------------------------------------------
# Emotion knowledge base: keywords, replies, advice, exercises
# ---------------------------------------------------------------------------

EMOTION_DATA: dict[str, dict[str, Any]] = {
    "anxiety": {
        "keywords": [
            "anxious", "anxiety", "worried", "worry", "nervous", "panic",
            "overwhelmed", "on edge", "racing thoughts", "restless", "uneasy",
            "fear", "scared", "tense", "jitters",
        ],
        "response_messages": [
            "It takes courage to name anxiety - you are not alone in feeling this way.",
            "Anxiety often shows up when we care deeply. Your feelings are valid.",
            "Thank you for trusting me with this. We can take this one gentle step at a time.",
        ],
        "advice_suggestions": [
            "Try labeling the worry: \"This is a thought, not a fact\" - it often loosens its grip.",
            "Limit news and social scrolling for a short window; your nervous system will thank you.",
            "Share one honest sentence with someone you trust; connection softens isolation.",
            "Break today into the next 10 minutes only - what is one tiny kind thing you can do?",
        ],
        "exercises": [
            {
                "name": "Deep breathing (4-7-8 style)",
                "steps": [
                    "Inhale quietly through your nose for 4 counts.",
                    "Hold for 7 counts (or whatever feels okay - skip hold if dizzy).",
                    "Exhale slowly through your mouth for 8 counts.",
                    "Repeat 3-4 cycles at your own pace.",
                ],
            },
            {
                "name": "5-4-3-2-1 grounding",
                "steps": [
                    "Name 5 things you can see.",
                    "Name 4 things you can touch or feel.",
                    "Name 3 things you can hear.",
                    "Name 2 things you can smell (or like the smell of).",
                    "Name 1 thing you can taste or one slow breath you feel in your body.",
                ],
            },
            {
                "name": "Short journaling",
                "steps": [
                    "Write for 2 minutes: \"If my anxiety had a color and shape, it would be...\"",
                    "End with: \"One sentence I need to hear today is...\"",
                ],
            },
            {
                "name": "Positive affirmations",
                "steps": [
                    "Say slowly, hand on heart: \"I am safe enough in this moment.\"",
                    "\"I can feel afraid and still choose one small next step.\"",
                    "\"This feeling can move through me; I do not have to fight it alone.\"",
                ],
            },
        ],
    },
    "stress": {
        "keywords": [
            "stress", "stressed", "pressure", "deadline", "burnout", "exhausted",
            "too much", "busy", "rushed", "hectic", "overloaded", "tired",
            "can't cope", "cant cope", "at my limit",
        ],
        "response_messages": [
            "Stress piles up quietly - noticing it is already a form of self-care.",
            "You are carrying a lot. It makes sense that it feels heavy right now.",
            "Thank you for being honest. Even small pauses can change how stress lands.",
        ],
        "advice_suggestions": [
            "Pick one task to defer or delegate; crossing one thing off your mental list helps.",
            "Schedule a 5-minute \"do nothing\" break - staring out a window counts.",
            "Name your top stressor in one line, then ask: what is literally the next tiny action?",
            "Hydrate and stretch shoulders; stress often lives in the body first.",
        ],
        "exercises": [
            {
                "name": "Box breathing",
                "steps": [
                    "Breathe in for 4, hold for 4, out for 4, hold for 4 - like a square.",
                    "Do 4 rounds. Adjust counts so it feels comfortable, not strained.",
                ],
            },
            {
                "name": "5-4-3-2-1 grounding (quick)",
                "steps": [
                    "5 see, 4 touch, 3 hear, 2 smell, 1 taste or breath - say each aloud or in your head.",
                ],
            },
            {
                "name": "Micro-journaling",
                "steps": [
                    "List 3 drains: \"What is draining my battery today?\"",
                    "List 1 recharge: \"What would add 5% energy if I tried it?\"",
                ],
            },
            {
                "name": "Affirmations for overload",
                "steps": [
                    "\"I am allowed to go at a sustainable pace.\"",
                    "\"Done is often braver than perfect.\"",
                    "\"I can reset in small moments; I do not need a full day off to begin.\"",
                ],
            },
        ],
    },
    "sadness": {
        "keywords": [
            "sad", "sadness", "depressed", "depression", "down", "low", "blue",
            "hopeless", "empty", "crying", "cry", "grief", "lost", "melancholy",
            "heavy heart", "unmotivated",
        ],
        "response_messages": [
            "Sadness deserves gentleness, not hurry. I am glad you shared this.",
            "Feeling low does not mean you are weak - it often means you have been strong for a long time.",
            "Your feelings are real. There is no \"right\" timeline for healing.",
        ],
        "advice_suggestions": [
            "One small connection - a text, a voice note - can shift a heavy hour.",
            "If sadness stays heavy for a long time, consider talking with a counselor or doctor; support helps.",
            "Let yourself name the loss or disappointment without fixing it immediately.",
            "Sunlight, a short walk, or a warm shower can be tiny bridges on dark days.",
        ],
        "exercises": [
            {
                "name": "Gentle breathing",
                "steps": [
                    "Place a hand on your belly; breathe so the hand rises slightly.",
                    "Longer exhale than inhale for 5 breaths - like sighing the tension out.",
                ],
            },
            {
                "name": "Grounding with compassion",
                "steps": [
                    "Notice 3 neutral objects in the room (a wall, a chair, light).",
                    "Whisper: \"This is hard, and I am still here.\"",
                ],
            },
            {
                "name": "Journaling prompt",
                "steps": [
                    "Write: \"Today I miss or need...\"",
                    "Then: \"One kind thing I wish someone would say to me is...\"",
                ],
            },
            {
                "name": "Soft affirmations",
                "steps": [
                    "\"It is okay to move slowly today.\"",
                    "\"My worth is not measured by my productivity.\"",
                    "\"Light often returns in small pieces; I can notice one.\"",
                ],
            },
        ],
    },
    "anger": {
        "keywords": [
            "angry", "anger", "mad", "furious", "rage", "irritated", "annoyed",
            "frustrated", "resentful", "betrayed", "unfair", "heated",
        ],
        "response_messages": [
            "Anger often signals a boundary or value being crossed - your reaction makes sense.",
            "You can feel angry and still choose how you act. Both things can be true.",
            "Thank you for naming it. Anger held alone can grow; shared, it can clarify.",
        ],
        "advice_suggestions": [
            "Before acting, pause: name what you need (respect, space, apology, clarity).",
            "Physical outlet: punch a pillow, fast walk, or squeeze fists then release - safely.",
            "Write an unsent letter - get it out without sending until you are calmer.",
            "If anger is frequent or explosive, a therapist can be a powerful ally.",
        ],
        "exercises": [
            {
                "name": "Cooling breath",
                "steps": [
                    "Exhale fully through the mouth with a whoosh.",
                    "Inhale through the nose for 4, exhale longer through the mouth for 6-8.",
                    "Repeat until your jaw unclenches slightly.",
                ],
            },
            {
                "name": "Grounding + body scan",
                "steps": [
                    "Plant feet flat; press down and notice solid floor.",
                    "Scan: shoulders, jaw, hands - unclench what you can, one area at a time.",
                ],
            },
            {
                "name": "Journaling",
                "steps": [
                    "Complete: \"I am angry because...\"",
                    "Then: \"Under the anger, I might also feel...\"",
                ],
            },
            {
                "name": "Affirmations",
                "steps": [
                    "\"My anger is information; I can listen without letting it drive.\"",
                    "\"I deserve respect; I can ask for it clearly when I am ready.\"",
                ],
            },
        ],
    },
    "loneliness": {
        "keywords": [
            "lonely", "loneliness", "alone", "isolated", "disconnected", "no one",
            "nobody", "left out", "invisible", "ignored", "solitude hurts",
        ],
        "response_messages": [
            "Loneliness hurts - and naming it is a brave step toward relief.",
            "Wanting connection is deeply human; you are not \"too much\" for needing people.",
            "Thank you for being honest. Even one small reach-out can matter more than it seems.",
        ],
        "advice_suggestions": [
            "Try low-stakes contact: comment on a post, message an old friend \"thinking of you.\"",
            "Join one recurring thing - a class, volunteer shift, or online group - rhythm builds bonds.",
            "If loneliness feels crushing or constant, professional support is a sign of strength, not weakness.",
            "Companion yourself kindly today: music, pet, favorite drink, cozy corner counts.",
        ],
        "exercises": [
            {
                "name": "Warm breathing",
                "steps": [
                    "Imagine warmth on your chest as you breathe in for 4 and out for 6.",
                    "Picture one person (even fictional) who \"gets\" you - hold that image one breath.",
                ],
            },
            {
                "name": "Sensory grounding",
                "steps": [
                    "Wrap in a blanket or hold something textured.",
                    "Name out loud: \"I am here; this moment is real\" - simple but anchoring.",
                ],
            },
            {
                "name": "Journaling",
                "steps": [
                    "Write: \"What kind of connection am I craving - witness, play, depth, help?\"",
                    "One tiny step I could try this week:",
                ],
            },
            {
                "name": "Affirmations",
                "steps": [
                    "\"I belong to the human family; loneliness is a feeling, not a verdict.\"",
                    "\"I am worth knowing; I can take one small social risk.\"",
                ],
            },
        ],
    },
    "happiness": {
        "keywords": [
            "happy", "happiness", "joy", "glad", "good", "great", "excited",
            "grateful", "thankful", "blessed", "content", "peaceful", "hopeful",
            "optimistic", "wonderful", "awesome",
        ],
        "response_messages": [
            "It is wonderful to hear you are in a lighter place - thank you for sharing that.",
            "Joy matters too; you deserve to savor it without waiting for permission.",
            "I am genuinely glad you are feeling good. Let us help you keep some of this glow.",
        ],
        "advice_suggestions": [
            "Savor it: name 3 specific things that contributed to this good feeling.",
            "Share the good news with someone - happiness grows when it is witnessed.",
            "Note what helped (sleep, people, activity) so you can revisit the recipe gently.",
            "Help someone small today; meaning often walks hand-in-hand with joy.",
        ],
        "exercises": [
            {
                "name": "Gratitude breathing",
                "steps": [
                    "Each inhale, think of one good thing; each exhale, send wishes for it to last.",
                    "Three breaths, three appreciations - big or tiny.",
                ],
            },
            {
                "name": "Grounding in the good",
                "steps": [
                    "Name 5 pleasant sensations right now (light, sound, warmth, taste, touch).",
                    "Store this list in your phone for harder days.",
                ],
            },
            {
                "name": "Journaling",
                "steps": [
                    "\"Today I feel good because...\"",
                    "\"I want to remember this feeling when I write:\"",
                ],
            },
            {
                "name": "Affirmations",
                "steps": [
                    "\"I allow myself to feel joy without guilt.\"",
                    "\"Good moments are real; I can trust that more will come.\"",
                ],
            },
        ],
    },
}


MOTIVATIONAL_MESSAGES: list[str] = [
    "You have already done something important by checking in with yourself today.",
    "Small steps count. Progress is not always visible - that does not mean it is absent.",
    "You are allowed to need support. Asking for help is wisdom, not weakness.",
    "This moment is one page in your story, not the whole book.",
    "Be as patient with yourself as you would be with a good friend.",
]


def clean_input(text: str) -> str:
    """
    Basic NLP-style normalization: lowercase, collapse whitespace,
    strip edges, keep apostrophes for contractions.
    """
    if not text:
        return ""
    # Lowercase for consistent keyword matching
    t = text.lower().strip()
    # Collapse repeated spaces and normalize quotes/apostrophe variants lightly
    t = re.sub(r"\s+", " ", t)
    t = t.replace("’", "'")
    return t


def detect_emotion(text: str) -> tuple[str, dict[str, int]]:
    """
    Keyword-based emotion detection. Returns (primary_emotion, scores_per_category).
    If no keywords match, returns ("neutral", scores).

    Uses substring match for multi-word phrases; for single-word keywords, uses
    whole-word matching to reduce false positives (e.g. \"mad\" vs \"made\").
    """
    cleaned = clean_input(text)
    scores: dict[str, int] = {e: 0 for e in EMOTION_DATA}

    for emotion, data in EMOTION_DATA.items():
        for kw in data["keywords"]:
            kw_l = kw.lower()
            if " " in kw_l:
                if kw_l in cleaned:
                    scores[emotion] += 1
            elif re.search(r"\b" + re.escape(kw_l) + r"\b", cleaned):
                scores[emotion] += 1

    max_score = max(scores.values()) if scores else 0
    if max_score == 0:
        return "neutral", scores

    # Pick top emotion; break ties with stable order preference (support heavier states first)
    tie_order = ["sadness", "anxiety", "stress", "anger", "loneliness", "happiness"]
    tied = [e for e, s in scores.items() if s == max_score]
    for pref in tie_order:
        if pref in tied:
            return pref, scores

    return tied[0], scores


def generate_response(
    primary_emotion: str,
    intensity: int | None = None,
) -> str:
    """
    Build an empathetic reply using emotion-specific messages,
    optional intensity-aware nuance, and a motivational close.
    """
    parts: list[str] = []

    if primary_emotion == "neutral":
        parts.append(
            "I hear you. It can be hard to label feelings - whatever you are carrying still matters."
        )
        generic_advice = [
            "Try naming one body sensation and one emotion - curiosity, not judgment.",
            "A five-minute walk, water, or fresh air can shift the edges of a foggy mood.",
            "If something specific is worrying you, write one sentence: what is actually in my control?",
        ]
        parts.append(random.choice(generic_advice))
    else:
        data = EMOTION_DATA[primary_emotion]
        parts.append(random.choice(data["response_messages"]))
        parts.append(random.choice(data["advice_suggestions"]))

    if intensity is not None:
        if intensity >= 8:
            parts.append(
                "That sounds really intense right now. Please consider reaching out to a professional "
                "or crisis line if you ever feel unsafe - you deserve real-time support."
            )
        elif intensity >= 5:
            parts.append(
                "A mid-to-high intensity day calls for extra gentleness - tiny steps are enough."
            )

    parts.append(random.choice(MOTIVATIONAL_MESSAGES))
    return " ".join(parts)


def suggest_exercise(primary_emotion: str) -> str:
    """Format one recommended exercise (breathing, grounding, journaling, or affirmations)."""
    if primary_emotion == "neutral" or primary_emotion not in EMOTION_DATA:
        primary_emotion = random.choice(list(EMOTION_DATA.keys()))

    ex = random.choice(EMOTION_DATA[primary_emotion]["exercises"])
    lines = [f"\n--- {ex['name']} ---"]
    for i, step in enumerate(ex["steps"], 1):
        lines.append(f"  {i}. {step}")
    return "\n".join(lines)


def create_action_plan(
    primary_emotion: str,
    intensity: int | None,
    duration_note: str,
) -> str:
    """
    Build a structured ~5-minute action plan with time boxes.
    """
    ex_name = "Deep breathing or 5-4-3-2-1 grounding"
    if primary_emotion in EMOTION_DATA:
        sample = EMOTION_DATA[primary_emotion]["exercises"][0]
        ex_name = sample["name"]

    mins = [
        ("0:00-1:00", "Hydrate; unclench jaw and shoulders; one slow exhale."),
        ("1:00-3:00", f"Try: {ex_name} - follow the steps at your own pace."),
        ("3:00-4:00", "Journal 3 lines: what I feel / what I need / one kind next step."),
        ("4:00-5:00", "Text someone, step outside for fresh air, or play one calm song."),
    ]

    header = [
        "\n========== Your ~5-minute action plan ==========",
        f"Detected focus area: {primary_emotion.replace('_', ' ').title()}",
    ]
    if intensity is not None:
        header.append(f"You rated intensity: {intensity}/10")
    if duration_note.strip():
        header.append(f"You've felt this way for: {duration_note.strip()}")

    body = [f"{slot}: {action}" for slot, action in mins]
    footer = [
        "After 5 minutes, check in: +1 if slightly better, same, or worse - all data is useful.",
        "==================================================",
    ]
    return "\n".join(header + [""] + body + [""] + footer)


def chatbot_loop() -> None:
    """Main CLI: structured questions, detection, support pack, repeat until 'quit'."""
    print("\n" + "=" * 54)
    print("  Emotional Support Chatbot - you are not alone")
    print("=" * 54)
    print(
        "\nThis is a supportive tool, not a substitute for professional care "
        "in a crisis.\nType 'quit' anytime to exit.\n"
    )

    while True:
        print("\n--- New check-in ---\n")
        print("Hello. I am here to listen without judgment.")
        feeling_today = input('How are you feeling today?\n> ')
        if clean_input(feeling_today) == "quit":
            print("\nTake care of yourself. Goodbye.\n")
            break

        emotions_in = input("\nWhat emotions are you feeling? (name as many as you like)\n> ")
        if clean_input(emotions_in) == "quit":
            print("\nTake care of yourself. Goodbye.\n")
            break

        cause = input("\nWhat do you think caused this feeling, or what is on your mind?\n> ")
        if clean_input(cause) == "quit":
            print("\nTake care of yourself. Goodbye.\n")
            break

        raw_intensity = input("\nHow intense is it? (1 = mild, 10 = overwhelming)\n> ")
        if clean_input(raw_intensity) == "quit":
            print("\nTake care of yourself. Goodbye.\n")
            break

        duration = input("\nHow long have you felt this way?\n> ")
        if clean_input(duration) == "quit":
            print("\nTake care of yourself. Goodbye.\n")
            break

        # Parse intensity 1-10
        intensity: int | None = None
        m = re.search(r"\b(\d{1,2})\b", raw_intensity.strip())
        if m:
            v = int(m.group(1))
            if 1 <= v <= 10:
                intensity = v

        combined = f"{feeling_today} {emotions_in} {cause}"
        primary, _scores = detect_emotion(combined)

        print("\n" + "-" * 54)
        print("  Summary")
        print("-" * 54)
        print(generate_response(primary, intensity))

        print("\n" + "-" * 54)
        print("  Suggested exercise")
        print("-" * 54)
        print(suggest_exercise(primary))

        print(create_action_plan(primary, intensity, duration))

        print(
            "\n[Tip] Type anything and press Enter for another check-in, or 'quit' to leave."
        )
        again = input("> ")
        if clean_input(again) == "quit":
            print("\nTake care of yourself. Goodbye.\n")
            break


def main() -> None:
    try:
        chatbot_loop()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Wishing you peace. Goodbye.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
