import os

def main():

    scripts = ['derived/code/make_images.py',
               'derived/code/ocr.py',
               'derived/code/clean.py',
               'analysis/code/make_data.py',
               'analysis/code/count.py']
    
    for script in scripts:
        os.system(f'python {script}')


if __name__ == '__main__':
    main()

