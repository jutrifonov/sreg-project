---
home: true
title: Stratified Randomized Experiments
description: Estimation of average treatment effects and asymptotically valid inference in stratified randomized experiments, with implementations in R, Stata, and Python.
---

<section class="hero">
<div class="wrap hero-grid">
<div class="hero-copy">
<p class="eyebrow">The sreg project</p>
<h1>Stratified<br>Randomized<br><span>Experiments</span></h1>
<p class="hero-description">sreg implements methods from modern econometric theory for estimation and inference on average treatment effects in stratified randomized experiments. It automatically applies point and variance estimators appropriate to the specified experimental design, enabling asymptotically valid inference. It supports individual- and cluster-level treatment assignment across large strata, matched pairs, general k-tuples, and mixed designs.</p>
<div class="hero-actions"><a class="button primary" href="get-started/">Installation and examples <span aria-hidden="true">→</span></a><a class="text-link" href="#designs">Supported designs</a></div>
<div class="hero-languages"><span>Implementations</span><a href="get-started/?lang=r">R</a><span class="separator">/</span><a href="get-started/?lang=stata">Stata</a><span class="separator">/</span><a href="get-started/?lang=python">Python</a></div>
</div>
<figure class="hero-randomization-art"><img src="assets/randomization-hero.png" alt="Conceptual illustration of stratified randomization: blue and ivory units grouped beneath two distribution curves" width="1254" height="1254" fetchpriority="high"></figure>
</div>
</section>

<section id="overview" class="overview-section wrap">
<div class="overview-copy"><p class="eyebrow">Purpose and scope</p><h2>Inference for stratified experiments</h2>
<p>sreg is intended for researchers analyzing stratified experimental data in development economics, experimental economics, and other fields using randomized experiments. It provides a common toolkit for estimating average treatment effects and conducting inference under a broad range of stratification designs.</p>
<p>A fully saturated regression can recover treatment effects by aggregating stratum-specific contrasts, but its conventional heteroskedasticity-robust standard errors are not generally valid under stratified randomization. Including strata and treatment–stratum interactions does not, by itself, resolve the variance-estimation problem. See <a href="#ref-bcs2019">Bugni, Canay, and Shaikh (2019)</a>.</p>
<p>sreg implements multiple estimators introduced in the recent econometric theory literature. Given the assignment indicators, strata, and design options, it automatically applies the corresponding point and variance estimators for asymptotically valid inference, avoiding manual implementation of design-specific weights and variance corrections. It supports matched pairs, general <i>k</i>-tuples, large strata of potentially unequal sizes, mixed designs, multiple treatments, and cluster-level assignment, with optional optimal linear adjustment using baseline covariates. The procedures draw on <a href="#references">recent econometric research</a>.</p></div>
<figure class="overview-logo"><img src="assets/sreg-logo.png" alt="sreg: Stratified Randomized Experiments package logo" width="2357" height="2359"><figcaption>R · Stata · Python</figcaption></figure>
</section>

<section id="packages" class="packages wrap">
<div class="section-intro"><p class="eyebrow">Software</p><h2>R, Stata, and Python implementations</h2><p>Estimation and inference for stratified randomized experiments, with interfaces and reporting tools specific to each language.</p></div>
<div class="package-grid">
<article class="package-card"><div class="package-heading"><span class="language-mark">R</span><span class="package-label">CRAN + GitHub</span></div><h3>sreg for R</h3><p>Estimation and inference in R, with S3 methods for reporting results and plotting confidence intervals.</p><div class="package-links"><a href="get-started/?lang=r">Get started <span aria-hidden="true">→</span></a><a href="https://github.com/jutrifonov/sreg" aria-label="R source on GitHub">GitHub ↗</a></div></article>
<article class="package-card"><div class="package-heading"><span class="language-mark stata-mark">St</span><span class="package-label">Native Stata / Mata</span></div><h3>sreg for Stata</h3><p>Estimation and inference in native Stata/Mata, with stored coefficient and covariance matrices and support for postestimation commands.</p><div class="package-links"><a href="get-started/?lang=stata">Get started <span aria-hidden="true">→</span></a><a href="https://github.com/jutrifonov/sreg-stata" aria-label="Stata source on GitHub">GitHub ↗</a></div></article>
<article class="package-card"><div class="package-heading"><span class="language-mark python-mark">Py</span><span class="package-label">Python implementation</span></div><h3>sreg for Python</h3><p>Estimation and inference in Python, with array and DataFrame inputs and Matplotlib plots.</p><div class="package-links"><a href="get-started/?lang=python">Get started <span aria-hidden="true">→</span></a><a href="https://github.com/jutrifonov/sreg-python" aria-label="Python source on GitHub">GitHub ↗</a></div></article>
</div>
</section>

<section class="example-section">
<div class="wrap example-grid">
<div class="example-copy"><p class="eyebrow">Estimation example</p><h2>Estimation and<br>inference</h2><p>The estimator takes observed outcomes, treatment assignments, and stratum indicators as inputs. Supplying baseline covariates selects linear covariate adjustment.</p><p class="example-note">The example uses individual-level assignment and large strata. Each active treatment is compared with the control group, coded <code>0</code>. The output reports ATE estimates, standard errors, and asymptotic confidence intervals.</p><a class="text-link" href="get-started/">Estimation walkthrough →</a><p class="empirical-link"><a href="empirical-example/">Empirical application: school performance in Peru →</a></p></div>
<div class="code-window">
<div class="code-toolbar"><div class="language-tabs" role="group" aria-label="Example language"><button type="button" data-select-lang="r" aria-pressed="true">R</button><button type="button" data-select-lang="stata" aria-pressed="false">Stata</button><button type="button" data-select-lang="python" aria-pressed="false">Python</button></div><span class="code-filename">Large-strata specification</span></div>
<div data-lang="r" markdown="1">
```r
library(sreg)

fit <- sreg(
  Y = dat$Y,
  S = dat$S,
  D = dat$D,
  X = dat[c("x_1", "x_2")]
)

print(fit)
```
</div>
<div data-lang="stata" hidden markdown="1">
```stata
* Outcome Y, treatment D, strata S; baseline covariates x_1 x_2
sreg Y x_1 x_2, treatment(D) strata(S)

* Inspect the estimated treatment effects
matrix list e(b)

* Plot estimates and confidence intervals
sregplot
```
</div>
<div data-lang="python" hidden markdown="1">
```python
from sreg import sreg

fit = sreg(
    Y=dat["Y"],
    S=dat["S"],
    D=dat["D"],
    X=dat[["x_1", "x_2"]],
)

print(fit)
```
</div>
<div class="code-footnote">Treatment effects · Standard errors · Confidence intervals</div>
</div>
</div>
</section>

<section id="designs" class="designs-section wrap">
<div class="section-intro"><p class="eyebrow">Scope</p><h2>Supported experimental designs</h2><p>The appropriate estimator and variance formula depend on the stratification structure and the unit of treatment assignment.</p></div>
<div class="design-map"><div class="map-toolbar"><span>Arguments by implementation</span><div class="language-tabs" role="group" aria-label="Design map language"><button type="button" data-select-lang="r" aria-pressed="true">R</button><button type="button" data-select-lang="stata" aria-pressed="false">Stata</button><button type="button" data-select-lang="python" aria-pressed="false">Python</button></div></div><div class="map-root"><code>sreg</code><span>Assignment unit</span></div><div class="map-branches"><section class="map-branch individual"><h3>Individual-level assignment</h3><div class="assignment-option"><span data-lang="r"><code>G.id = NULL</code></span><span data-lang="stata" hidden><code>omit cluster()</code></span><span data-lang="python" hidden><code>G_id=None</code></span></div><div class="map-regimes"><a class="map-node" href="get-started/#large-strata"><strong>Large strata</strong><span data-lang="r"><code>small.strata = FALSE</code></span><span data-lang="stata" hidden><code>omit smallstrata</code></span><span data-lang="python" hidden><code>small_strata=False</code></span><small>Large-strata variance procedure</small></a><a class="map-node" href="get-started/#small-strata"><strong>Small strata</strong><span data-lang="r"><code>small.strata = TRUE</code></span><span data-lang="stata" hidden><code>smallstrata</code></span><span data-lang="python" hidden><code>small_strata=True</code></span><small>Common stratum size; pairs or k-tuples</small></a><a class="map-node" href="get-started/#mixed-strata"><strong>Mixed design</strong><span data-lang="r"><code>small.strata = TRUE</code></span><span data-lang="stata" hidden><code>smallstrata</code></span><span data-lang="python" hidden><code>small_strata=True</code></span><small>Small and large strata combined</small></a></div></section><section class="map-branch cluster"><h3>Cluster-level assignment</h3><div class="assignment-option"><span data-lang="r"><code>G.id supplied</code></span><span data-lang="stata" hidden><code>cluster(G_id)</code></span><span data-lang="python" hidden><code>G_id supplied</code></span></div><div class="map-regimes"><a class="map-node" href="get-started/#large-strata"><strong>Large strata</strong><span data-lang="r"><code>small.strata = FALSE</code></span><span data-lang="stata" hidden><code>omit smallstrata</code></span><span data-lang="python" hidden><code>small_strata=False</code></span><small>Large-strata variance procedure</small></a><a class="map-node" href="get-started/#small-strata"><strong>Small strata</strong><span data-lang="r"><code>small.strata = TRUE</code></span><span data-lang="stata" hidden><code>smallstrata</code></span><span data-lang="python" hidden><code>small_strata=True</code></span><small>Common cluster-stratum size; pairs or k-tuples</small></a><a class="map-node" href="get-started/#mixed-strata"><strong>Mixed design</strong><span data-lang="r"><code>small.strata = TRUE</code></span><span data-lang="stata" hidden><code>smallstrata</code></span><span data-lang="python" hidden><code>small_strata=True</code></span><small>Small and large cluster-strata combined</small></a></div></section></div><div class="map-inputs"><strong>Adjustment and additional design inputs</strong><p data-lang="r">X = NULL: unadjusted; supply X for linear adjustment. Ng supplies represented cluster sizes. k identifies or validates the small-stratum size.</p><p data-lang="stata" hidden>Omit covariates for unadjusted estimation; list them after the outcome for linear adjustment. clustersize(Ng) supplies represented cluster sizes. k(#) identifies or validates the small-stratum size.</p><p data-lang="python" hidden>X=None: unadjusted; supply X for linear adjustment. Ng supplies represented cluster sizes. k identifies or validates the small-stratum size.</p></div><p class="map-caption">The assignment unit and selected strata procedure determine the estimator. With the small-strata option enabled, a common stratum size selects the small-strata procedure; varying sizes identify a mixed design, subject to the package’s classification requirements. For cluster assignment, stratum sizes and k count clusters.</p></div>
<p class="designs-note">Cluster assignment can be combined with large, small, or mixed strata. Multiple active treatments and covariate adjustment are supported across these designs.</p>
</section>

<section id="methods" class="methods-section"><div class="wrap methods-grid"><div><p class="eyebrow">Methodology</p><h2>Estimators and asymptotic inference</h2><p>The package implements estimators and variance formulas from the literature on covariate-adaptive randomization, matched-group designs, and cluster-randomized experiments. The methodological references state the assumptions required for consistency, asymptotic normality, and the efficiency properties of covariate adjustment.</p></div><div class="method-links"><a href="https://github.com/jutrifonov/sreg/raw/main/.github/assets/sreg-estimator-formulas.pdf"><span><strong>Estimator formulas</strong><small>Large, small, and mixed strata · PDF</small></span><span aria-hidden="true">↗</span></a><a href="#references"><span><strong>Methodological references</strong><small>Papers on randomization, adjustment, and inference</small></span><span aria-hidden="true">↗</span></a><a href="get-started/#citation"><span><strong>Cite sreg</strong><small>Software attribution and methodological references</small></span><span aria-hidden="true">→</span></a></div></div></section>

<section id="paper" class="paper-section wrap"><div><p class="eyebrow">Companion paper</p><h2>The sreg paper</h2><p>A companion paper is in preparation. It presents the estimation and inference procedures implemented in sreg, the supported experimental designs, and guidance for empirical applications.</p><p>The manuscript and its arXiv record will be linked here once available.</p></div><span class="paper-status">Coming soon</span></section>

<section id="references" class="references-section wrap"><div class="section-intro"><p class="eyebrow">References</p><h2>Theoretical foundations</h2><p>Theoretical results underlying the estimation and inference procedures implemented in sreg.</p></div><ol class="reference-list"><li id="ref-bcs2018"><span>Bugni, F. A., Canay, I. A., and Shaikh, A. M. (2018).</span> <a href="https://doi.org/10.1080/01621459.2017.1375934">Inference Under Covariate-Adaptive Randomization</a>. <i>Journal of the American Statistical Association</i>.</li><li id="ref-bcs2019"><span>Bugni, F. A., Canay, I. A., and Shaikh, A. M. (2019).</span> <a href="https://doi.org/10.3982/QE1150">Inference under Covariate-Adaptive Randomization with Multiple Treatments</a>. <i>Quantitative Economics</i>.</li><li id="ref-cluster"><span>Bugni, F. A., Canay, I. A., Shaikh, A. M., and Tabord-Meehan, M. (2025).</span> <a href="https://doi.org/10.1086/732836">Inference for Cluster Randomized Experiments with Non-ignorable Cluster Sizes</a>. <i>Journal of Political Economy Microeconomics</i>.</li><li id="ref-jiang"><span>Jiang, L., Linton, O. B., Tang, H., and Zhang, Y. (2026).</span> <a href="https://doi.org/10.1162/rest_a_01417">Improving Estimation Efficiency via Regression-Adjustment in Covariate-Adaptive Randomizations with Imperfect Compliance</a>. <i>Review of Economics and Statistics</i>.</li><li id="ref-baiadjust"><span>Bai, Y., Jiang, L., Romano, J. P., Shaikh, A. M., and Zhang, Y. (2024).</span> <a href="https://doi.org/10.1016/j.jeconom.2024.105740">Covariate adjustment in experiments with matched pairs</a>. <i>Journal of Econometrics</i>.</li><li id="ref-bai2022"><span>Bai, Y. (2022).</span> <a href="https://doi.org/10.1257/aer.20201856">Optimality of Matched-Pair Designs in Randomized Controlled Trials</a>. <i>American Economic Review</i>.</li><li id="ref-brs2022"><span>Bai, Y., Romano, J. P., and Shaikh, A. M. (2022).</span> <a href="https://doi.org/10.1080/01621459.2021.1883437">Inference in Experiments With Matched Pairs</a>. <i>Journal of the American Statistical Association</i>.</li><li id="ref-liu"><span>Liu, J. (2026 revision).</span> <a href="https://arxiv.org/abs/2301.09016">Inference for Two-stage Experiments under Covariate-Adaptive Randomization</a>. <i>Working paper, arXiv:2301.09016</i>.</li><li id="ref-cytrynbaum"><span>Cytrynbaum, M. (2024).</span> <a href="https://doi.org/10.3982/QE2475">Covariate Adjustment in Stratified Experiments</a>. <i>Quantitative Economics</i>.</li></ol></section>
