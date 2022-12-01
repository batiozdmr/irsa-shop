from storages.backends.s3boto3 import S3Boto3Storage


class MediaS3BotoStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        super(MediaS3BotoStorage, self).__init__(*args, **kwargs)


class ThumbS3BotoStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'thumb'
        super(ThumbS3BotoStorage, self).__init__(*args, **kwargs)


class StaticS3BotoStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(StaticS3BotoStorage, self).__init__(*args, **kwargs)
