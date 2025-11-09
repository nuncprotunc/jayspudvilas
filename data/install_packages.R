#!/usr/bin/env Rscript
packages <- c("effsize", "jsonlite")
repos <- "https://cloud.r-project.org"

# Ensure a writable user library exists and is on .libPaths()
userlib <- Sys.getenv("R_LIBS_USER")
if (nzchar(userlib) == FALSE) {
  # Construct default user library path on Windows
  rmaj <- R.Version()$major
  rmin <- strsplit(R.Version()$minor, "\\.")[[1]][1]
  userlib <- file.path(Sys.getenv("USERPROFILE"), "AppData", "Local", "R", "win-library", paste0(rmaj, ".", rmin))
}
if (!dir.exists(userlib)) {
  dir.create(userlib, recursive = TRUE, showWarnings = FALSE)
}
.libPaths(c(userlib, .libPaths()))

for (pkg in packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, repos = repos, lib = userlib)
  }
}
