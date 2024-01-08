# import os
# import subprocess
# import pkg_resources
#
#
# def extract_batch_file():
#     batch_content = pkg_resources.resource_string(__name__, 'run_server.bat')
#     batch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_server.bat')
#
#     with open(batch_path, 'wb') as batch_file:
#         batch_file.write(batch_content)
#
#     return batch_path
#
#
# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armsbackend.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#
#     # Run the main Django application using Gunicorn
#     execute_from_command_line(["manage.py"])
#
#
# if __name__ == '__main__':
#     # Extract the batch file to the script's directory
#     batch_file_path = extract_batch_file()
#
#     # Start the Waitress server using the extracted batch file
#     subprocess.Popen([batch_file_path])
#
#     # Run the main Django application
#     main()

# #!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys
#
#
# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armsbackend.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000", "--noreload"])
#     # execute_from_command_line(["waitress-serve", "--port=8000", "armsbackend.wsgi:application"])
#     # execute_from_command_line(sys.argv)
#
#
# if __name__ == '__main__':
#     main()

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armsbackend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
