# nolint start
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
#| label: fig-primary
#| fig-cap: "Google Trends Data From January of the Top Candidates for the Republican Party. "
#| warning: false
#| echo: false

library(gtrendsR)
library(ggplot2)
library(ggstream)
library(showtext)
font_add_google("Cairo", family = "Cairo")
showtext_auto()

obj <- gtrends(
    keyword = c("Donald Trump", "Ron DeSantis", "Mike Pence", "Nikki Haley", "Tim Scott"),
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
#| label: fig-secondary
#| fig-cap: "Aggregated Google Trends data of popular GOP Primary candidates in the last 10 days of available Google Search data. It is usually delayed by three days."
#| warning: false
#| echo: false

df$date <- as.Date(df$date)
df <- df[df$date > (max(df$date)-10),]
row.names(df) <- NULL

df <- data.frame(
    hits = tapply(df$hits, df$keyword, sum),
    candidate = names(tapply(df$hits, df$keyword, sum))
)

df$hits <- round(df$hits/sum(df$hits)*100,1)
df$label <- paste0(df$hits, "%")
df$color <- c("cadetblue3", "cornsilk3", "coral", "lightgoldenrod2", "palegreen3")

colors <- df$color[order(df$hits)]

df |> 
    ggplot() + 
    geom_bar(aes(x = hits, y = reorder(candidate, hits)), stat = "identity", width = 0.8, fill = df$color) +
    geom_text(aes(x = hits, y = reorder(candidate, hits), label = label), hjust = -.08, family = "Cairo", fontface = "bold", size = 5) + 
    ggtitle("Share of Web Searches in Last 10 Days") +
    xlab("Percentage of Hits (%)") +
    ylab("Candidate") +
    xlim(0,100) +
    theme(
        axis.ticks = element_blank(),
        axis.title = element_text(size = 18, face = "bold"),
        axis.text.y = element_text(face = "bold", size = 16, family = "Cairo", color = colors, margin = margin(r = -15)),
        axis.text.x = element_text(vjust = 2, size = 12, face = "bold"),
        panel.background = element_blank(),
        text = element_text(face = "bold", family = "Cairo"),
        plot.title = element_text(size = 22, face = "bold"),
        legend.title = element_text(face = "bold", size = 16, family = "Cairo"),
        plot.caption = element_text(hjust = 2.55, size = 12, face = "italic")
    )

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
