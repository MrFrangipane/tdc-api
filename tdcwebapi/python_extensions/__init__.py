import os.path


_HERE = os.path.dirname(__file__)
_ROOT = os.path.dirname(_HERE)


def make_resource_path(relative_filepath):
    path = os.path.join(_ROOT, 'resources', relative_filepath)
    if os.path.sep == '\\':
        return path.replace('/', os.path.sep)

    return path.replace("\\", os.sep)
