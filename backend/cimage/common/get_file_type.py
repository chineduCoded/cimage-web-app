def get_file_type(binary_data):
    file_types = {
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'\xFF\xD8\xFF': 'JPEG',
        b'GIF87a': 'GIF',
        b'GIF89a': 'GIF',
        b'\x42\x4D': 'BMP',  # BMP file signature
        # Add more file signatures and corresponding file types as needed
    }

    for signature, file_type in file_types.items():
        if binary_data.startswith(signature):
            return file_type

    return 'Unknown'