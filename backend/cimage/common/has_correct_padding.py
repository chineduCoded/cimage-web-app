def has_correct_padding(base64_str):
    # Check if the length of the base64 string is a multiple of 4
    return len(base64_str) % 4 == 0