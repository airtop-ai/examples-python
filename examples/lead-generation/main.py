from nodes.url_list_input.url_list_input_node import get_url_list_input
from env_config import env_config
from nodes.url_validator.url_validator_node import validate_url


urls = get_url_list_input()

print(urls)
print(env_config.AIRTOP_API_KEY)

result = validate_url(urls[0])
print("OUTPUT FROM VALIDATION", result)

