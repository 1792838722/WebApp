def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # 获取文件扩展名
    valid_extensions = ['.jpg', '.jpeg', '.png']  # 支持的文件扩展名
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
