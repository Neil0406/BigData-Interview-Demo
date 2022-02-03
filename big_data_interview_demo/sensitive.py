#SQL DB
DEFAULT_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'big_data_interview',
        'USER': 'root',
        'PASSWORD': '123456',
        # 'HOST': '127.0.0.1',
        'HOST': 'big_data_interview_mariadb',
        'PORT': '3306',
    }
}


