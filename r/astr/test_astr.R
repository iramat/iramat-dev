# This test function aims to check the alignment between the CHIPS API and the expected format in ASTR.
# check:
#   - archaeotommy: https://github.com/archaeothommy/ASTR/tree/main/R
#   - IRAMAT: https://github.com/iramat/ASTR/tree/main/R
# test
#   1) column names alignment
#   2) value format

# install.packages("pak")
pak::pak("iramat/ASTR")

library(magrittr)
library(ASTR) # from "iramat/ASTR" (not from "archaeothommy/ASTR") to test ASTR_db_api_connect()

# reading an ASTR table directly from a file
test_file <- system.file("extdata", "test_data_input_good.csv", package = "ASTR")
arch <- read_ASTR(test_file, id_column = "Sample", context = 1:7)
# reading a CHIPS dataset
df_hash <- db_api_connect()

# test
#   1) column names alignment
cat(colnames(arch), sep = "\n")
print("--------")
cat(colnames(df_hash$dataset_adisser17), sep = "\n")

# test
#   2) value format
knitr::kable(head(arch, 1), format = "pipe")
knitr::kable(head(df_hash$dataset_adisser17, 1), format = "pipe")