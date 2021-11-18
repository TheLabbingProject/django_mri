import os
import shutil
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

from tests.fixtures import IMPORTED_DIR

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.test_settings"
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    shutil.rmtree(IMPORTED_DIR)
    sys.exit(bool(failures))
