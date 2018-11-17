# Holds data for card request
class CardRequest:
  ref = ''
  amount = ''
  cardNbr = ''
  cardExpMth = ''
  cardExpYear = ''
  zipCode = ''

  # parses a comma seperated string into each field
  def parse(self, line):
    tokens = str(line).strip().split(',')

    self.ref = str(tokens[0]).strip()
    self.amount = str(tokens[1]).strip()
    self.cardNbr = str(tokens[2]).strip()
    self.cardExpMth = str(tokens[3]).strip()
    self.cardExpYear = str(tokens[4]).strip()
    self.zipCode = str(tokens[5]).strip()