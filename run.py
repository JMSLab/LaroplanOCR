import os
import time

def main():

    scripts = ['derived/code/make_images.py',
               'derived/code/ocr.py',
               'derived/code/clean.py',
               'analysis/code/make_data.py',
               'analysis/code/count.py']
    
    log_file = open("run.log", 'w')
    log_file.write(f"Compilation started at {time.strftime('%I:%M%p %Z on %b %d, %Y\n')}")
        
    for script in scripts:
        os.system(f'python {script}')
        log_file.write(f"{script} completed at {time.strftime('%I:%M%p %Z\n')}")
    
    log_file.write(f"Finished at {time.strftime('%I:%M%p %Z\n')}")
    log_file.close()


if __name__ == '__main__':
    main()

