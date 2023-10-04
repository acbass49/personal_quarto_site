#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| eval: false
library(gtrendsR)
library(ggplot2)
library(ggstream)
library(showtext)
font_add_google("Cairo", family = "Cairo")
showtext_auto()

obj <- gtrends(
    keyword = c("Donald Trump", "Ron DeSantis", "Mike Pence", "Nikki Haley", "Vivek Ramaswamy"),
    time = paste("2023-01-01",as.character(Sys.Date())),
    geo = "US",
    onlyInterest = TRUE
)

df <- obj$interest_over_time

df$hits <- as.numeric(ifelse(df$hits == "<1", "0.5", df$hits))

cols <- c("cadetblue3", "cornsilk3", "coral", "lightgoldenrod2", "palegreen3")

ggplot(df, aes(x = as.Date(date), y = hits, fill = keyword)) +
    geom_stream(type = "mirror") + 
    scale_fill_manual(values = cols) + 
    ggtitle("Search Popularity Since January 2023") +
    xlab("Year 2023") +
    ylab("Google Search Hits") +
    theme(
        axis.ticks = element_blank(),
        axis.title = element_text(size = 18, face = "bold"),
        axis.text.y = element_blank(),
        axis.text.x = element_text(vjust = 2, size = 12, face = "bold"),
        panel.background = element_blank(),
        text = element_text(face = "bold", family = "Cairo"),
        plot.title = element_text(size = 22, face = "bold"),
        legend.title = element_text(face = "bold", size = 16, family = "Cairo"),
        plot.caption = element_text(hjust = 2.55, size = 10, face = "italic")
    ) + 
    scale_x_date(date_labels="%b",date_breaks = "1 month") + 
    guides(fill=guide_legend(title="Keyword"))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
