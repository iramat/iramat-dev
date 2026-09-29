y <- c(
  rep(0,10), rep(1,20), # première pièce
  rep(0,15), rep(1,15)  # seconde pièce
)
y

Id <- rep(c('', 'B'), each= 30)
Id

# empaquetage des données à destination de JAGS
dataList <- list(
  y=y,
  N=length(y)
)
dataList

# lecture du modèle par JAGS
library(rjags)
jagsModel <- jags.model(
  file = "C:\\Users\\TH282424\\Rprojects\\iramat-dev\\doc\\formations\\bayes\\model08_ok.R", # le modèle prior
  data = dataList, # liste de données
  n.chains=3, # nb de chaines
  n.adapt=500
)

# burnin (préchauffage)
update( jagsModel, n.iter=500)

# générer la #walk (CM) et l'enregistrer
codaSamples <- coda.samples(
  jagsModel, # modèle JAGS
  # nom des variables à enregistrer
  variable.names=c('theta'),
  n.iter=333 # nb itérations
)

plot(codaSamples) 
# resulats: trace de theta (chaines mélangées) et density of theta
autocorr.plot(codaSamples)
# se déduit -> OKey
coda::gelman.plot(codaSamples)
# on voit les chaines entremellée = OKey
densplot(codaSamples)
# density of theta


coda::effectiveSize(codaSamples)
# nb de pas effectifs/utiles (à indiquer dans les publis)

# remotes::install_github("Julien-Bousquet/BayesCompanion")
library(BayesCompanion)
diagMCMC(codaSamples)

M <- as.matrix(codaSamples)
BayesCompanion::plotPost(M)

# quelles est la probabilité a posteriori que le taux theta du lancé de pièce soit entre 40% et 60%
mean(M > .4 & M < .6)
