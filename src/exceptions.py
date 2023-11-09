import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SkillConfigurationException(Exception):
    """Raised when there's a configuration error with the skill."""
    pass

class ValidationException(Exception):
    """Raised when a request to the skill fails validation."""
    pass

class ExternalAPIException(Exception):
    """Raised when an external API call fails."""
    pass