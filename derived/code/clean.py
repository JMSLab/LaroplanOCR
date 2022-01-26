import os
import re

def main():
    instub  = 'derived/output/text'
    outstub = 'derived/output/text'

    laroplans = ['1962', '1969', '1980']
    first_nonindex_page = {'1962':8, '1969':4, '1980':2}
    
    for lgr in laroplans:

        file = open(os.path.join(instub, f'laroplan_{lgr}.txt'), 'r', encoding = 'utf-8')
        lgr_raw_text = ''.join(file.readlines())
        file.close()

        lgr_text = remove_toc_pages(lgr_raw_text, first_nonindex_page[lgr])
        lgr_text = clean_text(lgr_text)
        lgr_text = fixes_to_punctuation(lgr_text)
        lgr_text = lgr_text.strip()

        file = open(os.path.join(outstub, f"lgr{lgr}_clean.txt"),
                    'w', encoding = 'utf-8')
        file.write(lgr_text)
        file.close()


def remove_toc_pages(text, first_page):

    return text[text.find(f'\n\n***** PAGE {first_page} *****'):]

def clean_text(text):
    
    text = re.sub(r"(?: )?\x0c(?: )?", "", text)   # Drop \x0c symbol

    text = re.sub(r"\n:?\d{1,3}\n", "", text)                            # Drop page numbering (sometimes has : before)
    text = re.sub(r"\n(\d{1,3}|[A-Z]) ?—? ?\d{1,7}\n", "", text)         # Drop other numbering (see page 28 in lgr 62 as example)
    text = re.sub(r"-\n{1,5}", "", text)                                 # Join paragraphs when indicated by -, up to 5 \n and lowercase
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)                         # Change \n for space, preserving \n{2,}
    text = re.sub(r"([a-z0-9åäöø])\n{1,4}([a-zåäöø])", r"\1 \2", text)   # Change \n{1,4} for space if next sentence continues in lowercase
    text = re.sub(r"([a-z0-9åäöø])\n{1,4}([0-9]+ [a-zåäöø])", r"\1 \2", text) # Change \n{1,4} for space if next sentence continues in number and lowercase

    return(text)

def fixes_to_punctuation(text):
    
    text = text.replace(" . ", "")                                    # Remove . surrounded by spaces
    text = re.sub(r"([a-z0-9åäöø])\.( [a-zåäöø])", r"\1\2", text)     # Remove . if next sentences starts with lowercase
    text = re.sub(r"([a-zåäöø]) ?(\,|;) ([A-ZÅÄÖØ])", r"\1. \3", text) # , and ; should be . if next sentence starts with uppercase

    return(text)


if __name__ == '__main__':
    main()
