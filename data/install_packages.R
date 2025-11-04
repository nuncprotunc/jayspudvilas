#!/usr/bin/env Rscript
packages <- c("effsize", "jsonlite")
repos <- "https://cloud.r-project.org"
for (pkg in packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, repos = repos)
  }
}
