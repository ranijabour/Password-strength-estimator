import os
import math
import time
import uuid
import ESrank
import BS
import rank_config


def keyBoard(word):
    for w in word:
        if not (w.isdigit() or w.isalpha() or isSymbol(w)):
            return False
    return True


def isSymbol(c):
    return (c in r"!~@#$%^&*()_+?><.,;:'{}[]=-|\/ ") or (c == '"')


def isShifted(c):
    if c.isalpha():
        return c.isupper()
    return False


def unShiftLetter(c):
    if c.isalpha():
        return c.lower()


def unShiftWord(word):
    p = ""
    lst = []
    for i in range(len(word)):
        if isShifted(word[i]):
            p = p + unShiftLetter(word[i])
            if i > len(word) // 2:
                lst.append(i - len(word))
            else:
                lst.append(i)
        else:
            p = p + word[i]
    return p, str(tuple(lst))


def isascii(value):
    return all(ord(c) < 128 for c in value)


def unLeetWord(word):
    lst = []
    if "0" in word:
        word = word.replace("0", "o")
        lst.append(1)
    if "1" in word:
        word = word.replace("1", "i")
        lst.append(12)
    elif "!" in word:
        word = word.replace("!", "i")
        lst.append(13)
    if "@" in word:
        word = word.replace("@", "a")
        lst.append(2)
    elif "4" in word:
        word = word.replace("4", "a")
        lst.append(3)
    if "3" in word:
        word = word.replace("3", "e")
        lst.append(6)
    if "$" in word:
        word = word.replace("$", "s")
        lst.append(4)
    elif "5" in word:
        word = word.replace("5", "s")
        lst.append(5)
    if "2" in word:
        word = word.replace("2", "z")
        lst.append(11)
    if "%" in word:
        word = word.replace("%", "x")
        lst.append(14)
    if "7" in word:
        word = word.replace("7", "t")
        lst.append(10)
    elif "+" in word:
        word = word.replace("+", "t")
        lst.append(9)
    if "9" in word:
        word = word.replace("9", "g")
        lst.append(8)
    elif "6" in word:
        word = word.replace("6", "g")
        lst.append(7)
    return word, str(tuple(sorted(lst)))


def main(password, path):
    r, explain = rank(password, path)
    out_file(password, r)
    return r


def rank(password, path):
    a1_path = os.path.join(path, "a1.txt")
    a2_path = os.path.join(path, "a2.txt")
    a3_path = os.path.join(path, "a3.txt")
    a4_path = os.path.join(path, "a4.txt")
    a5_path = os.path.join(path, "a5.txt")
    L1 = rank_config.config.get(f'L1')
    L2 = rank_config.config.get(f'L2')
    first = True
    last = True
    f = len(password)
    l = -1
    L = -5
    explain = []
    if (isascii(password)):
        for i in range(len(password)):
            if (not (password[i].isdigit() or isSymbol(password[i]))) and (first == True):
                f = i
                first = False
            if (not (password[-(i + 1)].isdigit() or isSymbol(password[-(i + 1)]))) and (last == True):
                l = -(i + 1)
                last = False
        if f == len(password):
            p = password[0:f]
            maxProb = 0
            for i in range(0, len(p) + 1):
                for j in range(i, len(p) + 1):
                    P1 = p[:i]
                    unLeetP2 = p[i:j]
                    P3 = p[j:]
                    pp1 = BS.main(a1_path, P1)
                    pp2 = BS.main(a2_path, unLeetP2)
                    pp3 = BS.main(a3_path, P3)

                    if (pp1 != None and pp2 != None and pp3 != None):
                        if float(pp1) * float(pp2) * float(pp3) > maxProb:
                            maxProb = float(pp1) * float(pp2) * float(pp3)
                            G1 = P1
                            G2 = unLeetP2
                            G3 = P3
                            g1 = pp1
                            g2 = pp2
                            g3 = pp3

            pos1 = "()"
            pos2 = "()"
            if maxProb > 0:
                pp4 = BS.main4(a4_path, pos1)
                pp5 = BS.main4(a5_path, pos2)
                prob = maxProb * float(pp4) * float(pp5)
                L = ESrank.main2(L1, L2, prob, 14)
                L = sum(L) / 2

                explain = []
                if G2 != "":
                    explain.append([2, G2, g2])
                if G1 != "":
                    explain.append([1, g1])
                if G3 != "":
                    explain.append([3, g3])

            else:
                L = -5
                explain = []
        else:
            if f != 0:
                P1 = password[0:f]
                if l != -1:
                    P2 = password[f:l + 1]
                    P3 = password[l + 1:]
                else:
                    P2 = password[f:]
                    P3 = ""
            else:
                P1 = ""
                if l != -1:
                    P2 = password[f:l + 1]
                    P3 = password[l + 1:]
                else:
                    P2 = password[f:]
                    P3 = ""

            unShiftP2, pos1 = unShiftWord(P2)
            unLeetP2, pos2 = unLeetWord(unShiftP2)
            pp1 = BS.main(a1_path, P1)
            pp2 = BS.main(a2_path, unLeetP2)
            pp3 = BS.main(a3_path, P3)
            pp4 = BS.main4(a4_path, pos1)
            pp5 = BS.main4(a5_path, pos2)

            if (pp1 != None and pp2 != None and pp3 != None and pp4 != None and pp5 != None):
                prob = float(pp1) * float(pp2) * float(pp3) * float(pp4) * float(pp5)
                L = ESrank.main2(L1, L2, prob, 14)
                L = sum(L) / 2

                explain = []
                if unLeetP2 != "":
                    explain.append((2, unLeetP2, pp2))
                if P1 != "":
                    explain.append((1, pp1))
                if P3 != "":
                    explain.append((3, pp3))
                if pos1 != "()":
                    explain.append((4, pp4))
                if pos2 != "()":
                    explain.append((5, pp5))

            else:
                L = -5
                explain = []

    return [L, explain]


def out_file(user_name, r):
    unique_filename = str(uuid.uuid1())

    file_path = os.path.join(os.getcwd(), "out_regular", unique_filename + '.txt')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Prepare the user data or an error message
    try:
        log_r = str(math.log2(r)) if r >= 0 else "strong password"
        user_data = f"{user_name},{log_r},{time.asctime()}\n"
    except Exception as e:
        user_data = f"fail {e}\n"

    # Write the user data or error message to the file
    with open(file_path, 'w+') as file:
        file.write(user_data)
