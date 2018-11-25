# Holds data for card request
class CardRequest:
  guid = ''
  ref = ''
  amount = ''
  cardNbr = ''
  cardExpMth = ''
  cardExpYear = ''
  zipCode = ''
  firstName = ''
  lastName = ''
  email = ''

  # parses a comma seperated string into each field
  def parse(self, line):
    tokens = str(line).strip().split(',')

    self.ref = str(tokens[0]).strip()
    self.amount = str(tokens[1]).strip()
    self.cardNbr = str(tokens[2]).strip()
    self.cardExpMth = str(tokens[3]).strip()
    self.cardExpYear = str(tokens[4]).strip()
    self.firstName = str(tokens[5]).strip()
    self.lastName = str(tokens[6]).strip()
    self.email = str(tokens[7]).strip()
    self.zipCode = str(tokens[8]).strip()