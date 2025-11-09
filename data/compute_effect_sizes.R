#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    stop("Package 'jsonlite' is required. Install it with install.packages('jsonlite').", call. = FALSE)
  }
})

# Data available on request
# Anonymized pre/post assessment scores for 2025 cohort
# Mathematics: n = 22 students
# Reading: n = 21 students
# Contact: jay@jayspudvilas.com

math_pre <- c(
  136.1, 124.8, 119.5, 120.4, 110.8, 121.2, 117.8, 120.4, 113.9, 115.7,
  91.5, 114.9, 116.3, 116.2, 114.0, 109.8, 113.4, 96.8, 107.5, 96.6,
  96.6, 104.3,
  96.8   # Student N+1 (new)
)
math_post <- c(
  155.5, 136.2, 135.5, 127.9, 127.3, 127.1, 126.9, 125.5, 124.5, 124.3,
  124.3, 124.1, 123.4, 122.9, 122.9, 122.5, 121.2, 120.2, 116.5, 110.2,
  104.7, 104.3,
  107.0  # Student N+1 (new)
)

reading_pre <- c(
  115.5, 129.5, 125.1, 116.7, 120.7, 128.9, 119.4, 111.1, 124.1, 118.9,
  120.9, 116.9, 111.9, 86.6, 115.5, 108.2, 88.6, 101.9, 92.6, 102.3, 99.1
)
reading_post <- c(
  138.3, 135.5, 134.7, 131.7, 131.4, 129.8, 128.9, 127.1, 125.1, 124.3,
  123.9, 118.8, 118.5, 118.5, 116.8, 114.8, 111.6, 110.2, 107.2, 105.1, 103.5
)

compute_summary <- function(pre, post, domain) {
  n <- length(pre)
  if (length(post) != n) {
    stop(sprintf("Pre/Post length mismatch for %s", domain), call. = FALSE)
  }

  gains <- post - pre
  mean_pre <- mean(pre)
  mean_post <- mean(post)
  mean_gain <- mean(gains)
  sd_gain <- stats::sd(gains)

  d_value <- mean_gain / sd_gain
  j_corr <- 1 - (3 / (4 * n - 9))
  g_value <- d_value * j_corr

  list(
    domain = domain,
    n = n,
    mean_pre = round(mean_pre, 2),
    mean_post = round(mean_post, 2),
    mean_gain = round(mean_gain, 2),
    sd_gain = round(sd_gain, 2),
    d = round(d_value, 2),
    g = round(g_value, 2)
  )
}

summaries <- list(
  compute_summary(math_pre, math_post, "Mathematics"),
  compute_summary(reading_pre, reading_post, "Reading")
)

output_path <- file.path("data", "results.json")
jsonlite::write_json(summaries, output_path, pretty = TRUE, auto_unbox = TRUE)

message("Computed effect sizes:")
print(do.call(rbind, lapply(summaries, as.data.frame)), row.names = FALSE)

message(sprintf("Summary JSON written to %s", output_path))
