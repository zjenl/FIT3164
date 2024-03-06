setwd("G:/FIT3163")
library(data.table)
library(dplyr)
library(tidyr)
library(ggplot2)

# load data
calendar <- read.csv("calendar.csv")
sell_prices <- read.csv("sell_prices.csv")
sales_data <- read.csv("sales_train_evaluation.csv")

# Add extra columns to calendar where each column represents a unique event type
# Extract unique event types from calendar
unique_event_types <- unique(c(calendar$event_type_1, calendar$event_type_2))
unique_event_types <- unique_event_types[nzchar(unique_event_types)]

# Create a loop to add columns for each unique event type
for (event_type in unique_event_types) 
{
  # Create a new column for the event type with initial value 0
  calendar$event_type <- 0
  
  # Update the new column based on the presence of the event type
  calendar$event_type[calendar$event_type_1 == event_type] <- 1
  
  calendar$event_type[calendar$event_type_2 == event_type] <- 
    calendar$event_type[calendar$event_type_2 == event_type] + 1
  
  # Change column name
  colnames(calendar)[ncol(calendar)] <- event_type
}

# Count total missing values in the sales_data and the sell_prices data frame
sum(is.na(sales_data))
sum(is.na(sell_prices))

# Merge calendar with sell_prices based on the week column
sell_prices <- sell_prices %>%
  left_join(select(calendar, wm_yr_wk, d, Sporting, Cultural, National, Religious), 
            by = c("wm_yr_wk" = "wm_yr_wk"), relationship = "many-to-many")

# Split the sales data frame to multiple ones based on categories
sales_by_dept <- split(sales_data, sales_data$dept_id)

# Split the price data frame based on item_id prefix
split_data <- function(df) 
{
  prefix <- gsub("_[0-9]+$", "", df$item_id)  # Extract the prefix
  split(df, prefix)  # Split the data frame
}
price_by_dept <- split_data(sell_prices)

# Extract unique departments 
unique_depts <- unique(sales_data$dept_id)

# Make specific category data frames
for (dept in unique_depts) 
{
  # Filter the sales_by_dept data frame for the current category
  dept_sales <- sales_by_dept[[dept]]
  assign(paste0(dept, "_sale"), dept_sales)
  
  # Filter the price_by_dept data frame for the current category
  dept_price <- price_by_dept[[dept]]
  assign(paste0(dept, "_price"), dept_price)
}
rm(dept_sales)
rm(dept_price)
rm(price_by_dept)
rm(sales_by_dept)

# Pivot the prices data to have rows indicating the days
FOODS_1_sale <- FOODS_1_sale %>%
  pivot_longer(cols = starts_with("d_"), 
               names_to = "d", 
               values_to = "sales")

# Merge price with sale
FOODS_1_sale <- merge(FOODS_1_sale, FOODS_1_price, 
                   by = c("item_id", "store_id", "d"))

# Extract the numeric part of the "d" column and convert it to numeric
FOODS_1_sale$d <- as.numeric(sub("d_", "", FOODS_1_sale$d))
FOODS_1_sale$item_id <- as.numeric(sub("FOODS_1_", "", FOODS_1_sale$item_id))

FOODS_1_sale <- subset(FOODS_1_sale, select = -c(id, dept_id, cat_id))
fwrite(FOODS_1_sale, "G:/FIT3163/FOODS_1_sale.csv", row.names=FALSE)
rm(FOODS_1_price)
gc()

# Pivot the prices data to have rows indicating the days
FOODS_2_sale <- FOODS_2_sale %>%
  pivot_longer(cols = starts_with("d_"), 
               names_to = "d", 
               values_to = "sales")

# Merge price with sale
FOODS_2_sale <- merge(FOODS_2_sale, FOODS_2_price, 
                      by = c("item_id", "store_id", "d"))

# Extract the numeric part of the columns and convert it to numeric
FOODS_2_sale$d <- as.numeric(sub("d_", "", FOODS_2_sale$d))
FOODS_2_sale$item_id <- as.numeric(sub("FOODS_2_", "", FOODS_2_sale$item_id))

FOODS_2_sale <- subset(FOODS_2_sale, select = -c(id, dept_id, cat_id))
fwrite(FOODS_2_sale, "G:/FIT3163/FOODS_2_sale.csv", row.names=FALSE)
rm(FOODS_2_price)
gc()

# Pivot the prices data to have rows indicating the days
FOODS_3_sale <- FOODS_3_sale %>%
  pivot_longer(cols = starts_with("d_"), 
               names_to = "d", 
               values_to = "sales")

# Merge price with sale
FOODS_3_sale <- merge(FOODS_3_sale, FOODS_3_price, 
                      by = c("item_id", "store_id", "d"))

# Extract the numeric part of the "day_id" column and convert it to numeric
FOODS_3_sale$d <- as.numeric(sub("d_", "", FOODS_3_sale$d))
FOODS_3_sale$item_id <- as.numeric(sub("FOODS_3_", "", FOODS_3_sale$item_id))

FOODS_3_sale <- subset(FOODS_3_sale, select = -c(id, dept_id, cat_id))
fwrite(FOODS_3_sale, "G:/FIT3163/FOODS_3_sale.csv", row.names=FALSE)
rm(FOODS_3_price)
gc()

# Pivot the prices data to have rows indicating the days
HOBBIES_1_sale <- HOBBIES_1_sale %>%
  pivot_longer(cols = starts_with("d_"), 
               names_to = "d", 
               values_to = "sales")

# Merge price with sale
HOBBIES_1_sale <- merge(HOBBIES_1_sale, HOBBIES_1_price, 
                        by = c("item_id", "store_id", "d"))

# Extract the numeric part of the "day_id" column and convert it to numeric
HOBBIES_1_sale$d <- as.numeric(sub("d_", "", HOBBIES_1_sale$d))
HOBBIES_1_sale$item_id <- as.numeric(sub("HOBBIES_1_", "", HOBBIES_1_sale$item_id))

HOBBIES_1_sale <- subset(HOBBIES_1_sale, select = -c(id, dept_id, cat_id))
fwrite(HOBBIES_1_sale, "G:/FIT3163/HOBBIES_1_sale.csv", row.names=FALSE)
rm(HOBBIES_1_price)
gc()

# Pivot the prices data to have rows indicating the days
HOBBIES_2_sale <- HOBBIES_2_sale %>%
  pivot_longer(cols = starts_with("d_"), 
               names_to = "d", 
               values_to = "sales")

# Merge price with sale
HOBBIES_2_sale <- merge(HOBBIES_2_sale, HOBBIES_2_price, 
                        by = c("item_id", "store_id", "d"))

# Extract the numeric part of the "day_id" column and convert it to numeric
HOBBIES_2_sale$d <- as.numeric(sub("d_", "", HOBBIES_2_sale$d))
HOBBIES_2_sale$item_id <- as.numeric(sub("HOBBIES_2_", "", HOBBIES_2_sale$item_id))

HOBBIES_2_sale <- subset(HOBBIES_2_sale, select = -c(id, dept_id, cat_id))
fwrite(HOBBIES_2_sale, "G:/FIT3163/HOBBIES_2_sale.csv", row.names=FALSE)
rm(HOBBIES_2_price)
gc()

# Pivot the prices data to have rows indicating the days
HOUSEHOLD_1_sale <- HOUSEHOLD_1_sale %>%
  pivot_longer(cols = starts_with("d_"), 
               names_to = "d", 
               values_to = "sales")

# Merge price with sale
HOUSEHOLD_1_sale <- merge(HOUSEHOLD_1_sale, HOUSEHOLD_1_price, 
                          by = c("item_id", "store_id", "d"))

# Extract the numeric part of the column and convert it to numeric
HOUSEHOLD_1_sale$d <- as.numeric(sub("d_", "", HOUSEHOLD_1_sale$d))
HOUSEHOLD_1_sale$item_id <- as.numeric(sub("HOUSEHOLD_1_", "", 
                                           HOUSEHOLD_1_sale$item_id))

HOUSEHOLD_1_sale <- subset(HOUSEHOLD_1_sale, select = -c(id, dept_id, cat_id))
fwrite(HOUSEHOLD_1_sale, "G:/FIT3163/HOUSEHOLD_1_sale.csv", row.names=FALSE)
rm(HOUSEHOLD_1_price)
gc()

# Pivot the prices data to have rows indicating the days
HOUSEHOLD_2_sale <- HOUSEHOLD_2_sale %>%
  pivot_longer(cols = starts_with("d_"), 
               names_to = "d", 
               values_to = "sales")

# Merge price with sale
HOUSEHOLD_2_sale <- merge(HOUSEHOLD_2_sale, HOUSEHOLD_2_price, 
                          by = c("item_id", "store_id", "d"))

# Extract the numeric part of the "day_id" column and convert it to numeric
HOUSEHOLD_2_sale$d <- as.numeric(sub("d_", "", HOUSEHOLD_2_sale$d))
HOUSEHOLD_2_sale$item_id <- as.numeric(sub("HOUSEHOLD_2_", "", 
                                           HOUSEHOLD_2_sale$item_id))

HOUSEHOLD_2_sale <- subset(HOUSEHOLD_2_sale, select = -c(id, dept_id, cat_id))
fwrite(HOUSEHOLD_2_sale, "G:/FIT3163/HOUSEHOLD_2_sale.csv", row.names=FALSE)
rm(HOUSEHOLD_2_price)
gc()

summary(FOODS_1_sale$sales)
summary(FOODS_1_sale$sell_price)

summary(FOODS_2_sale$sales)
summary(FOODS_2_sale$sell_price)
summary(FOODS_3_sale$sales)
summary(FOODS_3_sale$sell_price)
summary(HOBBIES_1_sale$sales)
summary(HOBBIES_1_sale$sell_price)
summary(HOBBIES_2_sale$sales)
summary(HOBBIES_2_sale$sell_price)
summary(HOUSEHOLD_1_sale$sales)
summary(HOUSEHOLD_1_sale$sell_price)
summary(HOUSEHOLD_2_sale$sales)
summary(HOUSEHOLD_2_sale$sell_price)