from stats.tools.t_test.ttest_logic import run_independent_ttest

# 예제 데이터 (그룹별로 분산 차이 확 나게 설정해 봐도 좋아)
group1 = [100, 102, 98, 101, 100]
group2 = [110, 130, 115, 125, 120]
alpha = 0.05

# 양측 검정
result = run_independent_ttest(group1, group2, alpha=alpha, tail="two")

# 결과 출력
print(result)