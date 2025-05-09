#-----------------------------------------------------------------------------  
#                       1. Paired t-test (two-tailed)  
#-----------------------------------------------------------------------------  

import numpy as np
import scipy.stats as stats

# ==== DATA INPUT ====
before = [580, 590, 600, 570, 510]
after = [650, 690, 670, 600, 670]
alpha = 0.05
# ====================

print("\n\n🔍 Paired t-test (two-tailed) result:")
print("-----------------------------------------------------------------------------")


# === Normality check on difference ===
def check_normality(diff):
    shapiro_p = stats.shapiro(diff).pvalue
    ks_p = stats.kstest(diff, 'norm', args=(np.mean(diff), np.std(diff, ddof=1))).pvalue
    ad_result = stats.anderson(diff)
    ad_stat = ad_result.statistic
    ad_crit = ad_result.critical_values[2]  # 5% level

    shapiro_pass = shapiro_p > alpha
    ks_pass = ks_p > alpha
    ad_pass = ad_stat < ad_crit
    n_passed = sum([shapiro_pass, ks_pass, ad_pass])

    return {
        "shapiro_p": shapiro_p,
        "ks_p": ks_p,
        "ad_stat": ad_stat,
        "ad_crit": ad_crit,
        "passed": n_passed >= 1,
        "shapiro_pass": shapiro_pass,
        "ks_pass": ks_pass,
        "ad_pass": ad_pass
    }

# Compute difference
diff = np.array(after) - np.array(before)

# Normality test
res = check_normality(diff)

print("\n🔍 Normality Test on Differences (after - before):")
print("-----------------------------------------------------------------------------")
print(f"# Shapiro-Wilk: {'passed' if res['shapiro_pass'] else 'failed'} (p = {res['shapiro_p']:.4f})")
print(f"# Kolmogorov-Smirnov: {'passed' if res['ks_pass'] else 'failed'} (p = {res['ks_p']:.4f})")
print(f"# Anderson-Darling: {'passed' if res['ad_pass'] else 'failed'} (stat = {res['ad_stat']:.4f}, crit = {res['ad_crit']:.4f})")

if res["passed"]:
    print("\n# ✅ Normality assumption met (at least 1 test passed). Proceeding to t-test...\n")
else:
    print("\n# ❌ Normality assumption failed. Consider using Wilcoxon Signed-Rank test.\n")
    exit()


# === Paired t-test ===
t_stat, p_val = stats.ttest_rel(after, before)
df = len(before) - 1

# Two-tailed critical value
critical_val = stats.t.ppf(1 - alpha / 2, df)

# Significance
significance = "significant" if p_val < alpha else "not significant (p ≥ α)"

# === Cohen's d ===
mean_diff = np.mean(diff)
std_diff = np.std(diff, ddof=1)
cohens_d = round(abs(mean_diff / std_diff), 3)

# === Output Summary ===
print("T-test Result:")
print("-----------------------------------------------------------------------------")
print(f"#  - t({df}) = {t_stat:.3f}")
print(f"#  - p = {p_val:.4f} (two-tailed)")
print(f"#  - critical value = ±{critical_val:.3f} (α = {alpha})")
print(f"#  - Test Result: {significance}")
print(f"#  - Cohen’s d ≈ {cohens_d}")
print("-----------------------------------------------------------------------------")
print("References (APA 7th Edition):")
print("Gosset, W. S. (1908). The probable error of a mean.")
print("*Biometrika, 6*(1), 1–25. https://doi.org/10.1093/biomet/6.1.1\n")
print("Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D.,")
print("Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S. J., Brett, M., Wilson, J.,")
print("Millman, K. J., Mayorov, N., Nelson, A. R. J., Jones, E., Kern, R., Larson, E., Carey, C. J.,")
print("... van Mulbregt, P. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python.")
print("*Nature Methods, 17*(3), 261–272. https://doi.org/10.1038/s41592-019-0686-2")
print("-----------------------------------------------------------------------------")

  
#-----------------------------------------------------------------------------  
#----------------------------------------------------------------------------- 







