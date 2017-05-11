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
    errors = cdf2cim.publish()
    if errors:
        for fpath, err in errors:
            fname = fpath.split("/")[-1]
            cdf2cim.logger.log_warning("Publication error: {} :: {}".format(fname, err))
    else:
        cdf2cim.logger.log("Publication succeeded")


# Main entry point.
if __name__ == '__main__':
    _main()

