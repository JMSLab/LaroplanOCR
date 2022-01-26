import os
import time
import pytesseract
import layoutparser as lp
import cv2

def main():
    instub  = 'derived/output/images'
    outstub = 'derived/output/text'

    laroplans = ['1962', '1969', '1980']
    fl_pages = {'1962':[10, 441],
                '1969':[11, 225],
                '1980':[9,  154]}
    ocr_agent = lp.TesseractAgent(languages = 'swe')

    for lgr in laroplans:

        pages = [f'page_{i}.jpg' for i in range(fl_pages[lgr][1] - fl_pages[lgr][0] + 1)]

        laroplan_text = ''

        start = time.time()
        for i, pagefile in enumerate(pages):

            page = cv2.imread(os.path.join(instub, lgr, pagefile))

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
        if lgr == laroplans[0]:
            f_log = open(os.path.join(outstub, 'ocr_runtimes.log'), 'w')

        runtime = round((end - start)/60, 2)

        f_log.write(f'*** LAROPLAN {lgr} ***\n')
        f_log.write(f'OCR runtime:    {runtime} minutes.\n\n')

        if lgr == laroplans[-1]:
            f_log.close()

if __name__ == '__main__':
    main()
