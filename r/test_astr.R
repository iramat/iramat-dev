library(magrittr)
library(ASTR)

# reading an ASTR table directly from a file
test_file <- system.file("extdata", "test_data_input_good.csv", package = "ASTR")
arch <- read_ASTR(test_file, id_column = "Sample", context = 1:7)
knitr::kable(head(arch, 4), format = "pipe")
