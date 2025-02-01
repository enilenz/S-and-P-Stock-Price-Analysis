import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
    file_name,exc_tb.tb_lineno,str(error))

    return error_message


class CustomException(Exception):
    """
    Custom Exception raised for logging purposes.
    Saves file name, line number of the error and the error message
    """
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message


class TickerNotFoundError(Exception):
    """
    Exception raised for errors in the input ticker field.

    Attributes:
        ticker -- input ticker which caused the error
        message -- explanation of the error
    """

    def __init__(self, ticker):
        self.ticker = ticker
        self.error_message = "The index data for " + self.ticker + " was not found"
        
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message
    

class InsufficientData1990():

    def __init__(self):
        pass
    pass


