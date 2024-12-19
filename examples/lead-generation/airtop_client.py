from airtop import Airtop, SessionConfigV1, SessionResponse, WindowResponse
from env_config import env_config

default_session_config: SessionConfigV1 = SessionConfigV1(
    persist_profile=False,
    timeout_minutes=10
)

class AirtopClient:
    sessions = []
    windows = []

    def __init__(self, api_key: str):
        """Initializes the AirtopClient.

        Args:
            api_key (str): The API key for authenticating with Airtop service.
        """
        self.client = Airtop(api_key=api_key)
    
    def create_session(self, config: SessionConfigV1 = default_session_config) -> SessionResponse:
        """Creates a new Airtop session.

        Creates and stores a new session using the provided configuration.
        The session is automatically added to the internal sessions list.

        Args:
            config (SessionConfigV1, optional): Configuration for the session. 
                Defaults to default_session_config.

        Returns:
            SessionResponse: The created session response object.
        """
        session = self.client.sessions.create(configuration=config)
        self.sessions.append(session)
        return session
    
    def create_window(self, session_id: str, url: str) -> WindowResponse:
        """Creates a new window in an existing session.

        Creates and stores a new window in the specified session.
        The window is automatically added to the internal windows list.

        Args:
            session_id (str): The ID of the session to create the window in.
            url (str): The URL to navigate to in the new window.

        Returns:
            WindowResponse: The created window response object.
        """
        window = self.client.windows.create(session_id=session_id, url=url)
        self.windows.append(window)
        return window

airtop_client = AirtopClient(str(env_config.AIRTOP_API_KEY))

