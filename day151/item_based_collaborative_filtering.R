## Books Rating Recommendation System
## From Jericho Siahaya

### Import dataset
ratingBuku <- read.csv(file="BX-Book-Ratings.csv", sep=";", header=TRUE)
namaBuku <- read.csv(file="BX-Books.csv", sep=";", header=TRUE)

### Library
library(readr)
library(tidyverse)
library(dplyr)
library(knitr)

### Data manipulation
all_data <- ratingBuku %>%
  group_by(ISBN, User.ID) %>%
  summarise(rating = sum(Book.Rating, na.rm = TRUE)) %>%
  inner_join(namaBuku)

top_500_books <- all_data %>%
  group_by(ISBN, Book.Title, Book.Author) %>%
  summarise(sum_rating = sum(rating)) %>%
  ungroup() %>%
  top_n(500, sum_rating) %>%
  distinct(ISBN)

all_data_top_50k <- all_data %>%
  inner_join(top_500_books)

top_50k_wide <- all_data_top_50k %>%
  ungroup() %>%
  distinct(User.ID, ISBN, rating) %>%
  spread(ISBN, rating, fill=0)

ratings <- as.matrix((top_50k_wide[,-1]))

### Cosine formula
cosine_sim <- function(a, b) {crossprod(a,b)/sqrt(crossprod(a) * crossprod(b))}

### Calculation
calcSim <- function(bookID = top_500_books,
                    rating_mat = ratings,
                    books = namaBuku,
                    return_n = 5) {
  book_col_index <- which(colnames(ratings) == bookID)
  cos_sims <- apply(rating_mat, 2, FUN = function(y)
  cosine_sim(rating_mat[,book_col_index], y))
  
  # Output with knitr::kable
  data_frame(ISBN = names(cos_sims), cos_sim = cos_sims) %>%
    filter(ISBN != bookID) %>%
    inner_join(books) %>%
    arrange(desc(cos_sim)) %>%
    top_n(return_n, cos_sim) %>%
    select(ISBN, Book.Title, Book.Author, cos_sim)
}

#########
# Tes rekomendasi pertama
Fahrenheit451 <- '0345342968'
TesRekomendasiPertama <- knitr::kable(calcSim(Fahrenheit451))
TesRekomendasiPertama

# Tes rekomendasi kedua
HarryPotter1 <- '059035342X'
TesRekomendasiKedua <- knitr::kable(calcSim(HarryPotter1))
TesRekomendasiKedua