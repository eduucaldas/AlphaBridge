## Data: parsing des .lin, création d'un Dataframe pandas, recherche de bidding
### Parsing & Dataframe
Il faut que les lins soient dans le dossier ./data/deals/
```python
from data.parser import parse_deal
from data.parser import create_dataframe
fram data.paser import save_df

data = parse_deal()
df = create_dataframe(data)
save_df(df, "store.hdfs")
```

### Recherche de bidding
```python
from data.parser import search_bidding

BIDDING = "1N,P,P,P"
df = search_bidding(BIDDING)

>> df.iloc[0]
east      [11.0, 9.0, 2.0, 20.0, 18.0, 17.0, 37.0, 35.0,...
lead                                                     51
leader    [12.0, 7.0, 1.0, 0.0, 25.0, 16.0, 13.0, 33.0, ...
north     [10.0, 6.0, 4.0, 3.0, 24.0, 22.0, 19.0, 15.0, ...
south     [8, 5, 23, 21, 14.0, 34.0, 31.0, 29.0, 27.0, 2...
west      [12.0, 7.0, 1.0, 0.0, 25.0, 16.0, 13.0, 33.0, ...
Name: 0, dtype: object
```
