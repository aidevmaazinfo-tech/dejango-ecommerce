from intents.models import Intent
from thefuzz import fuzz, process

FAQ_ALIASES = {
    # Greetings & Small Talk
    "FAQ_GREETING": ("hi", "hello", "hey", "assalam-o-alikum", "salam", "good morning", "good evening", "hey there"),
    "FAQ_THANKS": ("thank", "thanks", "thank you", "shukriya", "jazakallah", "bohat shukriya"),
    "FAQ_BYE": ("bye", "goodbye", "allah hafiz", "see you", "take care"),
    
    # Store Policies & Operations
    "FAQ_SHIPPING": ("shipping", "delivery time", "delivery times", "how long", "shipping kitni der", "delivery kitni der"),
    "FAQ_RETURNS": ("return", "returns", "send back", "wapas karna"),
    "FAQ_REFUNDS": ("refund", "money back", "paise wapas", "pese wapas"),
    "FAQ_PAYMENT": ("payment", "pay", "card", "cash on delivery", "cod", "paisa kaise dein"),
    "FAQ_CANCELLATION": ("cancel order", "cancellation", "cancel karna", "order cancel"),
    "FAQ_TRACKING": ("track order", "order tracking", "where is my order", "order kahan hai"),
    "FAQ_ACCOUNT": ("account", "profile", "address", "mera address", "password"),
    
    # Company & Contact Info
    "FAQ_COMPANY": ("who are you", "about company", "company info", "what is this store", "aap kon hain", "about us", "store ke baray mein"),
    "FAQ_CONTACT": ("contact", "support", "help line", "phone number", "email", "whatsapp", "rabta kaise karein"),
    "FAQ_HOURS": ("timing", "working hours", "open time", "store timing", "kab khulta hai"),
    "FAQ_LOCATION": ("location", "address store", "where is your shop", "outlet", "shop kahan hai"),
}

DEFAULT_FAQ = {
    # Greetings & Small Talk Responses
    "FAQ_GREETING": "Hello! Welcome to our store. How can I help you with your shopping today?",
    "FAQ_THANKS": "You're very welcome! Let me know if you need help with anything else.",
    "FAQ_BYE": "Goodbye! Have a great day, and feel free to reach out whenever you need assistance.",
    
    # Store Policies Responses
    "FAQ_SHIPPING": "Standard delivery usually takes 5 to 7 business days across the country.",
    "FAQ_RETURNS": "Returns are handled through customer support within 7 days of receiving your order.",
    "FAQ_REFUNDS": "Refunds are processed to your bank account or wallet within 3-5 days after a return is inspected.",
    "FAQ_PAYMENT": "We accept Cash on Delivery (COD) as well as secure online card payments.",
    "FAQ_CANCELLATION": "You can cancel your order directly from your profile or by contacting support before it ships.",
    "FAQ_TRACKING": "You can track your order using your unique order ID in the tracking section.",
    "FAQ_ACCOUNT": "You can manage your account profile, saved addresses, and preferences from your dashboard.",
    
    # Company & Contact Responses
    "FAQ_COMPANY": "We are a trusted e-commerce store dedicated to bringing you the best quality products at affordable prices.",
    "FAQ_CONTACT": "You can reach our support team via email at support@store.com or through our helpline.",
    "FAQ_HOURS": "Our customer support and online store are operational 24/7 to assist you.",
    "FAQ_LOCATION": "We operate primarily as an online store with nationwide shipping facilities.",
}

def faq_tool(message):
    text = (message or "").lower().strip()
    
    # 1. Check strict alias matching first
    for intent_name, aliases in FAQ_ALIASES.items():
        if any(alias in text for alias in aliases):
            database_intent = Intent.objects.filter(intent_name=intent_name, is_active=True).first()
            answer = database_intent.response if database_intent else DEFAULT_FAQ.get(intent_name)
            return {
                "success": True, 
                "tool": "faq_tool", 
                "intent": intent_name, 
                "message": answer, 
                "data": {"faq": answer}
            }

    # 2. Fallback: Search all active database intents using fuzzy matching against questions/responses
    all_intents = list(Intent.objects.filter(is_active=True))
    if all_intents:
        intent_texts = [i.intent_name.lower() for i in all_intents]
        best_match, score = process.extractOne(text, intent_texts, scorer=fuzz.partial_ratio)
        if score >= 75:
            matched_intent = next((i for i in all_intents if i.intent_name.lower() == best_match), None)
            if matched_intent and matched_intent.response:
                return {
                    "success": True,
                    "tool": "faq_tool",
                    "intent": matched_intent.intent_name,
                    "message": matched_intent.response,
                    "data": {"faq": matched_intent.response}
                }

    # 3. Ultimate Fallback for general unmapped questions
    general_fallback = "I'm not entirely sure about that specific question. You can ask me about products, shipping, returns, order tracking, or store details!"
    return {
        "success": True,
        "tool": "faq_tool",
        "intent": "FAQ_GENERAL",
        "message": general_fallback,
        "data": {"faq": general_fallback}
    }