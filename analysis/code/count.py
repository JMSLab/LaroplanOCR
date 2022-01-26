import os
import pandas as pd

def main():
    instub  = 'analysis/output'
    outstub = 'analysis/output'

    laroplans = ['1962', '1969', '1980']
    
    for lgr in laroplans:

        df = pd.read_csv(os.path.join(instub, f'lgr{lgr}_sentences.csv'), 
                         encoding = 'utf-8')
        
        df_words = make_words_dataset(df)
        
        df_words['word'] = df_words.word.str.lower()      # All characters to lowercase
        
        df_counts = df_words[["word_num", "word"]].groupby('word').count().reset_index()
        df_counts.columns = ["word", "n"]
        
        df_counts.to_csv(os.path.join(outstub, f'lgr{lgr}_counts.csv'),
                         encoding = 'utf-8')


def make_words_dataset(df, key_vars = ["page", "paragraph_id", "sentence_num"]):
    
    df_wide = pd.concat([df[key_vars], df.sentence_text.str.split(" ", expand = True)], axis = 1)
    
    max_n_words = len(df_wide.columns) - len(key_vars)
    df_wide.columns = key_vars + [f"word_{i}" for i in range(1, max_n_words + 1)]
    
    df_long = df_wide.melt(id_vars = key_vars, 
                           value_vars = [f"word_{i}" for i in range(1, max_n_words + 1)],
                           var_name   = "word_num", value_name = "word")
    
    df_long.dropna(inplace = True)
    
    df_long['word'] = df_long.word.str.replace(r'[\(\)\:\,\"”\'\.\s/&\+<>]+', '')
    
    for elem in ["", "*****", "—", "!", "$", "&", "+", "-", "/", ";", ">", ">>", "<", "<<"]:
        df_long = df_long[df_long.word != elem]
    
    numbers = df_long.word.str.isdecimal().astype("boolean")
    df_long = df_long[~numbers]
    
    return df_long


if __name__ == '__main__':
    main()
