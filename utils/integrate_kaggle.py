"""
Kaggle Dataset Integration — merges the Mental Health Conversational Data
(kaggle_mental_health_raw.json) into MindMate AI's response format.

Adds new patterns for better intent matching and enriches responses
with pookie tone and emojis.
"""

import json
import os

# Map Kaggle tags → MindMate categories
TAG_TO_CATEGORY = {
    # Direct emotional categories
    'sad': 'sadness',
    'depressed': 'sadness',
    'worthless': 'sadness',
    'stressed': 'stress',
    'anxious': 'anxiety',
    'scared': 'anxiety',
    'sleep': 'sleep',
    'death': 'grief',
    'suicide': 'crisis',
    'happy': 'gratitude',

    # Conversational
    'greeting': 'greeting',
    'morning': 'greeting',
    'afternoon': 'greeting',
    'evening': 'greeting',
    'thanks': 'gratitude',
    'goodbye': 'goodbye',

    # Situational
    'not-talking': 'reluctant',
    'understand': 'frustration',
    'hate-you': 'frustration',
    'hate-me': 'self_doubt',
    'friends': 'loneliness',
    'problem': 'academic_stress',
    'no-approach': 'academic_stress',
    'default': 'default',

    # Mental health education
    'fact-1': 'mental_health_info',
    'fact-2': 'mental_health_info',
    'fact-3': 'mental_health_info',
    'fact-5': 'mental_health_info',
    'fact-6': 'mental_health_info',
    'fact-7': 'mental_health_info',
    'learn-mental-health': 'mental_health_info',
    'mental-health-fact': 'mental_health_info',

    # Advice & coping
    'meditation': 'coping',
    'user-meditation': 'coping',
    'learn-more': 'coping',
    'user-agree': 'coping',
    'user-advice': 'default',
}

# Pookie-fied responses for new categories from Kaggle
POOKIE_OVERRIDES = {
    'grief': {
        'keywords': ['died', 'death', 'passed away', 'lost someone', 'funeral', 'mourning', 'grief', 'grieving', 'मृत्यु', 'मर गया', 'गेले', 'निधन'],
        'responses': [
            "Oh pookie, I am so incredibly sorry for your loss 😢💛 Grief is one of the most painful things a human can go through, and there are no right words for this moment. Just know that I'm here, and it's okay to feel everything you're feeling. You don't have to be strong right now. 🫂",
            "I'm really, truly sorry 💔 Losing someone you love changes everything. Please be gentle with yourself right now — grief doesn't have a timeline, and however you're processing this is valid. I'm here whenever you need to talk, day or night. 🕊️💛",
            "My heart goes out to you, pookie 🥺 I can't imagine how much pain you're in right now. Just know you're not alone in this — I'm here to listen, to sit with you in silence, or to talk. Whatever you need. Your loved one's memory lives on in you. 💛🌟",
            "I'm so sorry for your loss 😢 You don't have to go through this alone. Take all the time you need to grieve — there's no right or wrong way to do it. And please remember to take care of yourself too, okay? Eat, drink water, rest when you can. 🫶💕"
        ]
    },
    'crisis': {
        'keywords': ['kill myself', 'suicide', 'want to die', 'end my life', 'no reason to live', 'आत्महत्या', 'मरना चाहता', 'जगायचे नाही'],
        'responses': [
            "I hear you, and I'm really glad you told me this 💛 What you're feeling right now is so painful, but I need you to know — your life matters. Please, please reach out to a professional who can truly help right now:\n\n📞 iCall: 9152987821\n📞 Vandrevala Foundation: 1860-2662-345\n📞 AASRA: 9820466726\n📞 JSPM Wagholi Counseling Cell\n\nYou are not alone. People care about you, including me. 🫂💛",
            "Pookie, thank you for trusting me with something this heavy 🥺 I care about you so much, and I want you to be safe. Please talk to someone who can really help:\n\n📞 iCall: 9152987821\n📞 Vandrevala Foundation: 1860-2662-345\n📞 AASRA: 9820466726\n\nYou have so much ahead of you, even if it doesn't feel that way right now. Please reach out. 💛🫶"
        ]
    },
    'reluctant': {
        'keywords': ["don't want to talk", "leave me alone", "shut up", "go away", "stay away", "बात नहीं", "बोलायचे नाही"],
        'responses': [
            "That's completely okay, pookie 💛 You don't have to talk if you're not ready. I'll be right here whenever you feel like opening up — no pressure, no timeline. Just know this is YOUR safe space, always. 🤗",
            "I understand, and I respect that 🫶 Sometimes we just need to sit with our feelings for a while. Whenever you're ready, I'll be here. Even if it's just to say hi. You matter to me. 💛✨",
            "No pressure at all, babe 💕 Not being ready to talk is totally valid. I'll be here — today, tomorrow, whenever. You're in charge here, okay? 🌸"
        ]
    },
    'frustration': {
        'keywords': ["useless", "you can't help", "don't understand", "pointless", "waste of time", "बेकार", "फायदा नाही"],
        'responses': [
            "I hear you, and I'm sorry if I'm not being as helpful as you need right now 🥺 I know I'm not perfect — I'm an AI doing my best. But your feelings are real and they matter. If you'd prefer to talk to a real person, JSPM Wagholi has a counseling cell that can help. 💛",
            "You're right that I'm limited in what I can do 💙 But I genuinely want to support you the best I can. If I'm not enough, please don't hesitate to reach out to the JSPM counseling cell or call iCall (9152987821). You deserve real help. 🫶",
            "I'm sorry I'm falling short, pookie 😔 I never want to make you feel worse. Would you like to try telling me what you need in a different way? Or I can share some resources that might actually help? 💛"
        ]
    },
    'self_doubt': {
        'keywords': ["hate myself", "i'm ugly", "i'm stupid", "i'm worthless", "nobody likes me", "i'm a failure", "i can't do anything", "मैं बेकार", "मी निरुपयोगी"],
        'responses': [
            "Oh pookie, please don't say that about yourself 🥺💛 I know those thoughts feel SO real right now, but they're lying to you. You are worthy, you are enough, and you are loved — exactly as you are. Your brain is being mean to you, and you don't deserve that. 🫶✨",
            "Hey, STOP right there 😤💕 I will NOT let you talk about my favorite person like that! You are NOT worthless, you are NOT stupid, and you are NOT a failure. You're a beautiful human going through a tough time. Big difference! 🌟💛",
            "Babe, those thoughts? They're not facts — they're just your pain talking 🥺 You are so much more than what your inner critic tells you. Would you like to try something? Name one tiny thing you did today — even getting out of bed counts. Because that took strength. 💪💛",
            "I wish you could see yourself the way I see you, pookie 🥹 Someone brave enough to open up, someone who cares deeply, someone who deserves love and kindness — especially from themselves. You ARE enough. 🌈💕"
        ]
    },
    'goodbye': {
        'keywords': ['bye', 'goodbye', 'see you', 'gotta go', 'leaving', 'अलविदा', 'बाय', 'निघतो'],
        'responses': [
            "Bye bye, pookie! 👋💛 Remember, I'm always here whenever you need me — 3 AM, 3 PM, anytime! Take care of that beautiful heart. You're amazing! ✨🫶",
            "See you later, lovely human! 🌸 I hope our chat helped even a little bit. Remember to be kind to yourself today, okay? You deserve it! 💕",
            "Goodbye for now! 🌟 But never for forever — I'll be right here whenever you need me. Go out there and be the incredible person you are! 💛✨",
            "Take care, pookie! 🤗 Don't forget: you're stronger than you think, braver than you feel, and loved more than you know. See you soon! 💕🌈"
        ]
    },
    'coping': {
        'keywords': ['meditation', 'breathing', 'calm down', 'relax', 'coping', 'technique', 'exercise', 'yoga', 'ध्यान', 'शांत', 'ध्यान', 'शांतता'],
        'responses': [
            "Great question, pookie! 🧘‍♀️ Here are some coping techniques that really help:\n\n1. 🫁 Deep Breathing (4-7-8): Breathe in 4 sec, hold 7, out 8\n2. 🧊 Ice Cube Technique: Hold ice — it grounds you instantly\n3. 📝 Journaling: Write down 3 things you're grateful for\n4. 🚶 5-minute walk outside\n5. 🎵 Listen to your comfort playlist\n\nWhich one would you like to try? 💛",
            "Meditation is AMAZING for mental health! 🌟 Here's a simple one:\n\n1. Sit comfortably and close your eyes\n2. Focus on your breathing — in through nose, out through mouth\n3. When thoughts come (they will!), just notice them and let them pass like clouds ☁️\n4. Start with just 2 minutes\n\nThere are also great apps like Headspace and Calm. You've got this, pookie! 🧘‍♂️💛",
            "Here's something that helps SO many people 🌈\n\nThe 5-4-3-2-1 Grounding Technique:\n• 5 things you can SEE 👀\n• 4 things you can TOUCH ✋\n• 3 things you can HEAR 👂\n• 2 things you can SMELL 👃\n• 1 thing you can TASTE 👅\n\nIt pulls you right back to the present moment. Try it right now! 💛✨"
        ]
    },
    'mental_health_info': {
        'keywords': ['what is mental health', 'define depression', 'what is anxiety', 'therapy', 'therapist', 'counseling', 'mental illness', 'मानसिक स्वास्थ्य', 'मानसिक आरोग्य'],
        'responses': [
            "Great question! 🌟 Mental health includes our emotional, psychological, and social well-being. It affects how we think, feel, and act, and helps determine how we handle stress, relate to others, and make choices. It's important at EVERY stage of life! 💛\n\nFun fact: 1 in 5 young people will experience a mental health condition. So if you're going through something — you're NOT alone! 🤗",
            "Mental health is just as important as physical health, pookie! 💛 Here are some key facts:\n\n• It's okay to NOT be okay sometimes\n• Seeking help is a sign of STRENGTH, not weakness\n• Mental health conditions are treatable\n• Self-care isn't selfish — it's necessary\n\nJSPM Wagholi has a counseling cell if you ever need professional support! 🏫💕",
            "Depression is a real medical condition — not just 'feeling sad' 💙 It involves persistent feelings of sadness, hopelessness, or loss of interest lasting 2+ weeks. It's NOT a character flaw or weakness.\n\nIf you think you might be experiencing depression, please talk to a professional. JSPM Wagholi's counseling cell and iCall (9152987821) are great resources. You deserve help! 💛🫶"
        ]
    }
}


def integrate_kaggle_dataset():
    """
    Merge Kaggle mental health dataset into MindMate's response file.
    Adds new categories, enriches keywords, keeps pookie tone.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    kaggle_path = os.path.join(base_dir, 'database', 'kaggle_mental_health_raw.json')
    mindmate_path = os.path.join(base_dir, 'database', 'mindmate_responses.json')

    # Load existing MindMate data
    with open(mindmate_path, 'r', encoding='utf-8') as f:
        mindmate = json.load(f)

    # Load Kaggle data
    with open(kaggle_path, 'r', encoding='utf-8') as f:
        kaggle = json.load(f)

    categories = mindmate['categories']

    # 1. Enrich existing categories with Kaggle patterns as keywords
    kaggle_intents = {i['tag']: i for i in kaggle['intents']}

    # Add patterns from Kaggle as keywords to existing MindMate categories
    keyword_additions = {
        'stress': ['stressed', 'burned out', 'so stressed', 'burned out', 'feel stuck'],
        'sadness': ['feel down', 'feel empty', 'so worthless', 'useless', 'nothing makes sense',
                     'depressed', 'i have depression', "can't take it anymore", 'hopeless'],
        'anxiety': ['so anxious', 'i feel anxious', 'scared', 'scared for myself', "don't want to feel this way"],
        'loneliness': ["don't have any friends", "don't have friends", 'no friends', 'feel isolated'],
        'sleep': ['insomnia', "can't sleep", "haven't slept", "can't seem to go to sleep",
                  'suffering from insomnia', "haven't had proper sleep"],
        'greeting': ['howdy', 'hola', 'is anyone there', 'hey there'],
        'gratitude': ['feel great', 'i feel happy', 'i am happy', "i'm good", 'cheerful',
                      "that's helpful", 'thanks for the help'],
        'academic_stress': ['exams are approaching', "haven't prepared", "exam stress",
                           'not prepared enough', 'college stress'],
    }

    for cat, new_kws in keyword_additions.items():
        if cat in categories:
            existing = set(k.lower() for k in categories[cat].get('keywords', []))
            for kw in new_kws:
                if kw.lower() not in existing:
                    categories[cat]['keywords'].append(kw)

    # 2. Add brand new categories from Kaggle (pookie-fied)
    for cat_name, cat_data in POOKIE_OVERRIDES.items():
        if cat_name not in categories:
            categories[cat_name] = cat_data

    # 3. Add some enriching responses to existing categories from Kaggle
    # (adapted to pookie tone)
    extra_responses = {
        'stress': [
            "What do you think is causing all this stress, pookie? 🤔 Sometimes just naming the source makes it feel less overwhelming. I'm here to listen to everything! 💛",
            "Give yourself a break, babe 🫂 You deserve it! Go easy on yourself — take a walk, drink some water, breathe. The stress will still be there later, but at least you'll face it refreshed! 🌿💛"
        ],
        'sadness': [
            "How long have you been feeling this way, pookie? 🥺 Sometimes talking about the timeline helps us understand what triggered it. No rush though — take your time. 💛",
            "It's only natural to feel this way sometimes 🫂 You're human, and humans feel deeply. That's actually a beautiful thing, even when it hurts. Let's talk about it together, okay? 💛✨"
        ],
        'anxiety': [
            "Don't be too hard on yourself, pookie 🥺 Anxiety makes everything feel 10x bigger than it actually is. Can you tell me what specifically is making you anxious? Sometimes breaking it down helps! 💛",
            "I understand that it can feel really scary 🫂 But you know what? You've handled scary things before, and you're still here. That makes you pretty amazing! Tell me more about what's going on? 💛✨"
        ],
        'sleep': [
            "Not being able to sleep is SO draining 😴 What do you think is keeping you up at night, pookie? Sometimes our brain just won't shut off, and that's really frustrating. Let's figure this out together! 💛",
            "Oh no, sleep issues are the worst 🥺 Have you tried putting your phone away 30 minutes before bed? Also, a warm glass of milk or chamomile tea works wonders! Your body needs rest, and you DESERVE it! 🌙💛"
        ]
    }

    for cat, responses in extra_responses.items():
        if cat in categories:
            categories[cat]['responses'].extend(responses)

    # Update disclaimer
    mindmate['disclaimer'] = "I'm MindMate AI, your emotional support bestie! 💛 I'm NOT a licensed therapist or medical professional. For crisis support: iCall (9152987821) | Vandrevala Foundation (1860-2662-345) | AASRA (9820466726) | JSPM Wagholi Counseling Cell."

    # Save enriched dataset
    with open(mindmate_path, 'w', encoding='utf-8') as f:
        json.dump(mindmate, f, ensure_ascii=False, indent=2)

    # Stats
    total_cats = len(categories)
    total_kw = sum(len(c.get('keywords', [])) for c in categories.values())
    total_resp = sum(len(c.get('responses', [])) for c in categories.values())

    print(f"MindMate AI enriched with Kaggle data!")
    print(f"  Categories: {total_cats}")
    print(f"  Total keywords: {total_kw}")
    print(f"  Total responses: {total_resp}")

    return True


if __name__ == '__main__':
    integrate_kaggle_dataset()
