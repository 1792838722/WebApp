def b64_to_img(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)
    file.close()