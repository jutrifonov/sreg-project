---
title: R guide and reference
r_reference: true
description: Complete R documentation for sreg — data preparation, estimator arguments, supported designs, inference, reporting, plotting, and simulation.
---

<p class="eyebrow">R documentation</p>

# R guide and reference

<p class="lead">A detailed guide to specifying the experimental design, estimating treatment effects, conducting inference, and reporting results with sreg in R.</p>

Start with the [introductory walkthrough](get-started.md?lang=r) for a first analysis. This guide covers the functionality documented in the [R README](https://github.com/jutrifonov/sreg), organized around an empirical workflow. The [Peru application](empirical-example.md?lang=r) provides a complete example using experimental data.

## Installation and help {#install}

```r
install.packages("sreg")
library(sreg)
```

For the development version:

```r
install.packages("remotes")
remotes::install_github("jutrifonov/sreg")
```

CRAN installs required dependencies automatically. The README lists `dplyr`, `tidyr`, `extraDistr`, and `rlang` as dependencies; optional tools include `haven`, `knitr`, `rmarkdown`, and `testthat`. You do not need to load these packages to call `sreg()` directly. Record the version used in an analysis and consult its installed help:

```r
packageVersion("sreg")
help(sreg)
help(sreg.rgen)
help("plot.sreg")
citation("sreg")
sessionInfo()
```

The examples below follow the 2.1.0 README. The [release history](https://github.com/jutrifonov/sreg/blob/main/NEWS.md) records changes between versions.

## Preparing experimental data {#data}

Supply one row per observed individual. `Y`, `D`, `S`, and the rows of `X` must refer to the same observations in the same order. Code the control group as `0` and active treatments as `1, 2, …`. Each treatment effect is measured relative to control.

For individual assignment, omit `G.id`. For cluster assignment, repeat the cluster identifier on every individual record belonging to that cluster. Treatment and stratum membership are shared within a cluster. `Ng` records the size of the cluster represented by those observations; repeat that value across its records.

| Outcome `Y` | Stratum `S` | Treatment `D` | Cluster `G.id` | Size `Ng` | Baseline covariate |
| --- | --- | --- | --- | --- | --- |
| 8.2 | 1 | 0 | 1 | 10 | 12 |
| 9.1 | 1 | 0 | 1 | 10 | 12 |
| 10.4 | 1 | 1 | 2 | 30 | 14 |
| 11.0 | 1 | 1 | 2 | 30 | 14 |

These illustrative rows show the organization of cluster data, not a complete estimation sample. If `Ng` is omitted, sreg uses the number of observed records in each cluster. When only a subset of a cluster is observed, distinguish that observed count from the represented cluster size.

Inspect treatment allocation before estimation:

```r
# dat is your analysis dataset
head(dat)
table(stratum = dat$S, treatment = dat$D)
```

For cluster assignment, inspect allocation at the level of clusters:

```r
assignment <- unique(dat[c("G.id", "S", "D")])
table(stratum = assignment$S, treatment = assignment$D)
```

Use baseline covariates for adjustment. In cluster experiments, sreg aggregates individual-varying covariates to cluster means. It does not use within-cluster individual variation directly in the adjustment regression.

## Estimator arguments {#arguments}

```r
sreg(Y, S = NULL, D, G.id = NULL, Ng = NULL, X = NULL,
     HC1 = TRUE, small.strata = FALSE, k = NULL)
```

| Argument | Meaning and default |
| --- | --- |
| `Y` | Numeric observed outcomes, supplied as a vector or a single-column matrix, data frame, or tibble. |
| `S` | Numeric randomization-stratum indicators. `NULL` specifies no stratification. |
| `D` | Numeric treatment indicators; `0` is control and positive consecutive integers identify active treatments. |
| `G.id` | Numeric cluster identifiers. `NULL` specifies individual-level treatment assignment. |
| `Ng` | Represented cluster sizes. With `NULL`, sizes are calculated from available observations in each cluster. |
| `X` | Covariate matrix, data frame, or tibble, with one row per observation. `NULL` selects the unadjusted estimator. |
| `HC1` | Apply the finite-sample variance correction (`TRUE` by default). |
| `small.strata` | Select small-strata or mixed-design estimation and inference (`FALSE` by default). |
| `k` | Number of assignment units per small stratum. For cluster assignment, count clusters. Omit for a uniform small-strata design; supply for mixed designs with 4-tuples or larger. |

Stratum, treatment, cluster, and cluster-size inputs may also be supplied in the numeric vector or single-column formats accepted for outcomes. `X` can contain multiple columns.

sreg applies point and variance estimators corresponding to these design inputs. Including covariates selects the covariate-adjusted counterpart. Setting `small.strata = TRUE` changes the estimation procedure; it is not a generic correction for a small total sample.

## Worked design specifications {#designs}

The following examples generate complete datasets so that each specification can be run independently after `library(sreg)`. In an empirical analysis, replace the generated inputs with the corresponding variables in your data.

### Large strata and multiple treatments {#large-strata}

```r
set.seed(42)
large_data <- sreg.rgen(
  n = 1000, tau.vec = c(-0.3, 0.2),
  n.strata = 4, cluster = FALSE
)
large_fit <- sreg(
  Y = large_data$Y, S = large_data$S, D = large_data$D,
  X = large_data[c("x_1", "x_2")]
)
print(large_fit)
```

With R sreg 2.1.0 and the seed above, the estimates are:

| Contrast | Estimate | Standard error | 95% confidence interval |
| --- | --- | --- | --- |
| Treatment 1 − control | −0.29036 | 0.07901 | [−0.44523, −0.13550] |
| Treatment 2 − control | 0.18691 | 0.08047 | [0.02920, 0.34463] |

There are two active treatments and a control group. sreg reports treatment 1 versus control and treatment 2 versus control. Omit `X` to obtain unadjusted estimates; omit `S` only when the experiment was not stratified.

### Matched pairs {#pairs}

```r
set.seed(42)
pair_data <- sreg.rgen(
  n = 100, tau.vec = 1.2, cluster = FALSE,
  small.strata = TRUE, k = 2, treat.sizes = c(1, 1)
)
pair_fit <- sreg(
  Y = pair_data$Y, S = pair_data$S, D = pair_data$D,
  small.strata = TRUE, k = 2
)
print(pair_fit)
```

Each pair contains one control and one treated individual. Here `k = 2` in the estimator validates the common pair size; the estimator can also infer it when `k` is omitted.

### Matched triplets and general k-tuples {#small-strata}

```r
set.seed(42)
triplet_data <- sreg.rgen(
  n = 300, tau.vec = c(1.2, 0.8), cluster = FALSE,
  small.strata = TRUE, k = 3, treat.sizes = c(1, 1, 1)
)
triplet_fit <- sreg(
  Y = triplet_data$Y, S = triplet_data$S, D = triplet_data$D,
  X = triplet_data[c("x_1", "x_2")],
  small.strata = TRUE, k = 3
)
print(triplet_fit)
```

The 300 observations form 100 triplets, with one individual assigned to each of control, treatment 1, and treatment 2. For other uniform k-tuple designs, specify the corresponding group size and allocation. In the generator, the entries of `treat.sizes` count control first, then active treatments, and must sum to `k`.

### Mixed small and large strata {#mixed-strata}

```r
set.seed(42)
mixed_data <- sreg.rgen(
  n = 120, tau.vec = 0.5, cluster = FALSE,
  mixed.strata = TRUE, n.small = 80,
  k = 4, treat.sizes = c(2, 2), n.strata = 4
)
mixed_fit <- sreg(
  Y = mixed_data$Y, S = mixed_data$S, D = mixed_data$D,
  small.strata = TRUE, k = 4
)
print(mixed_fit)
```

Here 80 observations form 20 small strata of size four. The remaining 40 observations form four large strata. Note the different arguments: **`mixed.strata` generates data; `small.strata` selects the estimation procedure.**

With varying stratum sizes, an explicit `k` identifies the intended small component. Automatic detection with `k = NULL` covers conventional pairs and triplets; specify `k` for mixed 4-tuples and larger. At least 25% of all strata must have the selected small size. This threshold concerns the number of strata, not the number of observations. The mixed estimator combines the small- and large-strata components using observation-count weights.

### Cluster-level assignment {#clusters}

```r
set.seed(42)
cluster_data <- sreg.rgen(
  n = 300, Nmax = 50, tau.vec = c(1.2, 0.8),
  n.strata = 4, cluster = TRUE
)
cluster_fit <- sreg(
  Y = cluster_data$Y, S = cluster_data$S, D = cluster_data$D,
  G.id = cluster_data$G.id, Ng = cluster_data$Ng,
  X = cluster_data[c("x_1", "x_2")]
)
print(cluster_fit)
```

Here `n = 300` in the generator means **300 clusters**, rather than 300 individuals. The returned data have one row per observed individual. Supply both the cluster identifiers and represented sizes to the estimator.

For matched or mixed cluster designs, combine `G.id` and `Ng` with `small.strata = TRUE`. Then `k` counts clusters per small stratum, and `n.small` in the generator counts clusters assigned to the small component. See the [design map](index.md#designs) for the combinations of assignment level and stratum structure.

## Output, inference, and reporting {#results}

`print(fit)` invokes the S3 method `print.sreg(x, ...)`. Its table reports ATE estimates, standard errors, test statistics, p-values, 95% asymptotic confidence intervals, and significance indicators. It also reports the number of observations, treatments and strata, the assignment level, the strata procedure, the HC1 setting, and adjustment covariates. Cluster counts and small-stratum size are shown when applicable.

The returned object is a list of class `sreg`:

| Element | Contents |
| --- | --- |
| `tau.hat` | One estimated ATE per active treatment, relative to control. |
| `se.rob` | Corresponding estimated standard errors. |
| `t.stat` | Estimate divided by its standard error. |
| `p.value` | Two-sided asymptotic p-values for zero treatment effects. |
| `CI.left`, `CI.right` | Lower and upper endpoints of the 95% asymptotic intervals. |
| `data` | Input data organized by the function, including outcomes and design variables. |
| `lin.adj` | Data frame of covariates used for linear adjustment. |
| `small.strata` | Whether the small-strata option was selected. |
| `HC1` | Whether the finite-sample variance correction was applied. |

Extract a table for further analysis or export:

```r
results <- data.frame(
  treatment = seq_along(large_fit$tau.hat),
  estimate = as.vector(large_fit$tau.hat),
  standard_error = as.vector(large_fit$se.rob),
  statistic = as.vector(large_fit$t.stat),
  p_value = as.vector(large_fit$p.value),
  lower = as.vector(large_fit$CI.left),
  upper = as.vector(large_fit$CI.right)
)
print(results)
write.csv(results, "sreg-results.csv", row.names = FALSE)
```

An estimate is expressed in the units of the outcome. The intervals use the asymptotic normal approximation; the reported test statistic does not imply a finite-sample Student t reference distribution. With multiple treatments, these are marginal intervals for each contrast with control. They do not provide simultaneous coverage for all effects.

`HC1 = FALSE` disables the finite-sample variance correction. It does not change the choice of experimental design. The [introductory example](get-started.md#interpret) and [empirical application](empirical-example.md#report) show numerical results and their interpretation.

## Plotting and customization {#plotting}

`plot(fit)` dispatches to `plot.sreg()`. It displays treatment-effect estimates and their confidence intervals and invisibly returns the underlying ggplot object.

```r
p <- plot(
  large_fit,
  treatment_labels = c("Treatment 1", "Treatment 2"),
  title = "Treatment effects relative to control",
  bar_fill = "#2463a6",
  point_shape = 23,
  point_fill = "white",
  x_axis_title = "Average treatment effect",
  zero_line = TRUE
)
```

| Argument | Purpose and default |
| --- | --- |
| `x` | The fitted `sreg` object. |
| `treatment_labels` | Labels in treatment order; defaults to “Treatment 1”, “Treatment 2”, etc. |
| `title` | Plot title; defaults to “Estimated ATEs with Confidence Intervals”. |
| `bar_fill` | Interval colors: default viridis scale (`NULL`), a single color, or two gradient colors. |
| `point_shape`, `point_size` | Point symbol (`23`, a diamond) and size (`3`). |
| `point_fill`, `point_color` | Point fill (`"white"`) and outline (`"black"`). |
| `point_stroke` | Point-outline thickness (`1.2`). |
| `label_color`, `label_size` | Estimate and standard-error label color (`"black"`) and size (`4`). |
| `bg_color` | Panel background; `NULL` retains the theme default. |
| `grid` | Show grid lines (`TRUE`). |
| `zero_line` | Show a dashed reference line at zero (`TRUE`). |
| `y_axis_title`, `x_axis_title` | Axis titles; each defaults to `NULL`. |
| `...` | Additional arguments; currently unused by this method. |

Because the result is a ggplot object, it can be further formatted or saved with ggplot2:

```r
p <- p + ggplot2::theme(legend.position = "none")
ggplot2::ggsave("sreg-treatment-effects.pdf", plot = p,
                width = 7, height = 4)
```

For a plot based on observed experimental data, see the [Peru results](empirical-example.md#report).

## Simulation reference {#simulation}

`sreg.rgen()` generates outcomes, assignments, design identifiers, and covariates for examples and simulation studies. It is not needed to analyze an existing experimental dataset.

```r
sreg.rgen(n, Nmax = 50, n.strata = 10,
          tau.vec = c(0), gamma.vec = c(0.4, 0.2, 1),
          cluster = TRUE, is.cov = TRUE, small.strata = FALSE,
          k = 3, treat.sizes = c(1, 1, 1),
          mixed.strata = FALSE, n.small = NULL)
```

| Argument | Meaning |
| --- | --- |
| `n` | Total individuals if `cluster = FALSE`; total clusters if `cluster = TRUE`. |
| `Nmax` | Maximum generated cluster size (default `50`). |
| `n.strata` | Number of large strata (default `10`); in a mixed design, refers to the large component. |
| `tau.vec` | Vector of population effects, one for each active treatment; default `c(0)`. |
| `gamma.vec` | Three covariate coefficients; default `c(0.4, 0.2, 1)`. |
| `cluster` | Generate cluster assignment (`TRUE` by default) or individual assignment. |
| `is.cov` | Include covariates (`TRUE` by default). |
| `small.strata` | Generate a uniform small-strata design (`FALSE` by default). |
| `k` | Assignment units per small stratum (default `3`); counts clusters under cluster assignment. |
| `treat.sizes` | Allocation counts in each small stratum, control first (default `c(1, 1, 1)`). Supply one entry for control and each active treatment, summing to `k`. |
| `mixed.strata` | Generate both small and large strata (`FALSE` by default). |
| `n.small` | Individuals or clusters allocated to the small component; must be divisible by `k`. With `NULL`, uses the largest multiple of `k` not exceeding half of `n`. |

The generated data include `Y`, `S`, and `D`; cluster designs also provide `G.id` and `Ng`. When covariates are included, `x_1` and `x_2` can be selected as the columns of `X`. In cluster designs, the number of returned rows is the number of observed individuals, not the value of the cluster-count argument `n`.

Set the seed before generation for reproducibility within R. Choose `tau.vec`, `k`, and `treat.sizes` jointly: for example, two active treatments in triplets use `tau.vec = c(1.2, 0.8)`, `k = 3`, and `treat.sizes = c(1, 1, 1)`. The worked examples above cover large strata, pairs, triplets, mixed designs, and clusters.

## Empirical application and further documentation {#resources}

The [Peru encouragement experiment](empirical-example.md?lang=r) walks through loading `AEJapp`, recoding control from `3` to `0`, inspecting assignment by stratum, estimating both treatment effects, adding covariates, and reporting results. It includes the README specification alongside a baseline-age adjustment example.

- [R README and source](https://github.com/jutrifonov/sreg)
- [Package manual — PDF](https://github.com/jutrifonov/sreg/raw/main/.github/README.pdf)
- [Estimator formulas — PDF](https://github.com/jutrifonov/sreg/raw/main/.github/assets/sreg-estimator-formulas.pdf)
- [Theoretical foundations and references](index.md#references)
- [Companion paper — coming soon](index.md#paper)

The project authors are Juri Trifonov, Yuehao Bai, Azeem Shaikh, and Max Tabord-Meehan. Use `citation("sreg")` for the installed software's citation and cite the methodological papers corresponding to the procedure used. The package is distributed under the MIT license.
