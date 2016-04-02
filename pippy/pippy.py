# Standard Library
import os
import shutil
import sys
import tarfile

# Dependencies
import pipista_custom # This pipista was hacked to return the filename.

MODULE_NAME = 'faker'
PACKAGE_NAME = 'fake-factory'

mod_path = os.path.abspath(__file__)
mod_dir = os.path.dirname(mod_path)
print mod_dir
SITE_PACKAGES_DIR = 'site-packages'
TMP_DIR = os.path.join(mod_dir, 'tmp_pippy', MODULE_NAME)

ORIGINAL_WORKING_DIR = os.getcwd()


def download_and_extract(pkg_name, tmp_dir):
    tarball_filename = _download_pypi_tarball(pkg_name, tmp_dir)
    tarball_path = os.path.join(tmp_dir, tarball_filename)
    _extract_tarball(tarball_path, tmp_dir)


def _download_pypi_tarball(pkg_name, tmp_dir=None):
    try:
        os.mkdir(tmp_dir)
    except:
        print 'tmp directory already exists: %s', tmp_dir

    os.chdir(tmp_dir)
    tarball_filename = pipista_custom.pypi_download(pkg_name)
    os.chdir(ORIGINAL_WORKING_DIR)

    return tarball_filename

def _extract_tarball(path_to_tarball, path=None):
    with tarfile.open(path_to_tarball) as tar:
        tar.extractall(path=path)

def find_egg(pkg_name, path):
    """
    Find the egg.

    >>> pkg_name = 'fake-factory'

    >>> tmp_pippy = 'tmp_pippy'

    >>> find_egg(pkg_name, tmp_pippy) # doctest: +ELLIPSIS
    'tmp_pippy/.../fake_factory.egg-info'




    """
    underscored_name = pkg_name.replace('-', '_')
    egg_name = underscored_name + '.egg-info'
    egg_path = _find_dir(egg_name, path)
    return egg_path

def find_new_module(mod_name, path):
    """
    Find the module we just downloaded.

    >>> name = 'faker'

    >>> tmp_pippy = 'tmp_pippy'

    >>> find_new_module(name, tmp_pippy)
    'tmp_pippy/faker'




    """
    module_tmp_directory = _find_dir(mod_name, path)
    return module_tmp_directory

def _find(name, path):
    for root, dirs, files in os.walk(path):
        print(root, dirs, files)
        if name in files:
            return os.path.join(root, name)

def _find_dir(name, path):
    """
    Find a directory

    >>> _find_dir('faker', 'tmp_pippy/')
    'tmp_pippy/faker'


    """
    for root, dirs, files in os.walk(path):
        if name in dirs:
            dir_path = os.path.join(root, name)
            return dir_path

def install(mod_name, pkg_name=None, path=TMP_DIR):
    if not pkg_name: pkg_name = mod_name
    egg_path = find_egg(pkg_name, path)
    mod_path = find_new_module(mod_name, path)

    try:
        shutil.move(egg_path, SITE_PACKAGES_DIR)
        shutil.move(mod_path, SITE_PACKAGES_DIR)
    except:
        handle_exception(sys.exc_info())

def clean_up(tmp_dir):
    shutil.rmtree(tmp_dir)

def main():
    download_and_extract(PACKAGE_NAME, TMP_DIR)
    install(MODULE_NAME, PACKAGE_NAME, TMP_DIR)
    clean_up(TMP_DIR)

def handle_exception(info):
    print "Exception! " + repr(info[1])

if __name__ == '__main__':
    main()

