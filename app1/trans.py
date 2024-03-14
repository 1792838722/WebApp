from PIL import Image


def transform(src_file, filename):
    img = Image.open(src_file)
    img.rotate(90).save('resource/img/' + filename)
