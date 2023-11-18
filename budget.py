from itertools import zip_longest


class Category:

  def __init__(self, category):
    self.ledger = []
    self.category = category

  def __str__(self):
    size_of_category = len(self.category)
    total_asterisks = 30 - size_of_category
    total_asterisks_divided_by_two = int(total_asterisks / 2)

    category_str = "*" * total_asterisks_divided_by_two + self.category + "*" * total_asterisks_divided_by_two + "\n"
    total = 0

    for item in self.ledger:
      total += item["amount"]
      space = 30 - len(item["description"]) - 1 if len(
          item["description"]) < 23 else 0

      category_str += "{} {:>{space}.2f}\n".format(item["description"][:23],
                                                   float(item["amount"]),
                                                   space=space)

    category_str += "Total: {:.2f}".format(total)

    return category_str

  def deposit(self, amount, description=''):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=''):
    if self.check_funds(amount) is False:
      return False

    self.ledger.append({"amount": -amount, "description": description})

    return True

  def get_balance(self):
    balance = 0
    for item in self.ledger:
      balance += item["amount"]

    return balance

  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {category.category}")
      category.deposit(amount, f"Transfer from {self.category}")

      return True

    return False

  def check_funds(self, amount):
    if amount > self.get_balance():
      return False

    return True


def create_spend_chart(categories):
  output_str = "Percentage spent by category"
  output_str += "\n"
  categories_calcs = {}

  for category in categories:
    for ledger in category.ledger:
      if category.category not in categories_calcs:
        categories_calcs[
            category.
            category] = ledger["amount"] if ledger["amount"] < 0 else 0
      else:
        categories_calcs[
            category.
            category] += ledger["amount"] if ledger["amount"] < 0 else 0

  total = 0

  for key, value in categories_calcs.items():
    total += value

  percentage_dict = {}

  for key, value in categories_calcs.items():
    percentage_dict[key] = (value / total) * 100

  start = 100

  ordered_categories_by_length = sorted(percentage_dict.keys(), key=len)
  biggest_category_length = ordered_categories_by_length[-1]

  for percent in range(12, 1, -1):
    if start == 100:
      output_str += "{:<1}|".format(str(start))
    elif start == 0:
      output_str += "{:>3}|".format(str(start))
    else:
      output_str += "{:>3}|".format(str(start))

    items_list = list(percentage_dict.values())

    for value in items_list:
      if (start - int(value)) <= 0:
        output_str += "{:^3}".format("o")
      else:
        output_str += "{:^3}".format("")

    output_str += " \n"
    start -= 10

  output_str += "{:>14}\n".format("----------")

  formatted_categories = ''

  for i in range(len(biggest_category_length)):
    for idx, word in enumerate(list(percentage_dict.keys())):
      if idx == 0:
        formatted_categories += "     {}".format(
            word[i] if i < len(word) else ' ')
      elif i == len(biggest_category_length)-1:
        formatted_categories += "{:^4}".format(
            word[i] if i < len(word) else ' ')
      else:
        formatted_categories += "  {}".format(
            word[i] if i < len(word) else ' ')

    if i < len(biggest_category_length)-1:
      formatted_categories += "  \n"

  output_str += formatted_categories

  return output_str
