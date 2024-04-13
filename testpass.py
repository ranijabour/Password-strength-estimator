import re

def find_date(text):
    date_pattern = r'\b(19\d{2}|20[0-1]\d|2023)(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])|' \
                   r'(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(19\d{2}|20[0-1]\d|2023)|' \
                   r'(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])(19\d{2}|20[0-1]\d|2023)|' \
                   r'(19\d{2}|20[0-1]\d|2023)|' \
                   r'(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])|' \
                   r'(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\b'

    match = re.search(date_pattern, text)
    if match:
        return match.group()


def contains_mutual_substring(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Variables to keep track of the maximum length and ending position of the substring
    max_length = 0
    end_position = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_position = i  # Update the ending position of the substring
            else:
                dp[i][j] = 0

    # If a common substring of length greater than 2 exists, extract it
    if max_length > 2:
        start_position = end_position - max_length
        largest_common_substring = str1[start_position:end_position]
        return 1, largest_common_substring

    return 0, ""

