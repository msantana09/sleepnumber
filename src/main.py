import logging
import os
from ask_sdk_core.skill_builder import SkillBuilder
from common.config import config
from services import (CatchAllExceptionHandler, IncreaseFirmness,SetFirmness, LaunchRequestHandler, RequestLogger, ResponseLogger, SessionEndedRequestHandler,
                      SkillConfigurationExceptionHandler, ValidationExceptionHandler, ExternalAPIExceptionHandler)
from common.aws.secretsmanager import get_secret

log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)


sb = SkillBuilder()
sb.skill_id = config.skill_id

# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SetFirmness())
sb.add_request_handler(IncreaseFirmness())
sb.add_request_handler(SessionEndedRequestHandler())    

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_exception_handler(SkillConfigurationExceptionHandler())
sb.add_exception_handler(ValidationExceptionHandler())
sb.add_exception_handler(ExternalAPIExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
handler = sb.lambda_handler()
