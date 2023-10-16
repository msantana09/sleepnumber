import logging
from ask_sdk_core.skill_builder import SkillBuilder
from services import (CatchAllExceptionHandler, IncreaseFirmness,SetFirmness, LaunchRequestHandler, RequestLogger, ResponseLogger, SessionEndedRequestHandler)
from common.aws.secretsmanager import get_secret

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


secrets = get_secret("sleepnumber", "us-east-1")
sb = SkillBuilder()
sb.skill_id = secrets["skill_id"]

# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SetFirmness(secrets))
sb.add_request_handler(IncreaseFirmness(secrets))
sb.add_request_handler(SessionEndedRequestHandler())    

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
handler = sb.lambda_handler()
