from dg.CardRequest import CardRequest

import datetime

# thrown when the minimum number of tokens is missing
class MissingTokensException(Exception):
  pass

# class used to parse card request in CSV format
# throws validation errors if fields have errors
class LineParser:
  
  # parses a comma seperated string into each field
  # expected line format is
  # <merc ref>,<amount>,<card>,<expiry month>,<expiry year>,<first name>,<last name>,<email>,<postal code>
  def parse(self, line):
    req = CardRequest()
    tokens = str(line).strip().split(',')

    if len(tokens) < 9:
      raise MissingTokensException('Minimum number of tokens missing')

    # ------------ ref
    token = str(tokens[0]).strip()
    self.validateEmpty(token, 'ref')

    req.ref = token

    # ------------ amount
    token = str(tokens[1]).strip()

    if len(token) == 0:
      raise ValueError('Missing [amount] field')
    elif token.isnumeric() == False:
      raise ValueError('[amount] field is not numeric')

    req.amount = token

    # ------------ cardNbr
    token = str(tokens[2]).strip()

    if len(token) == 0:
      raise ValueError('Missing [cardNbr] field')
    elif token.isnumeric() == False:
      raise ValueError('[cardNbr] field is not numeric')
    else:
      if self.validateLuhn(token) == False:
        raise ValueError('[cardNbr] field is invalid')

    req.cardNbr = token

    # ------------ cardExpMth
    token = str(tokens[3]).strip()

    if len(token) == 0:
      raise ValueError('Missing [cardExpMth] field')
    elif token.isnumeric() == False:
      raise ValueError('[cardExpMth] field is not numeric')
    else:
      cardExpMth = int(token)
      if cardExpMth == 0 or cardExpMth > 12:
        raise ValueError('[cardExpMth] field is invalid')

    req.cardExpMth = token

    # ------------ cardExpYear
    token = str(tokens[4]).strip()

    if len(token) == 0:
      raise ValueError('Missing [cardExpYear] field')
    elif token.isnumeric() == False:
      raise ValueError('[cardExpYear] field is not numeric')
    else:
      cardExpYear = int(token)
      currentYear = datetime.datetime.now().year

      if (cardExpYear < currentYear - 10) or (cardExpYear > currentYear + 10):
        raise ValueError('[cardExpYear] field is invalid')
    
    req.cardExpYear = token

    # ------------ firstName
    token = str(tokens[5]).strip()
    self.validateEmpty(token, 'firstName')

    req.firstName = token

    # ------------ lastName
    token = str(tokens[6]).strip()
    self.validateEmpty(token, 'lastName')

    req.lastName = token

    # ------------ email
    token = str(tokens[7]).strip()
    self.validateEmpty(token, 'email')

    req.email = token

    # ------------ zipCode
    token = str(tokens[8]).strip()
    self.validateEmpty(token, 'zipCode')

    req.zipCode = token

    return req

  # Validates that a token is an empty string
  # throws ValueError if it is empty
  def validateEmpty(self, token, name):
    if len(token) == 0:
      raise ValueError('Missing [' + name + '] field')

  # Validates that a card passes the Luhn check
  # see https://en.wikipedia.org/wiki/Luhn_algorithm
  def validateLuhn(self, token):
    LUHN_ODD_LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)  # sum_of_digits (index * 2)

    evens = sum(int(p) for p in token[-1::-2])
    odds = sum(LUHN_ODD_LOOKUP[int(p)] for p in token[-2::-2])
    return ((evens + odds) % 10 == 0)