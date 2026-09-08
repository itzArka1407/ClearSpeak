import re


# ===================================
# CRITICAL INFORMATION DETECTION
# ===================================

def detect_critical_information(text):

    detected = []
    detected_values = set()

    def add_detection(info_type, value):

        key = (info_type, value)

        if key not in detected_values:

            detected.append({
                "type": info_type,
                "value": value
            })

            detected_values.add(key)


    # ===================================
    # PHONE NUMBERS
    # ===================================

    phone_pattern = r'\b[6-9]\d{9}\b'

    for match in re.finditer(phone_pattern, text):

        add_detection(
            "📞 Phone Number",
            match.group()
        )


    # ===================================
    # TIME
    # Examples:
    # 4:30 PM
    # 10:15 AM
    # ===================================

    time_pattern = (
        r'\b'
        r'(?:1[0-2]|0?[1-9])'
        r':'
        r'[0-5][0-9]'
        r'\s?'
        r'(?:AM|PM|am|pm)'
        r'\b'
    )

    for match in re.finditer(time_pattern, text):

        add_detection(
            "🕒 Time",
            match.group()
        )


    # ===================================
    # MONEY
    # Examples:
    # ₹1,500
    # $100
    # €50
    # £99.99
    # ===================================

    money_pattern = (
        r'[₹$€£]'
        r'\s?'
        r'\d[\d,]*'
        r'(?:\.\d{1,2})?'
    )

    for match in re.finditer(money_pattern, text):

        add_detection(
            "💰 Money",
            match.group()
        )


    # ===================================
    # MIXED IDENTIFIERS
    #
    # Examples:
    # REF-ABC-4821
    # 678-ABC-007
    # TXN@89#X21
    # AB#72X!9
    # ===================================

    identifier_pattern = (
        r'\b'
        r'(?=[A-Za-z0-9#@!_\-/.]*[A-Za-z])'
        r'(?=[A-Za-z0-9#@!_\-/.]*\d)'
        r'[A-Za-z0-9#@!_\-/.]+'
        r'\b'
    )

    for match in re.finditer(identifier_pattern, text):

        value = match.group()

        # Avoid incorrectly treating normal values
        # as mixed identifiers

        if not re.fullmatch(phone_pattern, value):

            add_detection(
                "🆔 Mixed Identifier",
                value
            )


    # ===================================
    # NUMERIC CODES
    # Examples:
    # 583291
    # 1234
    # 987654
    # ===================================

    code_pattern = r'\b\d{4,8}\b'

    for match in re.finditer(code_pattern, text):

        value = match.group()

        # Don't detect a phone number as a code

        if not re.fullmatch(phone_pattern, value):

            add_detection(
                "🔢 Numeric Code",
                value
            )


    return detected


# ===================================
# SPEECH DICTIONARIES
# ===================================

DIGIT_WORDS = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine"
}


SYMBOL_WORDS = {
    "-": "dash",
    "#": "hash",
    "@": "at symbol",
    "!": "exclamation mark",
    "_": "underscore",
    "/": "slash",
    ".": "dot"
}


# ===================================
# CHARACTER-BY-CHARACTER SPEECH
# ===================================

def speak_character_by_character(value):

    spoken_parts = []

    for character in value:

        # Numbers

        if character.isdigit():

            spoken_parts.append(
                DIGIT_WORDS[character]
            )


        # Letters

        elif character.isalpha():

            spoken_parts.append(
                character.upper()
            )


        # Symbols

        elif character in SYMBOL_WORDS:

            spoken_parts.append(
                SYMBOL_WORDS[character]
            )


        # Ignore spaces

        elif character.isspace():

            continue


        else:

            spoken_parts.append(character)


    # Deliberate pauses between critical characters

    return " ... ".join(spoken_parts)


# ===================================
# NUMBER TO WORDS
# ===================================

def number_to_words(number):

    number = int(number)

    if number == 0:
        return "zero"

    ones = [
        "",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine"
    ]

    teens = [
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen"
    ]

    tens = [
        "",
        "",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety"
    ]


    def convert_below_thousand(n):

        words = []

        if n >= 100:

            words.append(ones[n // 100])
            words.append("hundred")

            n %= 100


        if n >= 20:

            words.append(tens[n // 10])

            if n % 10 != 0:

                words.append(
                    ones[n % 10]
                )


        elif n >= 10:

            words.append(
                teens[n - 10]
            )


        elif n > 0:

            words.append(
                ones[n]
            )


        return " ".join(words)


    parts = []

    # Millions

    if number >= 1_000_000:

        parts.append(
            convert_below_thousand(
                number // 1_000_000
            )
        )

        parts.append("million")

        number %= 1_000_000


    # Thousands

    if number >= 1000:

        parts.append(
            convert_below_thousand(
                number // 1000
            )
        )

        parts.append("thousand")

        number %= 1000


    # Remaining

    if number > 0:

        parts.append(
            convert_below_thousand(number)
        )


    return " ".join(parts)


# ===================================
# TIME TRANSFORMATION
# ===================================

def transform_time(value):

    """
    Example:

    4:30 PM
        ↓
    four thirty P M
    """

    match = re.match(

        r'(\d{1,2})'
        r':'
        r'(\d{2})'
        r'\s?'
        r'(AM|PM|am|pm)',

        value
    )


    if not match:

        return value


    hour = int(match.group(1))

    minute = int(match.group(2))

    period = match.group(3).upper()


    hour_words = number_to_words(hour)


    if minute == 0:

        minute_words = "o'clock"

    elif minute < 10:

        minute_words = (
            "zero "
            + number_to_words(minute)
        )

    else:

        minute_words = number_to_words(minute)


    period_words = "A M" if period == "AM" else "P M"


    return (
        f"{hour_words} "
        f"{minute_words} "
        f"{period_words}"
    )


# ===================================
# MONEY TRANSFORMATION
# ===================================

def transform_money(value):

    """
    Examples:

    ₹1,500
        ↓
    one thousand five hundred rupees

    $100
        ↓
    one hundred dollars
    """

    currency_map = {
        "₹": "rupees",
        "$": "dollars",
        "€": "euros",
        "£": "pounds"
    }


    currency_symbol = value[0]

    currency_name = currency_map.get(
        currency_symbol,
        ""
    )


    # Remove symbol and commas

    number_string = (
        value[1:]
        .strip()
        .replace(",", "")
    )


    try:

        # Handle decimals

        if "." in number_string:

            whole_part, decimal_part = (
                number_string.split(".")
            )

            whole_words = number_to_words(
                whole_part
            )

            decimal_words = (
                " ".join(
                    DIGIT_WORDS[digit]
                    for digit in decimal_part
                )
            )

            return (
                f"{whole_words} "
                f"{currency_name} "
                f"and {decimal_words} cents"
            )


        # Normal whole number

        number_words = number_to_words(
            number_string
        )


        return (
            f"{number_words} "
            f"{currency_name}"
        )


    except ValueError:

        return value


# ===================================
# TRANSFORM SINGLE VALUE
# ===================================

def transform_value(info_type, value):


    # PHONE NUMBER

    if "Phone Number" in info_type:

        return speak_character_by_character(value)


    # NUMERIC CODE

    elif "Numeric Code" in info_type:

        return speak_character_by_character(value)


    # MIXED IDENTIFIER

    elif "Mixed Identifier" in info_type:

        return speak_character_by_character(value)


    # TIME

    elif "Time" in info_type:

        return transform_time(value)


    # MONEY

    elif "Money" in info_type:

        return transform_money(value)


    return value


# ===================================
# FULL CLEARSPEAK TRANSFORMATION
# ===================================

def transform_for_clarity(text):

    detected_info = detect_critical_information(text)

    transformed_text = text


    # Sort values from longest to shortest.
    # This prevents partial replacements.

    detected_info.sort(
        key=lambda item: len(item["value"]),
        reverse=True
    )


    for item in detected_info:

        info_type = item["type"]

        value = item["value"]


        transformed_value = transform_value(
            info_type,
            value
        )


        transformed_text = transformed_text.replace(
            value,
            transformed_value
        )


    return transformed_text