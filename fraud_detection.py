import pandas as pd
df = pd.read_csv("transactions.csv")
print(df)
import pandas as pd
df = pd.read_csv("transactions.csv")
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['transaction_time'] = pd.to_datetime(df['transaction_time'], format='%H:%M'
).dt.time
print(df.isnull().sum())
print(df)
df['rule_high_amount'] = df['amount'] > 50000
df['rule_new_account'] = (df['account_age_days'] < 30) & (df['amount'] > 20000)
df['hour'] = pd.to_datetime(df['transaction_time'].astype(str)).dt.hour
df['rule_night_time'] = (df['hour'] >= 0) & (df['hour'] <= 5)
df['rule_international'] = (df['is_international'] == 'Yes') & (df['amount'] > 10000)
print(df[['transaction_id', 'amount', 'rule_high_amount', 'rule_new_account', 'rule_night_time', 'rule_international']])
rule_columns = [
    'rule_high_amount',
    'rule_new_account',
    'rule_night_time',
    'rule_international'
]
# Each True = 1 point, False = 0
df['risk_score'] = df[rule_columns].sum(axis=1)
print(df[['transaction_id', 'risk_score']])
def classify_risk(score):
    if score == 0:
        return "Low Risk"
    elif score == 1:
        return "Medium Risk"
    else:
        return "High Risk"
df['risk_level'] = df['risk_score'].apply(classify_risk)
print(df[['transaction_id', 'risk_score', 'risk_level']])
risk_counts = df['risk_level'].value_counts()
print(risk_counts)
rule_trigger_count = df[['rule_high_amount', 'rule_new_account', 'rule_night_time', 'rule_international']].sum()
print(rule_trigger_count)
final_output = df[
    ['transaction_id', 'customer_id', 'amount', 'risk_score', 'risk_level']
]
print(final_output)
final_output.to_csv("fraud_detection_result.csv", index=False)