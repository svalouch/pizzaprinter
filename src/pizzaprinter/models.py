
import datetime
from pydantic import BaseModel


class Receipt(BaseModel):
    '''
    Model for the receipt data we're expecting.
    '''
    #: The user name of the person who ordered the pizza
    user: str
    #: Name of the pizza
    pizza: str
    #: Date and time when the order was placed
    date: datetime.datetime
    #: Size of the pizza
    size: str
    #: Amount of cache to be paid
    total: float
