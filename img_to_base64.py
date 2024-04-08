import base64

def img_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_str = base64.b64encode(file.read()).decode('utf-8')
    file.close()
    return encoded_str
