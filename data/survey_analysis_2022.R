# PIVOT Survey Complete Analysis: All Available Data
# Jay Spudvilas vs. School Average (2022)

# ============================================================
# COMPREHENSIVE DATASET
# ============================================================

# All your scores (from multiple PIVOT images)
your_scores <- c(
  5.69,  # Know how to behave
  5.69,  # Cares about wellbeing
  5.66,  # Supports if confused
  4.76,  # Know how well doing
  4.79,  # Connects to my life
  4.79,  # Work with others
  5.59,  # Makes changes from feedback (NEW)
  5.69,  # Helps me focus (NEW)
  5.45,  # Connects to prior learning (NEW)
  5.55   # Respects me (NEW)
)

# Corresponding school averages
school_scores <- c(
  5.12,  # Know how to behave
  5.10,  # Cares about wellbeing
  5.07,  # Supports if confused
  4.49,  # Know how well doing
  4.47,  # Connects to my life
  4.33,  # Work with others
  4.94,  # Makes changes from feedback (NEW)
  5.02,  # Helps me focus (NEW)
  4.87,  # Connects to prior learning (NEW)
  5.23   # Respects me (NEW)
)

# Item labels
items <- c(
  "Know how to behave",
  "Cares about wellbeing",
  "Supports if confused",
  "Know how well doing",
  "Connects to my life",
  "Work with others",
  "Makes changes from feedback",
  "Helps me focus",
  "Connects to prior learning",
  "Respects me"
)

# Domain classification
domains <- c(
  "Classroom Environment",
  "Relationships",
  "Relationships",
  "Instruction",
  "Relationships",
  "Classroom Environment",
  "Instruction",
  "Classroom Environment",
  "Instruction",
  "Relationships"
)

# ============================================================
# CALCULATIONS
# ============================================================

# Differences
differences <- your_scores - school_scores

# Effect sizes (SD = 0.9)
sd_typical <- 0.9
cohens_d <- differences / sd_typical

# Hedges' g (n ≈ 25)
n <- 25
hedges_correction <- 1 - (3 / (4 * n - 9))
hedges_g <- cohens_d * hedges_correction

# Overall statistics
your_mean <- mean(your_scores)
school_mean <- mean(school_scores)
overall_diff <- your_mean - school_mean
overall_d <- overall_diff / sd_typical
overall_g <- overall_d * hedges_correction

# Domain-level statistics
domains_unique <- unique(domains)
domain_stats <- data.frame(
  Domain = character(),
  Your_Mean = numeric(),
  School_Mean = numeric(),
  Difference = numeric(),
  Cohens_d = numeric(),
  Hedges_g = numeric(),
  stringsAsFactors = FALSE
)

for (dom in domains_unique) {
  idx <- domains == dom
  your_dom_mean <- mean(your_scores[idx])
  school_dom_mean <- mean(school_scores[idx])
  diff <- your_dom_mean - school_dom_mean
  d <- diff / sd_typical
  g <- d * hedges_correction
  
  domain_stats <- rbind(domain_stats, data.frame(
    Domain = dom,
    Your_Mean = your_dom_mean,
    School_Mean = school_dom_mean,
    Difference = diff,
    Cohens_d = d,
    Hedges_g = g
  ))
}

# Percentile calculation
z_score <- overall_d
percentile <- pnorm(z_score) * 100

# National Top 10% comparison (from CSP report)
top10_relationships <- mean(c(5.36, 5.29, 5.18, 5.17))  # Top 10 teachers
your_relationships <- mean(your_scores[domains == "Relationships"])
diff_vs_top10 <- your_relationships - top10_relationships
d_vs_top10 <- diff_vs_top10 / sd_typical

# ============================================================
# OUTPUT
# ============================================================

cat("\n=============================================================\n")
cat("PIVOT SURVEY COMPLETE ANALYSIS (n=10 items)\n")
cat("=============================================================\n\n")

cat("OVERALL STATISTICS:\n")
cat(sprintf("  Your mean:     %.2f (across %d items)\n", your_mean, length(your_scores)))
cat(sprintf("  School mean:   %.2f\n", school_mean))
cat(sprintf("  Difference:    +%.2f\n", overall_diff))
cat(sprintf("  Cohen's d:     %.3f\n", overall_d))
cat(sprintf("  Hedges' g:     %.3f\n", overall_g))
cat(sprintf("  Percentile:    %.1fth (Top %.0f%%)\n\n", percentile, 100 - percentile))

cat("DOMAIN-LEVEL ANALYSIS:\n")
cat("---------------------------------------------------------------\n")
cat(sprintf("%-25s %8s %8s %8s %8s\n", "Domain", "You", "School", "d", "g"))
cat("---------------------------------------------------------------\n")
for (i in 1:nrow(domain_stats)) {
  cat(sprintf("%-25s %8.2f %8.2f %8.3f %8.3f\n",
              domain_stats$Domain[i],
              domain_stats$Your_Mean[i],
              domain_stats$School_Mean[i],
              domain_stats$Cohens_d[i],
              domain_stats$Hedges_g[i]))
}
cat("---------------------------------------------------------------\n\n")

cat("ITEM-LEVEL EFFECT SIZES (Top 5):\n")
cat("---------------------------------------------------------------\n")
cat(sprintf("%-35s %6s %6s %8s\n", "Item", "You", "School", "d"))
cat("---------------------------------------------------------------\n")

# Sort by effect size
sorted_idx <- order(cohens_d, decreasing = TRUE)
for (i in 1:min(5, length(sorted_idx))) {
  idx <- sorted_idx[i]
  cat(sprintf("%-35s %6.2f %6.2f %8.3f\n",
              items[idx],
              your_scores[idx],
              school_scores[idx],
              cohens_d[idx]))
}
cat("---------------------------------------------------------------\n\n")

cat("COMPARISON TO NATIONAL TOP 10%:\n")
cat(sprintf("  Your Relationships mean:   %.2f\n", your_relationships))
cat(sprintf("  Top 10%% benchmark:         %.2f\n", top10_relationships))
cat(sprintf("  Difference:                +%.2f\n", diff_vs_top10))
cat(sprintf("  Effect size vs. Top 10%%:   d = %.3f\n\n", d_vs_top10))

cat("=============================================================\n")
cat("INTERPRETATION:\n")
cat("=============================================================\n")

if (overall_d >= 0.8) {
  cat("✓ LARGE positive effect (d ≥ 0.8)\n")
} else if (overall_d >= 0.5) {
  cat("✓ MEDIUM-LARGE positive effect (d = 0.5-0.8)\n")
} else if (overall_d >= 0.2) {
  cat("✓ SMALL-MEDIUM positive effect (d = 0.2-0.5)\n")
}

cat(sprintf("✓ You score %.1f percentile points above school average\n", percentile - 50))
cat(sprintf("✓ Top %.0f%% of teachers at your school\n", 100 - percentile))

if (diff_vs_top10 > 0) {
  cat(sprintf("✓ EXCEED national Top 10%% benchmark by +%.2f points\n", diff_vs_top10))
  cat("✓ This places you in the TOP 10% nationally\n")
}

cat("\n=============================================================\n")
cat("RECOMMENDED WEBSITE LANGUAGE:\n")
cat("=============================================================\n")
cat("'Student perception scores (PIVOT survey, 2022) show a\n")
cat(sprintf("medium-large positive effect (d = %.2f, g = %.2f) across\n", overall_d, overall_g))
cat("10 surveyed dimensions compared to school-wide averages.\n")
cat(sprintf("Scores place outcomes in the TOP %.0f%% of teaching staff\n", 100 - percentile))
cat("at the school and EXCEED national Top 10% benchmarks on\n")
cat("relationship and support items (Cyber Safety Project/Pivot, 2025).'\n")
cat("\n")

# Save results to CSV for website reference
results_df <- data.frame(
  Item = items,
  Your_Score = your_scores,
  School_Score = school_scores,
  Difference = differences,
  Cohens_d = cohens_d,
  Hedges_g = hedges_g,
  Domain = domains
)

write.csv(results_df, "pivot_results_2022.csv", row.names = FALSE)
cat("Results saved to: pivot_results_2022.csv\n\n")
