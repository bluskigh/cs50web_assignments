from json import dumps

from django.test import TestCase, Client, TransactionTestCase
from django.db import transaction

from .models import Post, User 

"""
django.test.Client is used to make requests, no default arguments are 
needed. Though you can provide optional defualt headers. 

get(path, data=None, follow=None, secure=None, **extra)
- returns a Response object
- extra keyword arguments parameter can be used to specify headers
to be sent in the request.
- follow if set to True the client will follow any redirects, thus 
a redirect_chain attribute will be set in the response object containing
tuples and the intermediate urls and status codes. 
ex [('http://google.com/next/', 302), ('http://google.com/final/', 302)]
to be clear the above is only the urls of the redirection urls, so the 
original url is not included
- secure set to True then https is emulated

post(path, data=None, content_type=MULTIIPART_CONTENT, ...)
- arguments exact as get except for content_type
- if you want the data to be serialized

What does it mean to serialize (serialization)?
- process of translating a data structure or object state into a format
that can be stored or transmitted and reconstructed later. 

in the pickle module
dumps() serializes a python object by converting it into a byte stream.
A byte is 8 bits. An ASCII letter is letter is 7 bits (but stored in a byte which is 8 bits). 
Therefore is converts a dict object into a stream of ascii letters.
loads() does the inverse, by converting the byte back into an object.

the json module
dumps() serlalizes python pbject into human-readable unicode text
loads() does the oppposite


But what is ASCII and Unicode?

ASCII
- uses 7 bits to represent a character, therefore 2 ^ 7 = 128
- it uses 8 bits but the last bit is used for avoiding errors as parity 
bit
- ascii was meant for english only
What is parity bit (check bit)?
- bit added to a string of binary code
- way of trying to establish if binary data has changed during 
tranmission 
- usually added applied to smallest unit of communication protocol(bytes)
- ensures that the total number of 1-bits in string is even or odd
    Two variants (even parity bit, odd parity bit)
        - even parity bit: given a set of bits, the occurrences of 1s are
        counted. if count is odd, bit value is set to 1 (even including 
        the parity bit). if count of 1s in a given set of bits is 
        already even parity bit's value is 0
        - odd parity: coding is reversed, if count of 1s is even parity
        bit vlaue is set to 1, making the whole set an odd number. if 
        count of bits with a value of 1 is odd, the count is already odd
        so the parity bit's value is 0.
    so, even parity is to make the 1s even, if odd then 1 else 0
    so, odd parity is to make the 1s odd, if odd then 0 else 1
- parity check has many issues with it though.
- The way it used is by two commicators agree upon a certain parity 
form, even or odd. If a sender tells the reciever that the message is
goignt o contain even parity and the reciever recieves odd parity he
knows the message has been messed with, vice versa.
https://en.wikipedia.org/wiki/Parity_bit
What is parity in mathematics?
- property of an integer of whether is is even or odd.
What else does parity mean?
- the quality or state of being equal or equivalent

ASCCI extended (8-bit ascii)
- uses all 8 bits including the bit used for parity in normal ASCII
- reuslting in 2 ^ 8 = 256
- now can represent accents such as french letters

UNICODE
- used to represent all the languages, 
- cannot save text as "Unicode" 
- you need to encode text to convert into unicode
- uses hexadecimal to reference numbers
    since a single character of hexadecimal represents value between 0-15
    a binary 4 bit number holds a value value between 0-15
    example: 1101 0011 = 211 in hexadecimal = D3 because 1101 = 13 in 
    decimal = D in hexadecimal 0011 = 3 = 3 in hexadecimal. Converting 
    D3 to decimal number using simple formula (13x16^1) + (3x16^0) = 211
    11010011 = binary version 
What is character encoding?
    - each character is assoicated with a number (code point)
    - way to convert text data into binary number

What does repertoire mean?
- a list or supply of capabilities



"""


"""
Extending from TestCase causes each test to be enclosed or capsulated by 
a transaction. After a certain test is run the transaction is rolled back.
Meaning, the updates doen to the database are reverted. So to keep the 
database clean. TransactionTestCase does do not roll back after each 
individual test.
"""
class TestApp(TransactionTestCase):
    pid = 0
    def setUp(self):
        self.client = Client()
        self.index = 0
        user = User.objects.create(username="mario_test")
        user.set_password("m")
        user.save()
        self.client.force_login(user)
