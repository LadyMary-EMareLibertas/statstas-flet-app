import numpy as np
import scipy.stats as stats

# ----------------------------
# 0. 공통 유틸 함수
# ----------------------------

# 표준 편차 계산 함수
# 입력된 데이터 리스트에서 표준편차를 소수점 3자리까지 반올림하여 반환
# ddof=1은 sample standard deviation (모집단 아님)
def compute_sd(data):
    return round(np.std(data, ddof=1), 3)

# 정규성 검정 함수
# 세 가지 검정(Shapiro-Wilk, Kolmogorov-Smirnov, Anderson-Darling)을 수행
# 셋 중 하나라도 통과하면 정규성을 만족한 것으로 간주
# alpha: 유의수준, 기본값 0.05
# 반환값: 각 검정의 결과 및 통과 여부 포함한 딕셔너리
def check_normality(group, alpha=0.05):
    group = np.array(group)

    # Shapiro-Wilk 검정 수행
    shapiro_p = stats.shapiro(group).pvalue
    shapiro_pass = shapiro_p > alpha

    # Kolmogorov-Smirnov 검정 수행 (평균과 표준편차 기준 정규분포 적합도)
    ks_p = stats.kstest(group, 'norm', args=(np.mean(group), np.std(group, ddof=1))).pvalue
    ks_pass = ks_p > alpha

    # Anderson-Darling 검정 수행
    ad_result = stats.anderson(group)
    ad_stat = ad_result.statistic
    ad_crit = ad_result.critical_values[2]  # 유의수준 5% 기준값
    ad_pass = ad_stat < ad_crit

    # 하나라도 통과하면 정규성 만족으로 판정
    passed = sum([shapiro_pass, ks_pass, ad_pass]) >= 1

    return {
        "passed": passed,
        "shapiro_p": shapiro_p,
        "shapiro_pass": shapiro_pass,
        "ks_p": ks_p,
        "ks_pass": ks_pass,
        "ad_stat": ad_stat,
        "ad_crit": ad_crit,
        "ad_pass": ad_pass
    }

# Cohen's d 해석 텍스트 반환 함수
# 입력값 d의 절댓값 크기에 따라 효과 크기를 텍스트로 반환
def interpret_cohens_d(d):
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"

# ----------------------------------------------
# 1. Paired t-test (두 집단 간 대응표본 t-검정)
# ----------------------------------------------

def run_paired_ttest(before, after, alpha=0.05, tail="two", return_dict=False):
    try:
        # 입력값 numpy 배열화
        before = np.array(before)
        after = np.array(after)
        diff = after - before

        # 정규성 검정
        norm = check_normality(diff.tolist(), alpha)

        # 정규성 미충족 시 종료
        if not norm["passed"]:
            error_msg = {
                "error": "Normality assumption not met.\nConsider using Wilcoxon Signed-Rank test.",
                "normality": norm
            }
            return error_msg if return_dict else error_msg["error"]

        # t-검정 실행
        t_stat, p_two = stats.ttest_rel(after, before)
        df = len(before) - 1  # 자유도 계산

        # 방향성 설정
        if tail == "two":
            p = p_two
            crit = stats.t.ppf(1 - alpha / 2, df)
            direction = None
        else:
            p = p_two / 2
            crit = stats.t.ppf(1 - alpha, df)
            direction = "after > before" if t_stat > 0 else "after < before"

        # 효과 크기 계산
        d = (np.mean(diff)) / np.std(diff, ddof=1)

        # NaN 발생 시 예외 반환
        if np.isnan(t_stat) or np.isnan(p) or np.isnan(d):
            return {
                "error": "T-test failed: one or more test statistics could not be calculated (NaN encountered).",
                "normality": norm
            } if return_dict else "T-test failed due to NaN in results."

        d_val = round(d, 3)
        d_interp = interpret_cohens_d(d)
        sig = "Significant" if p < alpha else "Not Significant"

        # 결과 딕셔너리 생성
        result = {
            "t_stat": t_stat,
            "p": p,
            "df": df,
            "crit": crit,
            "direction": direction,
            "cohen_d": d_val,
            "cohen_d_interp": d_interp,
            "sig": sig,
            "tail": tail,
            "alpha": alpha,
            "normality": norm,
            "error": None
        }

        if return_dict:
            return result

    except Exception as e:
        err = f"❌ Error: {e}"
        return {"error": err} if return_dict else err

# ----------------------------------------------
# 2. Independent t-test (독립표본 t-검정)
# ----------------------------------------------

def run_independent_ttest(group1, group2, alpha=0.05, tail="two"):
    try:
        group1 = np.array(group1)
        group2 = np.array(group2)

        # 정규성 검정
        norm1 = check_normality(group1, alpha)
        norm2 = check_normality(group2, alpha)

        # 정규성 미충족 시 종료
        if not (norm1["passed"] and norm2["passed"]):
            return (
                "❌ Normality assumption not met in one or both groups.\n"
                "Consider using Mann-Whitney U test."
            )

        # 분산 동질성 검정
        levene_stat, levene_p = stats.levene(group1, group2)
        equal_var = levene_p > alpha

        # 평균, 분산, 샘플 수 계산
        m1, m2 = np.mean(group1), np.mean(group2)
        s1, s2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        n1, n2 = len(group1), len(group2)

        # Student's t-test 또는 Welch's t-test 분기 처리
        if equal_var:
            test_used = "Student's t-test"
            df = n1 + n2 - 2
            t_stat, p_two = stats.ttest_ind(group1, group2, equal_var=True)
            crit = stats.t.ppf(1 - alpha / 2 if tail == "two" else 1 - alpha, df)
            pooled_sd = np.sqrt(((n1 - 1)*s1 + (n2 - 1)*s2) / df)
            d = (m1 - m2) / pooled_sd
        else:
            test_used = "Welch's t-test"
            se = np.sqrt(s1/n1 + s2/n2)
            t_stat = (m1 - m2) / se
            df = ((s1/n1 + s2/n2)**2) / (((s1/n1)**2)/(n1-1) + ((s2/n2)**2)/(n2-1))
            p_two = 2 * (1 - stats.t.cdf(abs(t_stat), df))
            crit = stats.t.ppf(1 - alpha / 2 if tail == "two" else 1 - alpha, df)
            d = (m1 - m2) / ((np.std(group1, ddof=1) + np.std(group2, ddof=1)) / 2)

        # p-값 및 방향 해석
        p = p_two if tail == "two" else p_two / 2
        direction = None if tail == "two" else ("group1 < group2" if t_stat > 0 else "group1 > group2")

        d_val = round(d, 3)
        d_interp = interpret_cohens_d(d)
        sig = "✅ Significant" if p < alpha else "❌ Not Significant"

        # 출력 문자열 구성 (뷰에서 추후 분리 예정)
        sd1 = compute_sd(group1)
        sd2 = compute_sd(group2)
        output = "🔍 Independent T-test Result\n"
        output += f"- Test Used: {test_used}\n"
        output += f"- Variance Equality: {'Passed (Levene’s p = {:.4f})'.format(levene_p) if equal_var else 'Failed (Levene’s p = {:.4f})'.format(levene_p)}\n"
        if direction:
            output += f"- Direction: {direction}\n"
        output += (
            f"- t({df:.2f}) = {t_stat:.3f}\n"
            f"- p = {p:.4f} ({tail}-tailed)\n"
            f"- Critical value = {crit:.3f} (α = {alpha})\n"
            f"- SD(Group 1) = {sd1}\n"
            f"- SD(Group 2) = {sd2}\n"
            f"- Cohen's d = {d_val} ({d_interp})\n"
            f"- Result: {sig}\n"
        )

        # 참고문헌 추가
        output += "\nReferences (APA 7th Edition):\n"
        output += "Gosset, W. S. (1908). The probable error of a mean.\n"
        output += "*Biometrika, 6*(1), 1-25. https://doi.org/10.1093/biomet/6.1.1\n"
        output += "Welch, B. L. (1947). The generalization of Student's problem when several different\n"
        output += "population variances are involved. *Biometrika, 34*(1-2), 28-35.\n"
        output += "https://doi.org/10.1093/biomet/34.1-2.28\n"
        output += "Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0.\n"
        output += "*Nature Methods, 17*(3), 261-272. https://doi.org/10.1038/s41592-019-0686-2"

        return output

    except Exception as e:
        return f"❌ Error: {e}"

# -----------------------------------------------
# 3. One-sample t-test (단일 표본 t-검정)
# -----------------------------------------------

def run_one_sample_ttest(sample, mu, alpha=0.05, tail="two"):
    try:
        sample = np.array(sample)
        n = len(sample)
        df = n - 1

        # 정규성 검정
        norm = check_normality(sample.tolist(), alpha)
        if not norm["passed"]:
            return (
                "❌ Normality assumption not met.\n"
                "Consider using Wilcoxon signed-rank test."
            )

        sample_mean = np.mean(sample)
        sample_std = np.std(sample, ddof=1)
        se = sample_std / np.sqrt(n)
        t_stat = (sample_mean - mu) / se

        if tail == "two":
            p = 2 * (1 - stats.t.cdf(abs(t_stat), df))
            crit = stats.t.ppf(1 - alpha / 2, df)
            direction = None
        else:
            p = 1 - stats.t.cdf(t_stat, df) if t_stat > 0 else stats.t.cdf(t_stat, df)
            crit = stats.t.ppf(1 - alpha, df)
            direction = "μ < sample mean" if t_stat > 0 else "μ > sample mean"

        d = (sample_mean - mu) / sample_std
        d_val = round(d, 3)
        d_interp = interpret_cohens_d(d)
        sig = "✅ Significant" if p < alpha else "❌ Not Significant"

        output = "🔍 One-sample T-test Result\n"
        if direction:
            output += f"- Direction: {direction}\n"
        output += (
            f"- Population mean (μ) = {mu}\n"
            f"- Sample mean = {sample_mean:.3f}\n"
            f"- t({df}) = {t_stat:.3f}\n"
            f"- p = {p:.4f} ({tail}-tailed)\n"
            f"- Critical value = {crit:.3f} (α = {alpha})\n"
            f"- Cohen’s d = {d_val} ({d_interp})\n"
            f"- Result: {sig}\n"
        )

        # 참고문헌 추가
        output += "\nReferences (APA 7th Edition):\n"
        output += "Gosset, W. S. (1908). The probable error of a mean.\n"
        output += "*Biometrika, 6*(1), 1–25. https://doi.org/10.1093/biomet/6.1.1\n"
        output += "Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0.\n"
        output += "*Nature Methods, 17*(3), 261–272. https://doi.org/10.1038/s41592-019-0686-2"

        return output

    except Exception as e:
        return f"❌ Error: {e}"

# -----------------------------------------------
# 3. One-sample t-test (two-tailed & one-tailed)
# -----------------------------------------------

def run_one_sample_ttest(sample, mu, alpha=0.05, tail="two"):
    try:
        sample = np.array(sample)
        n = len(sample)
        df = n - 1

        # 정규성 검정
        norm = check_normality(sample.tolist(), alpha)
        if not norm["passed"]:
            return (
                "❌ Normality assumption not met.\n"
                "Consider using Wilcoxon signed-rank test."
            )

        sample_mean = np.mean(sample)
        sample_std = np.std(sample, ddof=1)
        se = sample_std / np.sqrt(n)
        t_stat = (sample_mean - mu) / se

        if tail == "two":
            p = 2 * (1 - stats.t.cdf(abs(t_stat), df))
            crit = stats.t.ppf(1 - alpha / 2, df)
            direction = None
        else:
            p = 1 - stats.t.cdf(t_stat, df) if t_stat > 0 else stats.t.cdf(t_stat, df)
            crit = stats.t.ppf(1 - alpha, df)
            direction = "μ < sample mean" if t_stat > 0 else "μ > sample mean"

        d = (sample_mean - mu) / sample_std
        d_val = round(d, 3)
        d_interp = interpret_cohens_d(d)
        sig = "✅ Significant" if p < alpha else "❌ Not Significant"

        # ⚠️ 결과 문자열 조립 – 나중에 view(one_sample_two.py / one_sample_one.py)로 분리 예정
        output = "🔍 One-sample T-test Result\n"
        if direction:
            output += f"- Direction: {direction}\n"
        output += (
            f"- Population mean (μ) = {mu}\n"
            f"- Sample mean = {sample_mean:.3f}\n"
            f"- t({df}) = {t_stat:.3f}\n"
            f"- p = {p:.4f} ({tail}-tailed)\n"
            f"- Critical value = {crit:.3f} (α = {alpha})\n"
            f"- Cohen’s d = {d_val} ({d_interp})\n"
            f"- Result: {sig}\n"
        )

        output += "\nReferences (APA 7th Edition):\n"
        output += "Gosset, W. S. (1908). The probable error of a mean.\n"
        output += "*Biometrika, 6*(1), 1–25. https://doi.org/10.1093/biomet/6.1.1\n"
        output += "Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0.\n"
        output += "*Nature Methods, 17*(3), 261–272. https://doi.org/10.1038/s41592-019-0686-2"

        return output

    except Exception as e:
        return f"❌ Error: {e}"

