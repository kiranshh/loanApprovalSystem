import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from imblearn.over_sampling import SMOTE
import pickle

# reading the files
train=pd.read_csv("https://raw.githubusercontent.com/Chandu0312/loan_prediction/master/train.csv")
train.replace(
    to_replace=['Yes', 'Male','Graduate','Y'],
    value=1,
    inplace=True
)
train.replace(
    to_replace=['No', 'Female','Not Graduate','N'],
    value=0,
    inplace=True
)
train['Dependents'].replace('3+',3,inplace=True)
train['Property_Area'].replace('Urban',3,inplace=True)
train['Property_Area'].replace('Semiurban',2,inplace=True)
train['Property_Area'].replace('Rural',1,inplace=True)
train.drop('Loan_ID',axis=1,inplace=True)

nan_cols = [i for i in train.columns if train[i].isnull().any()]
nan_cols.remove('LoanAmount')
nan_cols.remove('Loan_Amount_Term')
imputer = KNNImputer(n_neighbors=5)
for i in nan_cols:
    train[[i]]=imputer.fit_transform(train[[i]])
train=train.fillna(train.isna().mean())

cat_cols = ['Credit_History','Dependents','Gender','Married','Education','Property_Area','Self_Employed']
for i in cat_cols:
    train[[i]]=train[[i]].astype("category")

X=train.drop('Loan_Status',axis=1)
y=train['Loan_Status']
sm = SMOTE(random_state = 2)
X, y = sm.fit_sample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
clf = LogisticRegression(random_state=1000,max_iter=10000).fit(X_train, y_train)
pickle.dump(clf, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))


