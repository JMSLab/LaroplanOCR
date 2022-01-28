import os
import time
import cv2
import layoutparser as lp
import pandas       as pd

def main():
    instub  = 'derived/output/images'
    outstub = 'derived/output/text'

    df_lgr = pd.read_csv('laroplaner.csv')
    lgr_years = df_lgr.year.tolist()

    ocr_agent = lp.TesseractAgent(languages = 'swe')

    for lgr in lgr_years:

        f_p = df_lgr.loc[df_lgr.year == lgr].first_rel_page.values[0]
        l_p = df_lgr.loc[df_lgr.year == lgr].last_rel_page.values[0]

        pages = [f'page_{i}.jpg' for i in range(l_p - f_p + 1)]

        laroplan_text = ''

        start = time.time()
        for i, pagefile in enumerate(pages):

            page = cv2.imread(os.path.join(instub, str(lgr), pagefile))

            result = ocr_agent.detect(page, return_response = True)

            laroplan_text += f'\n\n***** PAGE {i} *****\n\n'
            laroplan_text += result['text']

        end = time.time()

        # Save results
        textfile = os.path.join(outstub, f'laroplan_{lgr}.txt')
        with open(textfile, 'w', encoding='utf-8') as f:
            f.write(laroplan_text)
        f.close()

        # Log runtime
        if lgr == lgr_years[0]:
            f_log = open(os.path.join(outstub, 'ocr_runtimes.log'), 'w')

        runtime = round((end - start)/60, 2)

        f_log.write(f'*** LAROPLAN {lgr} ***\n')
        f_log.write(f'OCR runtime:    {runtime} minutes.\n\n')

        if lgr == lgr_years[-1]:
            f_log.close()

if __name__ == '__main__':
    main()
