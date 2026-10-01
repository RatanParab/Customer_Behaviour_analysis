from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("customer_shopping_behavior.csv")

# a=df.head()

# print(a)

# df.info()
# b=df.describe(include='all')
# print(b)

# c=df.isnull().sum()
# print(c)

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

# c=df.isnull().sum()
# print(c)



# -------

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df= df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

# a=df.columns
# print(a)






# ------ create column age_group

labels = ['Young Adult','Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'],q=4,labels=labels)

# a=df[['age','age_group']].head(10)
# print(a)




# ---- create column purchase frequency days

frequency_mapping = {'Fortnightly': 14,
                     'Weekly': 7,
                     'Monthly':30,
                     'Quarterly': 90,
                     'Bi-Weekly': 14,
                     'Annually': 365,
                     'Every 3 Months':90
                     }

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

# a=df[['purchase_frequency_days','frequency_of_purchases']].head(10)
# print(a)




# ----- discount / coupon

# for checking both containing same values bcz when coupon used we got discount

# a=(df['discount_applied']==df['promo_code_used']).all()
# print(a)


# both are same so drop one of them 
df = df.drop('promo_code_used',axis=1)





# ------for saving changes in file 
# df.to_csv("cleaned_shopping_behaviour.csv", index=False)



# username = "postgres"
# password = "Ratan@123"
# host = "localhost"
# port = "5433"
# database = "customer_behaviour"

# engine= create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# table_name = "customer"
# df.to_sql(table_name,engine,if_exists="replace",index=False)

# print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")



username = "postgres"
password = "Ratan@123"
host = "localhost"
port = 5433
database = "customer_behavior"

connection_url = URL.create(
    "postgresql+psycopg2",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(connection_url)

table_name = "customer"

df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")