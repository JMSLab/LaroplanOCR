import os
import time
import pandas as pd
from pdf2image import convert_from_path

def main():
    instub  = 'raw/orig'
    outstub = 'derived/output/images'

    quality = 400
    threads = 6

    df_lgr = pd.read_csv('laroplaner.csv')
    lgr_years = df_lgr.year.tolist()

    for lgr in lgr_years:

        f = df_lgr.loc[df_lgr.year == lgr].file.values[0]

        fp = df_lgr.loc[df_lgr.year == lgr].first_rel_page.values[0]
        lp = df_lgr.loc[df_lgr.year == lgr].last_rel_page.values[0]
        
        start_conv = time.time()
        pages = convert_from_path(os.path.join(instub, f), 
                                  dpi = quality, 
                                  first_page = fp, last_page = lp,
                                  thread_count = threads)
        end_conv = time.time()

        outfolder = os.path.join(outstub, str(lgr))
        make_output_dir(outfolder)

        start_sav = time.time()
        save_files(pages, lgr, outfolder)
        end_sav = time.time()

        if lgr == lgr_years[0]:
            f_log = open(os.path.join(outstub, 'pdf2jpg_runtimes.log'), 'w')

        runtime_conv = round((end_conv - start_conv)/60, 2)
        runtime_sav  = round((end_sav  - start_sav )/60, 2)
        
        f_log.write(f'*** LAROPLAN {lgr} ***\n')
        f_log.write(f'Conversion runtime:    {runtime_conv} minutes.\n')
        f_log.write(f'Saving files runtime:    {runtime_sav} minutes.\n\n')

        if lgr == lgr_years[-1]:
            f_log.close()

def make_output_dir(outfolder):

    if not os.path.isdir(outfolder):
        os.mkdir(outfolder)

    return None

def save_files(pages, lgr, outfolder):

    for i, page in enumerate(pages):
        if lgr == "1994b" and i == 17: # Skip cover in middle of pdf
            continue
        else:
            page.save(os.path.join(outfolder, f'page_{i}.jpg'), 'JPEG')

    return None

if __name__ == '__main__':
    main()
