"""
.. module:: publish.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: cdf2cim publication entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import cdf2cim



def _main():
    """Publishes cdf2cim files to web-service.

    """
    successes, failures = cdf2cim.publish()
    for fpath, err in failures:
        cdf2cim.logger.log_warning("Publication error: {} :: {}".format(fpath, err))
    for fpath in successes:
        cdf2cim.logger.log("Published file: {}".format(fpath))


# Main entry point.
if __name__ == '__main__':
    _main()
