import logging, subprocess
import os

def subprocess_call_with_logging(logfilePath, popenargs, **kwargs):
    LOG_FILE = os.path.basename(logfilePath)
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, filename=LOG_FILE, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    process = subprocess.Popen(popenargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def check_io():
           while True:
                output = process.stdout.readline().decode()
                if output:
                    logger.log(logging.INFO, output)
                else:
                    break

    # keep checking stdout/stderr until the child exits
    while process.poll() is None:
        check_io()

if __name__ == '__main__':
    subprocess_call_with_logging("test.log", ["ls", "-l"])