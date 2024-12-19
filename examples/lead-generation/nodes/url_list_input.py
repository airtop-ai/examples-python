from state import State
from utils import validate_url


def get_url_list_input() -> list[str]:
    """Langgraph node that gets a list of URLs from user input.

    Prompts the user to enter URLs one at a time until they type 'done'.
    Each URL is validated before being added to the list.

    Returns:
        list[str]: A list of valid URLs entered by the user.
    """
    urls = []
    while True:
        url = input("Enter a URL (or type 'done' to finish): ")
        if url.lower() == "done":
            break

        is_valid, error_message = validate_url(url)
        if not is_valid:
            print(error_message)
            continue

        urls.append(url)

    return urls


def url_list_input_node(state: State):
    urls = get_url_list_input()
    return State(urls=urls)
