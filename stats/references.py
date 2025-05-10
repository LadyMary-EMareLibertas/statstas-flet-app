def get_references_for_test(test_type: str, extra: list = []) -> str:
    """
    Return appropriate references for the given t-test type.

    Parameters:
        test_type: str  # 'paired', 'independent', 'one_sample', 'welch'
        extra: list[str]  # e.g., ['welch'], ['wilcoxon'] for condition-based additions

    Returns:
        str: Formatted reference block (APA 7th edition)
    """
    references = []

    # --- Universal reference (SciPy used in all) ---
    references.append(
        "Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., "
        "Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S. J., Brett, M., Wilson, J., "
        "Millman, K. J., Mayorov, N., Nelson, A. R. J., Jones, E., Kern, R., Larson, E., Carey, C. J., "
        "... van Mulbregt, P. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. "
        "*Nature Methods, 17*(3), 261–272. https://doi.org/10.1038/s41592-019-0686-2"
    )

    # --- Gosset (Student's t-test) ---
    if test_type in {"paired", "independent", "one_sample"} or "student" in extra:
        references.append(
            "Gosset, W. S. (1908). The probable error of a mean. "
            "*Biometrika, 6*(1), 1–25. https://doi.org/10.1093/biomet/6.1.1"
        )

    # --- Welch t-test ---
    if test_type == "welch" or "welch" in extra:
        references.append(
            "Welch, B. L. (1947). The generalization of Student's problem when several different population variances are involved. "
            "*Biometrika, 34*(1–2), 28–35. https://doi.org/10.1093/biomet/34.1-2.28"
        )

    # --- Wilcoxon Signed-Rank Test (nonparametric) ---
    if "wilcoxon" in extra:
        references.append(
            "Wilcoxon, F. (1945). Individual comparisons by ranking methods. "
            "*Biometrics Bulletin, 1*(6), 80–83. https://doi.org/10.2307/3001968"
        )

    return "References (APA 7th Edition):\n\n" + "\n\n".join(references) + "\n" + ("-" * 77) + "\n"