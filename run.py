import os
import time

def main():

    scripts = ['derived/code/make_images.py',
               'derived/code/ocr.py',
               'derived/code/clean.py',
               'analysis/code/make_data.py',
               'analysis/code/count.py']
    
    log_file = open("run.log", 'w')
    log_file.write("Started at " + time.strftime('%I:%M:%S%p %Z on %b %d, %Y\n\n'))
    
    for script in scripts:
        log_file.write(time.strftime('%I:%M:%S%p') + f"   :{script} started\n")
        os.system(f'python {script}')
        log_file.write(time.strftime('%I:%M:%S%p') + f"   :{script} completed\n")
    
    log_file.write("\nFinished at " + time.strftime('%I:%M:%S%p %Z on %b %d, %Y\n'))
    log_file.close()


if __name__ == '__main__':
    main()

