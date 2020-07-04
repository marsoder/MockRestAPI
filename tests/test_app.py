import os
import pytest
import sys
sys.path.append("/home/xioahei/Learning/MockRiksdagAPI/")
from models import Transcript, TranscriptSchema


@pytest.fixture(scope="session")
def app():
    abs_file_path = os.path.abspath(os.path.dirname(__file__))

