import random
import test


def main(rank0, password, quote, release, lucky_number, username):
    quote_create = addQoute(quote, release)
    str_quote = quote_create + password
    list_symbols, str_symbols = add_symbols(str_quote)
    list_lucky, str_lucky = add_lucky(str_symbols, lucky_number)
    rank1 = test.main_generate(str_quote, username)
    rank2 = test.main_generate(str_symbols, username)
    rank3 = test.main_generate(str_lucky, username)
    ranks = [rank0, rank1, rank2, rank3]
    return ranks, password, quote_create, str_quote, list_symbols, str_symbols, list_lucky, str_lucky


def add_lucky(str_symbols, lucky_number):
    index = random.randint(0, len(str_symbols) - 1)
    res_list = [str_symbols[0:index], str(lucky_number), str_symbols[index:]]
    res_str = ''.join(res_list)
    return res_list, res_str


def addQoute(quote, release):
    words = quote.split()
    initials = [word[0] for word in words]
    random_initials = [random.choice([letter.upper(), letter.lower()]) for letter in initials]
    quote_string = ''.join(random_initials)
    result_string = release[2] + quote_string + release[3]

    return result_string


def add_symbols(curr):
    myList = ["!", "@", "#", "$", "%", "&", "*", "?", "+"]
    indices = random.sample(range(len(curr)), 2)
    indices.sort()
    index1, index2 = indices
    indices = random.sample(range(len(myList)), 2)
    sym1, sym2 = indices
    res_list = [curr[0:index1], myList[sym1], curr[index1:index2], myList[sym2], curr[index2:]]
    res_str = ''.join(res_list)
    return res_list, res_str

# def main(password, lucky_number, quote, release):
