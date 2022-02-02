remove(list=ls())
library(dplyr)
library(ggplot2)

# Load data

lgr_years <- c(1962, 1969, 1980)

df <- data.frame()
for (lgr in lgr_years) {
  df_lgr <- read.table(sprintf('../analysis/output/lgr%s_counts.csv', lgr),
                       sep = ',', header = T, fileEncoding = 'utf-8')
  df_lgr$year = lgr
  
  df <- rbind(df, df_lgr)
}


df_keywords <- read.table('keywords.csv', sep = ',', header = T,
                          fileEncoding = 'utf-8')


# Collect counts for words related to keywords

exact_words <- df_keywords[df_keywords$wildcard == 0, ]$keyword
df_exact    <- df %>% filter(word %in% exact_words)

df_exact$keyword  <- df_exact$word
df_exact$approach <- "exact"


wildcard_words <- df_keywords[df_keywords$wildcard == 1, ]$keyword

df_wildcard <- data.frame()
for (ww in wildcard_words) {
  df_word         <- df %>% filter(grepl(ww, word))
  df_word$keyword <- ww
  df_wildcard     <- rbind(df_wildcard, df_word)
}
df_wildcard$approach <- "wildcard"

df_counts <- rbind(df_exact, df_wildcard)


# Group counts by keywords

df_counts <- df_counts %>%
  group_by(approach, keyword, year) %>%
  summarize(Count = sum(n))


# Make plot

df_counts <- df_counts %>% filter(approach == "wildcard") # Keep wildcard words only

ggplot(df_counts,
       aes(y = Count, x = year, color = keyword)) +
  geom_line() +
  geom_point() +
  scale_x_continuous(breaks = lgr_years,
                     name   = "Year") +
  theme_bw() +
  theme(legend.position = 'bottom',
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank())
  
ggsave("keywords.png", height = 4, width = 5)
