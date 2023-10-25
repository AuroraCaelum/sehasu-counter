from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math

startingDate = datetime.datetime(2023, 8, 5)

URL = "https://sehasu-counter.s3.ap-northeast-2.amazonaws.com/dailyCounts.csv"
df = pd.read_csv(URL)

successedDate = [80]

X = df["date"]
y = df["totalCount"]

goal = 1200000

line_fitter = LinearRegression()
line_fitter.fit(y.values.reshape(-1, 1), X)

print(line_fitter.predict([[goal]]))

predictor = goal
prediction = line_fitter.predict([[goal]])

plt.figure(figsize=(11, 5))
plt.ylim(600000, 1400000)  # y축 범위
plt.plot(X, y, "o")  # 기록 데이터
for i in successedDate:
    plt.plot(X[i], y[i], "o", color="red")  # 성공 데이터
# 예측기능 범위 시작

# plt.plot(math.ceil(prediction[0]), predictor, "o")  # 예측 데이터
# 예측량 주석
# plt.annotate(
#     "Expectation: "
#     + (startingDate + datetime.timedelta(days=math.ceil(prediction[0]))).strftime(
#         "%Y-%m-%d"
#     ),
#     xy=(prediction[0], predictor),
#     xytext=(prediction[0], predictor + 40000),
#     ha="left",
# )
# 기록 주석
# plt.annotate(
#     format(goal, ","),
#     xy=(prediction[0], predictor),
#     xytext=(prediction[0], predictor - 60000),
#     ha="left",
# )

# 예측기능 범위 끝

placing = 100000
for i in range(len(X)):
    if i % 5 == 0:
        plt.annotate(
            (startingDate + datetime.timedelta(days=int(X[i]))).strftime("%Y-%m-%d")
            + "\n"
            + str(format(y[i], ",")),
            xy=(X[i], y[i]),
            xytext=(X[i], y[i] + placing),
            ha="center",
            arrowprops=dict(arrowstyle="->", color="black"),
        )
        if placing == 100000:
            placing = -125000
        else:
            placing = 100000
# 예측기능 범위 시작
# plt.plot([X[0], math.ceil(prediction[0])], [y[0], predictor])  # 증가량 예측 직선
# 예측기능 범위 끝

# plt.plot(line_fitter.predict(y.values.reshape(-1, 1)), y, "-")
# plt.plot([X, y], [prediction[0], predictor])
arrYticks, txtYticks = plt.yticks()
plt.yticks(arrYticks, ["{:,.0f}".format(x) for x in arrYticks])
arrXticks, txtXticks = plt.xticks()
plt.xticks(
    arrXticks,
    [
        ((startingDate + datetime.timedelta(days=x)).strftime("%Y-%m-%d"))
        for x in arrXticks
    ],
)
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
# plt.show()

plt.savefig("src/lib/prediction.png", dpi=150, transparent=True)
