#############################
## SUBPROCESS WITH LOGGING
#############################
import subprocess
import logging
import os

def subprocess_call_with_logging(logfilePath, popenargs, **kwargs):
    LOG_FILE = os.path.basename(logfilePath)
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, filename=LOG_FILE, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    process = subprocess.Popen(popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    

def subprocess_call_with_str_logging(popenargs, **kwargs):

    process = subprocess.Popen(popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def check_io():
        interim_text = ""
        while True:
            output = process.stdout.readline().decode()
            if output:
                interim_text += "{output}\n".format(output=output)
            else:
                break

    # keep checking stdout/stderr until the child exits
    log_txt = ""
    while process.poll() is None:
        interim_text = check_io()
        if interim_text:
            log_txt += "{interim_text}\n".format(interim_text=interim_text)
    return log_txt

def subprocess_call_with_output_returned(popenargs, **kwargs):
    proc = subprocess.Popen(popenargs, **kwargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate()
    return outs, errs

    
