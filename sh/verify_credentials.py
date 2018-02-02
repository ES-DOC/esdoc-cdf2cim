"""
.. module:: verify_credentials.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Verifies credentials with cdf2cim web-service.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from cdf2cim import logger
from cdf2cim import verify_credentials
from cdf2cim.exceptions import ClientError
from cdf2cim.exceptions import WebServiceAuthenticationError
from cdf2cim.exceptions import WebServiceAuthorizationError
from cdf2cim.exceptions import WebServiceConnectionError
from cdf2cim.exceptions import WebServiceProcessingError



def _main():
    """Verifies credentials with cdf2cim web-service.

    """
    try:
        verify_credentials()
    except (
        ClientError,
        WebServiceConnectionError,
        WebServiceAuthenticationError,
        WebServiceAuthorizationError,
        WebServiceProcessingError
        ) as err:
        logger.log_error(err)
    except Exception as err:
        logger.log_error(err)


# Main entry point.
if __name__ == '__main__':
    _main()
