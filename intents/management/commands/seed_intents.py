from django.core.management.base import BaseCommand

from intents.models import Intent



DEFAULT_INTENTS = [

    {
        "intent_name": "greeting",

        "trigger_phrase":
            "hello,hi,hey,"
            "good morning,"
            "good afternoon,"
            "good evening,"
            "greetings",

        "response":
            "Hello! How can I help you today?"
    },


    {
        "intent_name": "farewell",

        "trigger_phrase":
            "bye,goodbye,"
            "see you,take care,"
            "good night",

        "response":
            "Goodbye! Have a great day."
    },


    {
        "intent_name": "thanks",

        "trigger_phrase":
            "thanks,thank you,"
            "thx,appreciate it",

        "response":
            "You're welcome!"
    },


    {
        "intent_name": "identity",

        "trigger_phrase":
            "who are you,"
            "what are you,"
            "what can you do",

        "response":
            "I am a document search assistant that helps you find information from uploaded documents."
    },


    {
        "intent_name": "help",

        "trigger_phrase":
            "help,"
            "what can i ask,"
            "commands,"
            "options",

        "response":
            "You can ask questions about uploaded documents and I will find relevant information."
    },

]


class Command(BaseCommand):

    help = "Create default chatbot intents"


    def handle(self, *args, **kwargs):

        for item in DEFAULT_INTENTS:

            Intent.objects.get_or_create(
                intent_name=item["intent_name"],
                defaults=item
            )


        self.stdout.write(
            self.style.SUCCESS(
                "Default intents created"
            )
        )