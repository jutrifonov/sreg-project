---
title: User guide
description: Installation, ATE estimation, covariate adjustment, and asymptotic inference using sreg in R, Stata, and Python.
---

<p class="eyebrow">User guide</p>

# Estimation and inference

<p class="lead">This guide illustrates estimation of an average treatment effect under stratified randomization. A simulated example introduces the data structure, linear covariate adjustment, and interpretation of the reported estimates and standard errors.</p>

<div class="guide-language"><span>Implementation</span><div class="language-tabs" role="group" aria-label="Guide language"><button type="button" data-select-lang="r" aria-pressed="true">R</button><button type="button" data-select-lang="stata" aria-pressed="false">Stata</button><button type="button" data-select-lang="python" aria-pressed="false">Python</button></div></div>

<div class="callout"><strong>Detailed R documentation</strong><br>For all estimator arguments, worked design specifications, returned results, plot customization, and simulation options, see the <a href="r-guide.md">R guide and reference</a>. The <a href="empirical-example.md?lang=r">empirical application</a> follows a complete analysis of experimental data.</div>

<div class="callout"><strong>Simulation specification</strong><br>1,000 individuals · 4 large strata · 1 active treatment versus control · 2 baseline covariates. The simulated treatment effect is 0.5 outcome units.</div>

## 01 · Installation {#install}

<div data-lang="r" markdown="1">

Install the released R package from CRAN, then load it:

```r
install.packages("sreg")
library(sreg)
```

For the latest development version, install from the [R repository](https://github.com/jutrifonov/sreg):

```r
install.packages("remotes")
remotes::install_github("jutrifonov/sreg")
```

The example below uses the large-strata estimator. Feature availability may differ between the CRAN release and the development version; record the installed version when reporting an empirical analysis.

</div>
<div data-lang="stata" hidden markdown="1">

The Stata implementation requires **Stata 14.2 or newer**. Download the [Stata repository](https://github.com/jutrifonov/sreg-stata) using **Code → Download ZIP**, and unzip it. Access to the repository is required for this installation route.

Replace the example path with the absolute path to the extracted folder:

```stata
net install sreg, from("/path/to/sreg-stata") replace
help sreg
```

The package runs natively in Stata and Mata, without an R or Python dependency. These instructions refer to `sreg-stata`, the native implementation.

</div>
<div data-lang="python" hidden markdown="1">

The Python implementation requires **Python 3.9 or newer**. Install the current source from the [Python repository](https://github.com/jutrifonov/sreg-python) in your Python environment. This command requires Git and access to the repository:

```bash
python -m pip install "git+https://github.com/jutrifonov/sreg-python.git"
```

Then import the estimator and data generator:

```python
from sreg import sreg, sreg_rgen
```

The repository describes PyPI installation as a post-release option. Use the repository installation above for this walkthrough.

</div>

## 02 · Data and estimand {#data}

For the individual-randomized example, let Y(1) and Y(0) denote potential outcomes under treatment and control. The estimand is the average treatment effect, **τ = E[Y(1) − Y(0)]**. With multiple active treatments, the package estimates an ATE for each treatment relative to control.

The simulation has 1,000 individuals in four strata and a treatment effect of 0.5. The generator returns observed outcomes `Y`, stratum indicators `S`, assignments `D`, and covariates `x_1` and `x_2`. Treatment is assigned at the individual level within strata.

<div data-lang="r" markdown="1">

```r
set.seed(42)
dat <- sreg.rgen(
  n = 1000,
  tau.vec = c(0.5),
  n.strata = 4,
  cluster = FALSE
)

head(dat)
table(dat$S, dat$D)
```

</div>
<div data-lang="stata" hidden markdown="1">

Save any data you are working on first: the `clear` option replaces the dataset in memory.

```stata
set rng mt64
set seed 42
sreg_rgen, n(1000) individual strata(4) tau(.5) clear

list Y S D x_1 x_2 in 1/6
tabulate S D
```

</div>
<div data-lang="python" hidden markdown="1">

```python
dat = sreg_rgen(
    n=1000,
    tau_vec=(0.5,),
    n_strata=4,
    cluster=False,
    random_state=42,
)

print(dat.head())
print(dat.groupby(["S", "D"]).size())
```

</div>

The random seed makes a simulation repeatable within a given implementation and environment. **The same seed does not generate identical data across R, Stata, and Python.** Compare estimates across languages using the same input dataset.

| Variable | Definition |
| --- | --- |
| `Y` | The observed outcome for each individual |
| `S` | The stratum used for randomization |
| `D` | Treatment assignment: `0` for control, `1` for treatment |
| `x_1`, `x_2` | Baseline covariates used for linear adjustment |

## 03 · Estimation and covariate adjustment {#estimate}

The following specification estimates the ATE with linear adjustment for `x_1` and `x_2`. The default uses the large-strata procedure and applies the HC1 finite-sample correction to the variance estimator.

Covariates should be selected with reference to the experimental design and the intended adjustment specification. The package's adjustment procedure and corresponding variance estimator are described in the [methodological references](https://github.com/jutrifonov/sreg#references).

<div data-lang="r" markdown="1">

```r
fit <- sreg(
  Y = dat$Y,
  S = dat$S,
  D = dat$D,
  X = dat[c("x_1", "x_2")]
)
print(fit)
```

Omit `X` for estimation without covariate adjustment:

```r
fit_unadjusted <- sreg(Y = dat$Y, S = dat$S, D = dat$D)
print(fit_unadjusted)
```

</div>
<div data-lang="stata" hidden markdown="1">

```stata
sreg Y x_1 x_2, treatment(D) strata(S)
```

The command prints the results directly. Omit the covariate names for estimation without covariate adjustment:

```stata
sreg Y, treatment(D) strata(S)
```

Stata replaces the active estimation results each time an estimation command runs. Rerun the adjusted command before inspecting its stored results below.

</div>
<div data-lang="python" hidden markdown="1">

```python
fit = sreg(
    Y=dat["Y"],
    S=dat["S"],
    D=dat["D"],
    X=dat[["x_1", "x_2"]],
)
print(fit)
```

Omit `X` for estimation without covariate adjustment:

```python
fit_unadjusted = sreg(Y=dat["Y"], S=dat["S"], D=dat["D"])
print(fit_unadjusted)
```

</div>

## 04 · Interpretation and inference {#interpret}

Each row corresponds to an active treatment relative to control. The reported standard error is obtained from the variance estimator for the specified randomization design and adjustment procedure.

| Quantity | Interpretation |
| --- | --- |
| Treatment effect | Estimated average effect of treatment relative to control, in the units of `Y` |
| Standard error | Estimated sampling uncertainty, accounting for the selected design and adjustment |
| 95% confidence interval | The estimate plus or minus approximately 1.96 standard errors, based on the asymptotic normal approximation |
| p-value | Two-sided asymptotic test of the null hypothesis that the corresponding ATE equals zero |

In this simulation, the true ATE is **0.5**. The estimation error varies across simulated samples. The efficiency properties of covariate adjustment concern the relevant asymptotic variance; they do not imply that estimated standard errors decrease in every finite sample.

Confidence intervals and tests rely on an asymptotic approximation. The HC1 correction does not make inference exact in finite samples. When several treatment effects are reported, the individual 95% intervals are marginal intervals, rather than a simultaneous confidence region.

<div data-lang="r" markdown="1">

The returned object provides the estimates, standard errors, and interval endpoints:

```r
fit$tau.hat
fit$se.rob
cbind(lower = fit$CI.left, upper = fit$CI.right)
```

For this example, running R sreg 2.1.0 with seed 42 gives:

| Estimated effect | Standard error | 95% confidence interval |
| --- | --- | --- |
| 0.48152 | 0.06456 | [0.35500, 0.60805] |

The estimated ATE is 0.48152 outcome units, with a standard error of 0.06456. The 95% interval contains the data-generating value of 0.5 and excludes zero.

</div>
<div data-lang="stata" hidden markdown="1">

Inspect the adjusted model's stored results and plot its confidence interval:

```stata
sreg Y x_1 x_2, treatment(D) strata(S)
matrix list e(b)
matrix list e(V)
sregplot
```

`e(b)` contains the estimates; `e(V)` contains their covariance matrix. The treatment coefficient is named `tau1`.

</div>
<div data-lang="python" hidden markdown="1">

Extract the estimates and standard errors, or plot the result:

```python
print(fit["tau_hat"])
print(fit["se_rob"])
ax = fit.plot()
```

The plot method returns a Matplotlib `Axes` object for subsequent formatting or export.

</div>

## 05 · Specification for empirical applications {#next}

For an empirical application, supply observed outcomes, treatment assignments, randomization strata, and any covariates used for adjustment. Code control as `0` and active treatments as consecutive integers `1, 2, …`. Stratum codes `1, 2, …` provide a common format across implementations.

The specification must correspond to the assignment mechanism. Strata partition assignment units before randomization; clusters are groups of individuals assigned jointly to treatment. These identifiers have distinct roles in estimation and variance calculation.

### Large strata {#large-strata}

The example uses the large-strata procedure. For an unstratified experiment, omit the strata argument. The distinction between large and small strata concerns the stratification structure underlying the inference procedure, not the overall sample size alone.

### Matched pairs and k-tuples {#small-strata}

Select the small-strata estimator when the design uses small matched groups. The option is `small.strata = TRUE` in R, `smallstrata` in Stata, and `small_strata=True` in Python. In a uniform design the common group size can be inferred; an explicit `k` validates it.

### Mixed small and large strata {#mixed-strata}

Use the small-strata option to select mixed inference for varying stratum sizes. Specify `k` to identify the small component when it consists of 4-tuples or larger. At least 25% of strata must have the selected small-stratum size. See the [estimator formulas](https://github.com/jutrifonov/sreg/raw/main/.github/assets/sreg-estimator-formulas.pdf) and your implementation's reference before using this specification.

### Cluster assignment {#cluster-assignment}

Supply cluster identifiers and represented cluster sizes: `G.id` and `Ng` in R, `cluster()` and `clustersize()` in Stata, or `G_id` and `Ng` in Python. For small or mixed strata, `k` counts **clusters** per small stratum. Individual-varying covariates are aggregated to cluster means for adjustment.

<div class="callout"><strong>Design-specific variance estimation</strong><br>The example uses individual assignment and large strata. Cluster-randomized and matched-group designs require their corresponding estimator options and variance formulas.</div>

## Empirical application

The [Peru encouragement experiment](empirical-example.md) provides a complete application using the package's AEJapp data: treatment recoding, unadjusted and age-adjusted estimates, confidence intervals, and plotting in R, Stata, and Python.

## Reference documentation {#reference}

<div data-lang="r" markdown="1">

- **Complete guide:** [R guide and reference](r-guide.md).
- **Function help:** run `help(sreg)` and `help(sreg.rgen)` in R.
- **Examples and source:** visit the [R repository](https://github.com/jutrifonov/sreg).
- **Release information:** visit the [CRAN package page](https://cran.r-project.org/package=sreg).

</div>
<div data-lang="stata" hidden markdown="1">

- **Command help:** run `help sreg`, `help sreg_rgen`, and `help sregplot`.
- **Replication examples:** open [`examples/try_sreg.do`](https://github.com/jutrifonov/sreg-stata/blob/main/examples/try_sreg.do).
- **Source and installation updates:** visit the [Stata repository](https://github.com/jutrifonov/sreg-stata).

</div>
<div data-lang="python" hidden markdown="1">

- **API documentation:** read the [Python API reference](https://github.com/jutrifonov/sreg-python/blob/main/docs/api.md).
- **Additional examples:** read the [Python practical guide](https://github.com/jutrifonov/sreg-python/blob/main/docs/getting-started.md).
- **Source and installation updates:** visit the [Python repository](https://github.com/jutrifonov/sreg-python).

</div>

### Software citation {#citation}

Cite the software version used in the analysis and the methodological papers corresponding to the estimator and randomization design. The project authors are Juri Trifonov, Yuehao Bai, Azeem Shaikh, and Max Tabord-Meehan.

<div data-lang="r" markdown="1">

Get the citation for your installed R version:

```r
citation("sreg")
```

</div>
<div data-lang="stata" hidden markdown="1">

Record the Stata package version used in your analysis and consult the authorship and references in the [Stata README](https://github.com/jutrifonov/sreg-stata#authors).

</div>
<div data-lang="python" hidden markdown="1">

Use the repository's [citation metadata](https://github.com/jutrifonov/sreg-python/blob/main/CITATION.cff) and record the version used in your analysis.

</div>

<p class="page-source">Based on the R, Stata, and Python package documentation. Installation routes and advanced features may differ by release.</p>
