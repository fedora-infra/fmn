"""This module is responsible for loading the application configuration."""
import fedmsg


#: The application configuration dictionary.
app_conf = fedmsg.config.load_config()
