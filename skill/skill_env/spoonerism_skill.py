from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui.ssml_output_speech import SsmlOutputSpeech
from spoonerisms import ssmlify, spoonerify

# from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler
# sb = WebserviceSkillHandler()
from ask_sdk_core.skill_builder import SkillBuilder
sb = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type('LaunchRequest')(handler_input)
    
    def handle(self, handler_input):
        speech_text = 'What words would you like to spoonerize?'

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard('Spoonerism Maker', speech_text)
        ).set_should_end_session(False)
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input)
                or is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Spoonerism Maker", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can tell me words that I should spoonerify."

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Spoonerism Maker", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class ValueIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ValueIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        sentence = slots['Value'].value
        ssml = ssmlify(sentence)
        plain_text = spoonerify(sentence)

        return Response(SsmlOutputSpeech(ssml=ssml), SimpleCard("Spoonerism Maker", plain_text), should_end_session=True)

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, something went wrong, please try again."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ValueIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(AllExceptionHandler())
handler = sb.lambda_handler()