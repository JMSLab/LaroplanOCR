import os
import pandas as pd
import numpy  as np

def main():
    instub  = 'derived/output/text'
    outstub = 'analysis/output'

    laroplans = ['1962', '1969', '1980']
    
    for lgr in laroplans:

        file = open(os.path.join(instub, f'lgr{lgr}_clean.txt'), 
                    'r', encoding = 'utf-8')
        lgr_text = ''.join(file.readlines())
        file.close()

        paragraphs = lgr_text.split('\n\n')

        df_paragraphs = make_paragraphs_dataset(paragraphs)
        df_sentences  = make_sentences_dataset(df_paragraphs)
        
        csv_par = os.path.join(outstub, f'lgr{lgr}_paragraphs.csv')
        df_paragraphs.to_csv(csv_par, encoding = 'utf-8', index = False)
        
        csv_sent = os.path.join(outstub, f'lgr{lgr}_sentences.csv')
        df_sentences.to_csv(csv_sent, encoding = 'utf-8', index = False)

def make_paragraphs_dataset(paragraphs):
    
    paragraphs = [par.strip() for par in paragraphs if par.strip() != ""]
    
    df = pd.DataFrame({'paragraph':paragraphs})
    
    # Construct page
    df["is_page_delim"] = df.paragraph.str.match(r"\*\*\*\*\* PAGE \d+ \*\*\*\*\*")
    df["number"]        = df.paragraph.str.extract(r"(\d+)").astype("float")
    df["page"]          = np.where(df.is_page_delim == 1, df.number, np.array([np.nan]*df.shape[0]))
    df.page.ffill(inplace = True) 
    
    # Get rid of page delimiters and group paragraph across pages when appropriate
    df["page_begin"] = df.is_page_delim.shift(1).fillna(False).astype("bool")
    df["page_end"]   = df.is_page_delim.shift(-1).fillna(False).astype("bool")
    df["first_char"] = df.paragraph.str[0]
    
    df = df[df["is_page_delim"] == False]
    
    df["crosspage_par_ends"]   = (df.page_end.shift(1) & \
                                  df.page_begin & df.first_char.str.islower())
        
    df["paragraph_id"] = np.array(range(df.shape[0])) - df.crosspage_par_ends
            
    df_pages = df[["paragraph_id", "page"]].groupby(["paragraph_id"]).min("page")
    df_text  = df[["paragraph_id", "paragraph"]].groupby(["paragraph_id"])\
                                .paragraph.apply(lambda x : ' '.join(x))

    df = pd.merge(df_pages, df_text, on = "paragraph_id").reset_index()
    
    df["page"]         = df.page.astype("int")
    df["paragraph_id"] = df.paragraph_id.astype("int")

    return df[["page", "paragraph_id", "paragraph"]]

def make_sentences_dataset(df):
    
    key = ["page", "paragraph_id", "paragraph"]

    df_wide = pd.concat([df,
                         df.paragraph.str.split(".", expand = True)],
                        axis = 1)
    max_n_sent = len(df_wide.columns) - len(key)
    df_wide.columns = key + [f"sentence_{i}" for i in range(1, max_n_sent + 1)]
    
    df_long = df_wide.melt(id_vars = ["paragraph_id", "paragraph", "page"], 
                           value_vars = [f"sentence_{i}" for i in range(1, max_n_sent + 1)],
                           var_name   = "sentence_num", value_name = "sentence_text")
    
    df_long.dropna(inplace = True)
    df_long = df_long[df_long.sentence_text != ""]
    df_long['sentence_num'] = df_long.groupby(["paragraph_id"]).cumcount() + 1   # Recode sentence num after dropping missing
    
    df_long.sort_values(by = ["paragraph_id", "sentence_num"], inplace = True)
    df_long["sentence_text"] = df_long.sentence_text.str.strip()
    
    return df_long[["page", "paragraph_id", "sentence_num", "sentence_text"]]


if __name__ == '__main__':
    main()
