"""
.. module:: verify_credentials.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Verifies credentials with cdf2cim web-service.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from cdf2cim import logger
from cdf2cim import verify_credentials



def _main():
    """Verifies credentials with cdf2cim web-service.

    """
    try:
        verify_credentials()
    except Exception as err:
        logger.log_error(err)


# Main entry point.
if __name__ == '__main__':
    _main()
