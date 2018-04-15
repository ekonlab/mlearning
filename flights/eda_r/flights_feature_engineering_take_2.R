# Spy planes feature engineering take two

# Load packages and set working directory
library(rjson)
library(plyr)
library(dplyr)
library(tidyr)
library(ggmap)
library(ggplot2)
library(lubridate)
library(anytime)
library(sp)
library(tmaptools)
library(SpatialEpi)
library(Imap)


setwd("/Users/albertogonzalez/Documents/GitHub/mlearning/flights/eda_r")
list.files()


# Load data (substitute this by the random 500 files from Lucas DB)
input_file =read.csv(file = "flights_output_take_one.csv")
head(input_file)

# Count number of different aircrafts
n_crafts = length(unique(input_file$adshex))
n_crafts

# In this case we are not going to select random 500, but work with the whole population

# Duration and bounding box for all the planes in the population

###############################################################
# ONE FLIGHT CALCULATIONS
###############################################################

# Select that flight
one_flight = input_file %>%
  filter(adshex=="10534350")

str(one_flight)
head(one_flight)

# Duration of that flight
init = min(one_flight$timestamp)
init = anytime(init)
end = max(one_flight$timestamp)
end = anytime(end)
dura = difftime(end,init,units="mins")
dura

# Bounding box of that flight
xy <- one_flight[,c(3,4)]
min_coord = head(xy,1)
max_coord = tail(xy,1)
area_meters = gdist(min_coord$lng,min_coord$lat,max_coord$lng,max_coord$lat, units = "m", a = 6378137.0, b = 6356752.3142, verbose = FALSE)
area_km2 = area_meters / 1000
area_km2

# Calculate steer: change in compass from previous transponder
# Calculated over track
head(one_flight)
steer = diff(one_flight$track)
steer = as.data.frame(steer)
# Add first zero index to steer
steer_2 = rbind(0,steer)

# Add one flight calculations
one_flight$duration = dura
one_flight$box_km2 = area_km2
one_flight$steer = steer_2
one_flight


###############################################################
# ONE FLIGHT CALCULATIONS: CONVERT INTO A FUNCTION
###############################################################

foo = function(flight_df){
  
  # Duration of that flight
  init = min(flight_df$timestamp)
  init = anytime(init)
  end = max(flight_df$timestamp)
  end = anytime(end)
  dura = difftime(end,init,units="mins")
  flight_df$duration = dura
  flight_df
  
  # Bounding box of that flight
  xy <- flight_df[,c(3,4)]
  min_coord = head(xy,1)
  max_coord = tail(xy,1)
  area_meters = gdist(min_coord$lng,min_coord$lat,max_coord$lng,max_coord$lat, units = "m", a = 6378137.0, b = 6356752.3142, verbose = FALSE)
  area_km2 = area_meters / 1000
  flight_df$box_km2 = area_km2
  
  # Calculate steer: change in compass from previous transponder
  steer = diff(flight_df$track)
  steer = as.data.frame(steer)
  steer_2 = rbind(0,steer)
  flight_df$steer = steer_2
  flight_df
  
}

# Test the function with one flight
# Get flights ids
flights_rows = as.data.frame(table(input_file$adshex))
head(flights_rows)

one_flight = input_file %>%
  filter(adshex=="10534350")

t = foo(one_flight)
t

# Run the function for all flights
df2 = ddply(input_file, ~ adshex, foo)
















