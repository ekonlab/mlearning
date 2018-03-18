# Identify segments by flight
setwd("/Users/albertogonzalez/Downloads/")

# libraries
library(dplyr)
library(rjson)

# Load suspects
input_file = fromJSON(file="suspects.json")

# Convert to csv and export
json = do.call("rbind",input_file)
write.csv(json,file='suspects.csv', row.names=FALSE)



df = do.call("rbind.fill", lapply(input_file, as.data.frame))
str(df)




