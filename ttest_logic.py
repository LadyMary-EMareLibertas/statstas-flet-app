import numpy as np
from scipy import stats

def run_paired_ttest(before, after, alpha=0.05):
    try:
        if len(before) != len(after):
            return {"error": "Length of before and after must match."}

        diff = np.array(after) - np.array(before)

        # 정규성 검정
        shapiro_p = stats.shapiro(diff).pvalue
        ks_p = stats.kstest(diff, 'norm', args=(np.mean(diff), np.std(diff, ddof=1))).pvalue
        ad_result = stats.anderson(diff)
        ad_stat = ad_result.statistic
        ad_crit = ad_result.critical_values[2]
        normal = shapiro_p > alpha or ks_p > alpha or ad_stat < ad_crit

        if not normal:
            return {
                "error": "Normality failed",
                "shapiro_p": round(shapiro_p, 4),
                "ks_p": round(ks_p, 4),
                "ad_stat": round(ad_stat, 4),
                "ad_crit": round(ad_crit, 4)
            }

        # Paired t-test
        t_stat, p_val = stats.ttest_rel(after, before)
        df = len(before) - 1
        critical = stats.t.ppf(1 - alpha / 2, df)
        mean = np.mean(diff)
        std = np.std(diff, ddof=1)
        d = abs(mean / std)

        return {
            "n": len(before),
            "t_stat": round(t_stat, 4),
            "p_val": round(p_val, 4),
            "critical_val": round(critical, 4),
            "cohens_d": round(d, 3),
            "significance": "significant" if p_val < alpha else "not significant",
            "normality": {
                "shapiro_p": round(shapiro_p, 4),
                "ks_p": round(ks_p, 4),
                "ad_stat": round(ad_stat, 4),
                "ad_crit": round(ad_crit, 4),
                "passed": normal
            }
        }
    except Exception as e:
        return {"error": str(e)}