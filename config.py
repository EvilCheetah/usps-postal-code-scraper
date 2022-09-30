from os import getenv
from pathlib import Path


def config():
    _check_env_variables()
    _create_necessary_directories()


def _check_env_variables():
    '''
        Ensures all Environment variables are set
    '''
    if ( not getenv('OUTPUT_DIRECTORY') ):
        raise RuntimeError('Please provide "OUTPUT_DIRECTORY" in ".env" file')

    if ( not getenv('OUTPUT_FILE') ):
        raise RuntimeError('Please provide "OUTPUT_FILE" in ".env" file')


def _create_necessary_directories():
    '''
        Creates necessary directories if they don't already exist
    '''
    if ( not Path( getenv('OUTPUT_DIRECTORY') ).is_dir() ):
        Path('OUTPUT_DIRECTORY').mkdir(parents = True, exist_ok = True)