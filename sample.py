from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 데이터 불러오기
df = pd.read_csv('math_problems.csv')

# 특징 추출
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['problem'])
y = df['diagram']

# 학습 및 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 결정 트리 모델 학습
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# 예측 및 성능 평가
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")


new_problem = "두 점 A(1, 1)와 B(4, 5) 사이의 거리를 구하시오."
new_problem_transformed = vectorizer.transform([new_problem])
predicted_diagram = model.predict(new_problem_transformed)

print(predicted_diagram[0])
