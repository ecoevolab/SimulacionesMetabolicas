# Install and load ggplot2 if you haven't already
# install.packages("ggplot2")
library(ggplot2)

# Load the built-in 'diamonds' dataset for this example
data(diamonds)

# Create the faceted stacked bar plot
ggplot(data = diamonds, aes(x = cut, fill = clarity)) +
  geom_bar(position = "stack") +
  facet_wrap(~ color) +
  labs(
    title = "Stacked Bar Plot of Diamond Clarity by Cut and Color",
    x = "Cut Quality",
    y = "Count",
    fill = "Clarity"
  ) +
  theme_minimal()


ggplot(data = diamonds, aes(x = cut, fill = clarity)) +
  geom_bar(position = "fill") + # Changes to a proportional stacked bar
  facet_wrap(~ color) +
  labs(
    title = "Proportional Stacked Bar Plot of Diamond Clarity by Cut and Color",
    x = "Cut Quality",
    y = "Proportion", # Updated label
    fill = "Clarity"
  ) +
  theme_minimal()


print(diamonds)
