# -*- coding: utf-8 -*-

"""
.. module:: exceptions.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package exceptions.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
class ClientError(Exception):
    """Raised if a client error occurs when calling the web-service.

    """
    def __init__(self, err):
        """Instance constructor.

        """
        super(ClientError, self).__init__("UNKNOWN FAILURE :: {}".format(err))


class InvalidFileSearchCriteria(Exception):
    """Raised if NetCDF4 file search criteria are deemed invalid.

    """
    def __init__(self, criteria):
        """Instance constructor.

        """
        super(InvalidFileSearchCriteria, self).__init__(
            "NETCDF FILE SEARCH CRITERIA ARE INVALID :: {}".format(criteria)
            )


class WebServiceConnectionError(Exception):
    """Raised if web-service connection fails.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(WebServiceConnectionError, self).__init__("WEB-SERVICE CONNECTION FAILURE")



class WebServiceAuthenticationError(Exception):
    """Raised if web-service authentication fails.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(WebServiceAuthenticationError, self).__init__("WEB-SERVICE AUTHENTICATION FAILURE")


class WebServiceAuthorizationError(Exception):
    """Raised if web-service authorization fails.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(WebServiceAuthorizationError, self).__init__("WEB-SERVICE AUTHORIZATION FAILURE")


class WebServiceProcessingError(Exception):
    """Raised if web-service processing fails.

    """
    def __init__(self, http_status_code, err):
        """Instance constructor.

        """
        super(WebServiceProcessingError, self).__init__("WEB-SERVICE ERROR: {} :: {}".format(http_status_code, err))
