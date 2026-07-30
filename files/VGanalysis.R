# Title : VideoGames Analysis
# Author : Alex Bass
# Description : Making a few charts for Donkey Kong Power Point

## packages -------

library(tidyverse)
library(patchwork)
library(showtext)
library(lubridate)

## cleaning and variable creation -------

font <- "Lato" #selected font

font_add_google(font, family = font)
showtext_auto()

data <- read_csv('vgsales.csv')

data$Name <- toupper(data$Name)

data$Type <- factor(ifelse(grepl("DONKEY",data$Name), "Donkey Kong",
                         ifelse(grepl("MARIO",data$Name), "Mario", 
                                ifelse(grepl("POKE",data$Name), "Pokemon",
                                       ifelse(grepl("ZELDA",data$Name), "Zelda",
                                              ifelse(grepl("ANIMAL CROSSING",data$Name), "Animal Crossing", "Other game"))))),
       levels = c("Donkey Kong", "Mario", "Pokemon", "Zelda", "Animal Crossing", "Other game"))

data$Nintendo <- factor(ifelse(grepl("Nintendo",data$Publisher), "Nintendo", "Other maker"),
                  levels = c("Nintendo", "Other maker"))

Nintendo <- data[data$Nintendo == "Nintendo",]

## plot and save ----

plot_data <- Nintendo %>% 
  group_by(Type) %>% 
  summarise(Mean = mean(Global_Sales)) %>% 
  arrange(desc(Mean)) %>% 
  mutate(color = ifelse(Type == 'Donkey Kong', "dodgerblue3", "grey40"))

plot_data %>% 
  ggplot(aes(x = reorder(Type, Mean), y = Mean)) +
  geom_bar(stat = "identity", fill = plot_data$color) +
  coord_flip() +
  theme_minimal() + 
  labs(
    y = 'Average Sales in Millions',
    x = ''
  ) + 
  theme(legend.position = "none",
        axis.title = element_text(family = font, size = 24),
        axis.text = element_text(family = font, size = 18)
        ) + 
  scale_color_manual(values = c("dodgerblue3", "grey"))

ggsave('NintendoSales.png', width = 2000, height = 1000, units = 'px')

Nintendo %>% 
  mutate(DK = ifelse(Type == "Donkey Kong", "Donkey Kong", "Other Nintendo\n Games"),
         Year = car::recode(as.numeric(Year), '1980:1984="80s"; 1985:1989="85s"; 1990:1994="90s";1995:1999="95s"; 2000:2004="00s";2005:2009="05s";2010:2021="10s";else=NA', as.factor = T, levels = c('80s','85s', '90s','95s', '00s', '05s','10s'))) %>% 
  drop_na(starts_with("Year")) %>% 
  group_by(Year, DK) %>% 
  summarise(Mean = mean(Global_Sales)) %>% 
  ggplot(aes(x = Year, y = Mean, color = DK, group = DK)) + 
  geom_line() +
  theme_minimal() + 
  theme(
    legend.title = element_blank(),
    axis.title = element_text(family = font, size = 14),
    axis.text = element_text(family = font, size = 14),
    legend.text = element_text(family = font, size = 12)
  ) + 
  scale_color_manual(values = c('dodgerblue3', 'grey')) + 
  ylim(0,7) + 
  labs(y = "Average Sales in Millions")

ggsave('NintendoSalesOverTime.png', width = 2000, height = 1000, units = 'px')
