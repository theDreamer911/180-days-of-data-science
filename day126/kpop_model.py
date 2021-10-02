
# Import libraries
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Import data
df = pd.read_csv('fix_final_clean_kpop.csv')

# Subset relevant columns for model
df_model = df[['popl_by_country', 'reason', 'yr_litened', 'gender_pref',
               'daily_music_hr', 'watch_MV_yn', 'daily_MV_hr', 'obsessed_yn',
               'news_medium', 'pursuit', 'time_cons_yn', 'life_chg', 'pos_eff',
               'yr_merch_spent', 'money_src', 'concert_yn', 'crazy_ev', 'age',
               'country', 'job', 'gender', 'num_grp_like', 'bts_vs_others']]

# Get dummies
df_dummy = pd.get_dummies(df_model)
df_dummy

df_real = df[['yr_litened', 'daily_music_hr', 'daily_MV_hr',
              'yr_merch_spent', 'age', 'num_grp_like']]

# Train and Test Split

X = df_real.drop('daily_music_hr', axis=1)
X
y = df_real.daily_music_hr
y.value_counts()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=21)

# XGBoost

# Initialize linear regression model
xgb_clf = xgb.sklearn.XGBClassifier(nthread=-1, seed=1)

# Train the model
xgb_clf.fit(X_train, y_train)

# GridSearchCV

params = {'min_child_weight': [5], 'gamma': [1], 'subsample': [0.8, 1.0],
          'colsample_bytree': [0.6, 0.8], 'max_depth': [1, 2]}

gs_xgb = GridSearchCV(
    xgb_clf, params, scoring='neg_mean_absolute_error', cv=10)

gs_xgb.fit(X_train, y_train)

gs_xgb.best_score_

xgb_best = gs_xgb.best_estimator_
xgb_best

xgb_best.fit(X_train, y_train)

# Linear Regression
lm = LinearRegression()

lm.fit(X_train, y_train)

# Model save

with open('model.pkl', 'wb') as file:
    pickle.dump(xgb_best, file)
