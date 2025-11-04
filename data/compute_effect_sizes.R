#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  if (!requireNamespace("effsize", quietly = TRUE)) {
    stop("Package 'effsize' is required. Install it with install.packages('effsize').", call. = FALSE)
  }
  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    stop("Package 'jsonlite' is required. Install it with install.packages('jsonlite').", call. = FALSE)
  }
})

# Data available on request
# Anonymized pre/post assessment scores for 2025 cohort
# Mathematics: n = 22 students
# Reading: n = 21 students
# Contact: jay@jayspudvilas.com

math_pre <- NULL  # Placeholder - data available on request
math_post <- NULL

reading_pre <- NULL
reading_post <- NULL

compute_summary <- function(pre, post, domain) {
  n <- length(pre)
  if (length(post) != n) {
    stop(sprintf("Pre/Post length mismatch for %s", domain), call. = FALSE)
  }

  cohen <- effsize::cohen.d(post, pre, hedges.correction = FALSE)

  sd_pooled <- sqrt(((n - 1) * stats::var(pre) + (n - 1) * stats::var(post)) / (2 * n - 2))

  list(
    domain = domain,
    d_value = round(unname(cohen$estimate), 4),
    sd_pooled = round(sd_pooled, 4),
    n = n
  )
}

summaries <- list(
  compute_summary(math_pre, math_post, "Mathematics"),
  compute_summary(reading_pre, reading_post, "Reading")
)

summary_df <- do.call(rbind, lapply(summaries, as.data.frame))
published_df <- data.frame(
  domain = c("Mathematics", "Reading"),
  published_d = c(1.47, 1.18)
)

comparison <- merge(summary_df, published_df, by = "domain")
comparison$delta <- round(comparison$d_value - comparison$published_d, 4)

message("Computed effect sizes:")
print(summary_df, row.names = FALSE)

message("Published dashboard values and deltas:")
print(comparison, row.names = FALSE)

if (any(abs(comparison$delta) > 0.01)) {
  warning("Computed effect sizes differ from published values by more than 0.01.")
} else {
  message("All computed effect sizes align with published dashboard values (±0.01 tolerance).")
}

output_path <- file.path("data", "results.json")
jsonlite::write_json(summaries, output_path, pretty = TRUE, auto_unbox = TRUE)

message(sprintf("Summary JSON written to %s", output_path))
