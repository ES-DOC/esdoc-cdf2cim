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
    for fpath, err in cdf2cim.publish():
    	fname = fpath.split("/")[-1]
        cdf2cim.logger.log_warning("Publication error: {} :: {}".format(fname, err))


# Main entry point.
if __name__ == '__main__':
    _main()

