## Gezinomi Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama

import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: '%.2f' % x)
df = pd.read_excel('miuul_gezinomi.xlsx') #veri dosyasını okutma
print(df.head())  #Veri seti ile ilgili genel bilgiler
print(df.shape)
print(df.info())

# Unique şehirler ve frekansların bulunması
df['SaleCityName'].nunique()

#Hangi Concept'den kaçar tane satış olmuştur ?
df['ConceptName'].value_counts()

#Şehirlere göre satışlaran toplam ne kadar kazanılmış ?
df.groupby('SaleCityName').agg({'Price': "sum"})

#Concept türlerine göre ne kadar kazanılmış ?
df.groupby("ConceptName").agg({'Price': "sum"})

#Şehirlere göre PRICE ortalamaları nedir ?
df.groupby(by=['SaleCityName']).agg({'Price': "mean"})

#Conceptlere göre PRICE ortalamaları nedir ?
df.groupby(by=['ConceptName']).agg({'Price': "mean"})

#Şehir-Concept kırılımında PRICE ortalamaları nedir ?
df.groupby(by=['SaleCityName', 'ConceptName']).agg({'Price': "mean"})

###############################################################################

#satis_checkin_day_diff değişkenini EB_Score adında yeni bir kategorik değişkene çeviriniz.

bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = ['Last Minuters', 'Potentiel Planners', 'Planners', 'Early Bookers']

df['EB_Score'] = pd.cut(df['SaleCheckInDayDiff'], bins, labels=labels)
df.head(50).to_excel('eb_scorew.xlsx', index=False)


#Şehir,Concept,[EB_Score,Sezon,CInday] kırılımında ücret ortalamalarını ve frekanslarını bulun.

#Şehir,Concept,EB_Score kırılımında ücret ortalamaları
df.groupby(by=['SaleCityName', 'ConceptName', 'EB_Score']).agg({'Price': ["mean", "count"]})

#Şehir-Concept-Sezon kırılımında ücret ortalamaları
df.groupby(by=['SaleCityName', 'ConceptName', 'Seasons']).agg({'Price': ["mean", "count"]})

#Şehir-Concept,CInday kırılımında ücret ortalamaları
df.groupby(by=['SaleCityName','ConceptName', 'CInDay']).agg({'Price': ["mean", "count"]})


###############################################################################

#City-Concept-Season kırılımın çıktısını PRICE'a göre sıralayınız.

agg_df = df.groupby(['SaleCityName', 'ConceptName', 'Seasons']).agg({'Price': "mean"}).sort_values('Price', )
agg_df.head(20)

#Indexte yer alan isimleri değişken ismine çevirme

agg_df.reset_index(inplace=True)

agg_df.head()


#Yeni level based satışları tanımlama ve veri setine değişken olarak ekleme

agg_df['sales_level_based'] = agg_df[['SaleCityName', 'ConceptName', 'Seasons']].agg(lambda x: '_'.join(x).upper(), axis=1)


#Personelleri segmentlere ayırma

agg_df['SEGMENT'] = pd.qcut(agg_df['Price'], 4, labels=["D", "C", "B", "A"])
agg_df.head(10)
agg_df.groupby('SEGMENT').agg({'Price': ["mean", "max", "sum"]})

#"Antalya her şey dahil high" hangi segmenttedir ve ne kadar ücret beklenmektedir ?
agg_df.sort_values(by='Price')
new_user = "ANTALYA_HERSEY_DAHIL_HIGH"
agg_df[agg_df['sales_level_based'] == new_user]
