library(ggplot2)
library(Hmisc)

solar_data <- read_excel("solar_data.xlsx")
ggplot(solar_data, aes(x = Temp, y = SolarEnergy)) + geom_point()

ggplot(data = solar_data, mapping = aes(x = Site, y = Temp)) + stat_summary(fun.data = mean_sdl, geom = "bar") 

ggplot(data = solar_data, mapping = aes(x = Site, y = Rain)) + stat_summary(fun.data = mean_sdl, geom = "bar") 

ggplot(data = solar_data, mapping = aes(x = Site, y = Humidity)) + stat_summary(fun.data = mean_sdl, geom = "bar") 

ggplot(data = solar_data, mapping = aes(x = Site, y = SolarEnergy)) + stat_summary(fun.data = mean_sdl, geom = "bar") 
