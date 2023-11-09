import logging
from time import sleep
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler,
    AbstractExceptionHandler,
    AbstractRequestInterceptor,
    AbstractResponseInterceptor,
)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.response import Response
from sleepyq import Sleepyq
from exceptions import ( SkillConfigurationException, ValidationException, ExternalAPIException)
import prompts
from common.config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CustomAbstractRequestHandler(AbstractRequestHandler):
    def __init__(self) -> None:
        super().__init__()
        self.sleepiq_client = Sleepyq(config.username, config.password)
        self.sleepiq_client.login()


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = prompts.LAUNCH_MESSAGE

        return (
            handler_input.response_builder.speak(speak_output)
            .ask(speak_output)
            .response
        )


class SetFirmness(CustomAbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SetFirmness")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        bed = self.sleepiq_client.beds_with_sleeper_status()[0]

        slots = handler_input.request_envelope.request.intent.slots
        if "firmness" in slots:
            firmness = int(slots["firmness"].value)
            left_firmness = bed.left.data["sleepNumber"]
            right_firmness = bed.right.data["sleepNumber"]

            if left_firmness != firmness:
                self.sleepiq_client.set_sleepnumber("L", firmness, bedId=bed.bedId)
            if right_firmness != firmness:
                self.sleepiq_client.set_sleepnumber("R", firmness, bedId=bed.bedId)

        response = f"Sleepnumber is being  updated to {firmness}"
        return handler_input.response_builder.speak(response).response


class IncreaseFirmness(CustomAbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("IncreaseFirmness")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In IncreaseFirmness")
        bed = self.sleepiq_client.beds_with_sleeper_status()[0]

        left_firmness = bed.left.data["sleepNumber"]
        right_firmness = bed.right.data["sleepNumber"]

        if left_firmness <= 90:
            left_firmness += 10
        else:
            left_firmness = 100

        if right_firmness <= 90:
            right_firmness += 10
        else:
            right_firmness = 100

        self.sleepiq_client.set_sleepnumber("L", left_firmness, bedId=bed.bedId)
        sleep(15)
        self.sleepiq_client.set_sleepnumber("R", right_firmness, bedId=bed.bedId)
        sleep(15)

        response = f"Sleepnumber firmness has been increased to {left_firmness} on the left and {right_firmness} on the right"
        return handler_input.response_builder.speak(response).response



class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response    
    

# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))



class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(prompts.ERROR_MESSAGE)

        return handler_input.response_builder.response
    

class SkillConfigurationExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return isinstance(exception, SkillConfigurationException)

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speech = "There was a configuration error with the skill. Please check the skill settings."
        handler_input.response_builder.speak(speech).set_should_end_session(True)
        return handler_input.response_builder.response

class ValidationExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return isinstance(exception, ValidationException)

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speech = "Sorry, I didn't understand that. Please try again."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

class ExternalAPIExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return isinstance(exception, ExternalAPIException)

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speech = "Sorry, I can't access the external service right now. Please try again later."
        handler_input.response_builder.speak(speech).set_should_end_session(True)
        return handler_input.response_builder.response
 