import logging
import ssl

import pika

_log = logging.getLogger(__name__)


# This is a copy of ``fedora_messaging.twisted.service._configure_tls_parameters`` with some
# adjustments to use the provided configuration dict and not the fedora_messaging general
# configuration.
def configure_tls_parameters(parameters, tls_config):  # pragma: no cover
    """
    Configure the pika connection parameters for TLS based on the configuration.

    This modifies the object provided to it. This accounts for whether or not
    the new API based on the standard library's SSLContext is available for
    pika.

    Args:
        parameters (pika.ConnectionParameters): The connection parameters to apply
            TLS connection settings to.
        tls_config (dict): The TLS configuration.
    """
    cert = tls_config["certfile"]
    key = tls_config["keyfile"]
    if cert and key:
        _log.info(
            "Authenticating with server using x509 (certfile: %s, keyfile: %s)",
            cert,
            key,
        )
        parameters.credentials = pika.credentials.ExternalCredentials()
    else:
        cert, key = None, None

    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    if tls_config["ca_cert"]:
        try:
            ssl_context.load_verify_locations(cafile=tls_config["ca_cert"])
        except ssl.SSLError as e:
            raise ValueError(f'The "ca_cert" setting in the "tls" section is invalid ({e})')
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.check_hostname = True
    if cert and key:
        try:
            ssl_context.load_cert_chain(cert, key)
        except ssl.SSLError as e:
            raise ValueError(f'The "keyfile" setting in the "tls" section is invalid ({e})')
    parameters.ssl_options = pika.SSLOptions(ssl_context, server_hostname=parameters.host)
