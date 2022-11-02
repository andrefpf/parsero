EPSILON = "&"
BLANK = " \n"
SPECIAL = "!@#$%_-=,.:;/'\""
DIGIT = "0123456789"
LOWER_CASE = "abcdefghijklmnopqrstuvxwyz"
UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVXWYZ"
ALPHANUMERIC = DIGIT + LOWER_CASE + UPPER_CASE + BLANK
SYMBOL = DIGIT + LOWER_CASE + UPPER_CASE + BLANK + SPECIAL

any_blank = "|".join(BLANK)
any_digit = "|".join(DIGIT)
any_lower_case = "|".join(LOWER_CASE)
any_upper_case = "|".join(UPPER_CASE)
any_alphanumeric = "|".join(ALPHANUMERIC)
any_symbol = "|".join(SYMBOL)
