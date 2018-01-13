# ExceptionErrors.py
#
# User defined exceptions

# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

# Simulator errors

class RedundantCall(Error):
    """debugging aid to track calls """
    pass

class ImageTk_Missing(Error):
    """debugging aid to track calls """
    pass

class SimulatorWindowClosed(Error):
    """used when the simulator window is closed """
    pass

class SimulatorNotRunning(Error):
    """A call was made which requires the simulator ro be running"""
    pass
