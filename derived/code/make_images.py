import os
import time
from pdf2image import convert_from_path

def main():
    instub  = 'raw/orig'
    outstub = 'derived/output/images'

    quality = 400
    threads = 4

    laroplans = ['1962', '1969', '1980']
    fl_pages = {'1962':[10, 441],
                '1969':[11, 225],
                '1980':[9,  154]}

    for lgr in laroplans:

        f = f'Laroplan {lgr}.pdf'
        if lgr == '1980':
            f = f'Laroplan {lgr} (subject).pdf'
        
        start_conv = time.time()
        pages = convert_from_path(os.path.join(instub, f), 
                                  dpi = quality, 
                                  first_page = fl_pages[lgr][0], last_page = fl_pages[lgr][1],
                                  thread_count = threads)
        end_conv = time.time()

        outfolder = os.path.join(outstub, lgr)
        make_output_dir(outfolder)

        start_sav = time.time()
        for i, page in enumerate(pages):
            page.save(os.path.join(outfolder, f'page_{i}.jpg'), 'JPEG')
        end_sav = time.time()

        if lgr == laroplans[0]:
            f_log = open(os.path.join(outstub, 'pdf2jpg_runtimes.log'), 'w')

        runtime_conv = round((end_conv - start_conv)/60, 2)
        runtime_sav  = round((end_sav  - start_sav )/60, 2)
        
        f_log.write(f'*** LAROPLAN {lgr} ***\n')
        f_log.write(f'Conversion runtime:    {runtime_conv} minutes.\n')
        f_log.write(f'Saving files runtime:    {runtime_sav} minutes.\n\n')

        if lgr == laroplans[-1]:
            f_log.close()

def make_output_dir(outfolder):

    if not os.path.isdir(outfolder):
        os.mkdir(outfolder)

    return None


if __name__ == '__main__':
    main()
