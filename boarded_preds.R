library(grf)
library(readr)


data <- read_csv('data.csv')
data <- na.omit(data[,c('oasis_resprate', 'oasis_meanbp', 'oasis_heartrate', 'oasis_urineoutput', 'hospital_expire_flag','days_survived', 'icustay_boarder_initial', 'remaining_beds')])
X <- as.matrix( data[,c('oasis_resprate', 'oasis_meanbp', 'oasis_heartrate', 'oasis_urineoutput')])
Y <-as.matrix( data[,c('hospital_expire_flag')])
W <- as.matrix( data[,c('icustay_boarder_initial')])

tau.forest = causal_forest(X, Y, W, num.trees = 100, tune.parameters=TRUE)
data['changed_hospital_expire_flag'] <- data.frame(predict(tau.forest, X)[1])
hist(data$hospital_expire_flag)
hist(data$changed_hospital_expire_flag)

write_csv(data,'data_results.csv')
