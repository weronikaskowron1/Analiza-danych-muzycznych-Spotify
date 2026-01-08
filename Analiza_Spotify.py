#!/usr/bin/env python
# coding: utf-8

# ## Wstęp

# Źródło danych: https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.kaggle.com%2Fdatasets%2Fparadisejoy%2Ftop-hits-spotify-from-20002019%2Fdata%3Ffbclid%3DIwZXh0bgNhZW0CMTAAYnJpZBEwR0k3NlBiMDl1SEFNUTJ0QnNydGMGYXBwX2lkEDIyMjAzOTE3ODgyMDA4OTIAAR4RXm7EyUq5-gUyFkNl5mdVT32_YebOxoA9BlcB10BncWMMc6bMZMfCi1JXuw_aem_anx_r8gNiTOF5Twb-l6leQ&h=AT3Us8mOSIL-bnJb-SDnY1WBHEjfo7DlUTn5wMiFjlrWb-Wgm9PpfSQNmTzuki36R9FLrvz5YPCXYGnZwby8PrXeboRPmcTpeJnNy6FsaeFsb-XelLHgFz0_Ltlt7h542NHiDQ
# 
# Baza danych zawiera informacje o utworach muzycznych, w której znajdują się następujące kolumny:
# - **artist** - nazwa wykonawcy  
# - **song** - tytuł utworu  
# - **duration_ms** - długość utworu w milisekundach  
# - **explicit** - czy utwór zawiera treści wulgarne  
# - **year** - rok wydania  
# - **popularity** - popularność utworu  
# - **danceability** - wskaźnik taneczności  
# - **energy** - poziom energii  
# - **key** - tonacja utworu  
# - **loudness** - głośność  
# - **mode** - tryb (durowy/molowy)  
# - **speechiness** - stopień "mówionego" charakteru utworu  
# - **acousticness** - prawdopodobieństwo akustyczności  
# - **instrumentalness** - udział elementów instrumentalnych  
# - **liveness** - wskaźnik nagrania na żywo  
# - **valence** - poziom pozytywności utworu  
# - **tempo** - tempo
# - **genre** - gatunek muzyczny  

# ## Wczytywanie bibliotek oraz przygotowanie środowiska

# In[1]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from bokeh.io import output_notebook
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, show
import seaborn as sns
sns.set_style("darkgrid")
plt.rcParams["figure.autolayout"] = True


# ## Wczytanie danych

# In[2]:


df=pd.read_csv("songs_normalize.csv")
df.head()


# ## Struktura danych

# In[3]:


df.info()


# ## Sprawdzanie i usuwanie duplikatów

# In[4]:


duplicated_rows = df.duplicated()
print(duplicated_rows[duplicated_rows == True].sum())

df = df.drop_duplicates()
duplicated_rows = df.duplicated()
print(duplicated_rows[duplicated_rows == True].sum())


# ## Usuwanie pustych wierszy

# In[5]:


df=df.dropna()
df.isnull().sum()


# ## Statystyki zmiennych numerycznych

# In[6]:


df.describe()


# ## Wykresy

# In[7]:


fig, ax = plt.subplots(figsize=(20,10))
artysci = df["artist"].value_counts().head(50)
sns.barplot(x=artysci.index, y=artysci.values,hue=artysci.index, palette="Set2", ax=ax)
ax.tick_params(axis='x', rotation=90)
ax.set_title("50 artystów z największą ilością piosenek", fontsize = 35)
ax.set_xlabel("Artysta", fontsize = 25)
ax.set_ylabel("Liczba utworów", fontsize = 25)
ax.tick_params(axis='both', labelsize=17)
plt.show()


# In[8]:


fig, ax = plt.subplots(figsize=(16,7))
gatunki_lista = df["genre"].str.split(",").explode().str.strip()
gatunki = gatunki_lista.value_counts()
gatunki = gatunki.drop("set()", errors="ignore")
sns.barplot(x=gatunki.index, y=gatunki.values,hue=gatunki.index, palette="Set2", ax=ax)
ax.set_title("Gatunki oraz ich występowanie", fontsize = 30)
ax.set_xlabel("Gatunek", fontsize = 20)
ax.set_ylabel("Liczba utworów", fontsize = 20)
ax.tick_params(axis='x', rotation=90)
ax.tick_params(axis='both', labelsize=14)
plt.show()


# In[9]:


artysci_popularnosc=df.groupby("artist")["popularity"].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(16,7))
sns.barplot(x=artysci_popularnosc.index, y=artysci_popularnosc.values,hue=artysci_popularnosc.index, palette="Set2", ax=ax)
ax.set_title("Najpopularniejsi artyści", fontsize = 30)
ax.set_xlabel("Artysta", fontsize = 20)
ax.set_ylabel("Popularność 0-100", fontsize = 20)
ax.tick_params(axis='x', rotation=90)
ax.tick_params(axis='both', labelsize=14)
plt.show()


# In[10]:


ciemny = df[(df["valence"] >= 0.0) & (df["valence"] <= 0.3)]
sredni = df[(df["valence"] > 0.3) & (df["valence"] <= 0.6)]
jasny = df[(df["valence"] > 0.6) & (df["valence"] <= 1.0)]
ilosc = [len(ciemny), len(sredni), len(jasny)]
opisy = ["Smutny,cieżki (0.0–0.3)", "Neutralny (0.4–0.6)", "Pozytywny,radosny (0.7–1.0)"]
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x=opisy, y=ilosc,hue=opisy, palette="Set2", ax=ax)
ax.set_title("Rozkład utworów według valence", fontsize = 20)
ax.set_ylabel("Liczba utworów", fontsize = 15)
ax.tick_params(axis='both', labelsize=11)
plt.show()


# In[11]:


tonacja_liczba = df["key"].value_counts()
fig, ax = plt.subplots(figsize=(16,7))
sns.barplot(x=tonacja_liczba.index, y=tonacja_liczba.values,hue=tonacja_liczba.index,legend=False, palette="Set2", ax=ax)
ax.set_title("Rozkład utworów według tonacji", fontsize = 30)
ax.set_xlabel("Tonacja", fontsize = 20)
ax.set_ylabel("Liczba utworów", fontsize = 20)
ax.tick_params(axis='both', labelsize=15)
plt.show()


# In[12]:


artysci_wartosci = (df.groupby("artist")[["danceability", "energy", "valence","popularity"]].mean().sort_values("popularity", ascending=False)).head(10)
artysci_wartosci = artysci_wartosci.drop(columns="popularity")
artysci_wartosci_long = artysci_wartosci.reset_index().melt(id_vars="artist",var_name="Cecha",value_name="Wartość")
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=artysci_wartosci_long,x="Wartość",y="artist",hue="Cecha",palette="Set2",ax=ax)
ax.set_title("Średnie cechy muzyczne dla 10 najpopularniejszych artystów", fontsize = 20)
ax.set_ylabel("Artysta", fontsize = 15)
ax.set_xlabel("Wartość", fontsize = 15)
plt.show()


# In[13]:


plt.figure(figsize=(10,6))
sc = plt.scatter(df["energy"], df["danceability"],c=df["key"],alpha=0.7, cmap = "Set2")
cbar = plt.colorbar(sc)
cbar.set_label("Tonacja", fontsize=15)
plt.xlabel("Energia", fontsize = 15)
plt.ylabel("Taneczność", fontsize = 15)
plt.title("Zależność, energii, taneczności i tonacji", fontsize = 20)
plt.show()


# In[14]:


fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=df, x='loudness', y='tempo', hue='valence', palette='Set2',legend=False, alpha=0.7)
sm = plt.cm.ScalarMappable(cmap='Set2')
sm.set_array(df["valence"])
cbar = fig.colorbar(sm, ax=ax, orientation="vertical")
cbar.set_label("Valence", fontsize = 15)
ax.set_title("Zależność tempa, głośności i valence", fontsize = 20)
ax.set_xlabel("Głośność", fontsize = 15)
ax.set_ylabel("Tempo", fontsize = 15)
plt.show()


# ## Top hity w latach 1998–2020

# In[15]:


najpopularniejsza_piosenka=df.loc[df.groupby("year")["popularity"].idxmax(),["year","artist","song","popularity"]].sort_values("year",ascending=True)
set2_colors = sns.color_palette("Set2", 8).as_hex()
najpopularniejsza_piosenka.style.set_caption("Top hitów Spotify lata 1998–2020") \
    .background_gradient(subset=["year"], cmap=sns.color_palette("Set2", as_cmap=True)) \
    .map(lambda x: "background-color: lavender", subset=["popularity"]) \
    .format({"popularity": "{:.0f}"})


# ## Najpopularniejsze utwory artystów, którzy mają co najmniej 10 piosenek

# In[16]:


liczba_piosenek=df['artist'].value_counts()
wiele = liczba_piosenek[liczba_piosenek > 10].index
najpopularniejsza = df.loc[(df[df["artist"].isin(wiele)].groupby("artist")["popularity"].idxmax()),["artist","song"]]
najpopularniejszTabelka = (
    najpopularniejsza.style
        .set_caption("Najpopularniejsze utwory artystów, którzy mają co najmniej 10 piosenek")
        .map(lambda x: "background-color: lavender", subset=["song"]))
najpopularniejszTabelka


# In[17]:


czy_explicit = df["explicit"].value_counts()
plt.figure(figsize = (10,6))
plt.pie(czy_explicit, labels = ["Explicit", "Non-explicit"], explode = [0.05, 0.05],  autopct = lambda p: f"{int(p/100*czy_explicit.sum())} utworów\n({p:.1f}%)",  colors = ['#8da0cb', '#a6d854'], shadow=True, startangle=200, textprops={'fontsize': 15})
plt.title("Explicit vs. non-explicit – rozkład utworów", fontsize = 20)
plt.show()


# ## Najdłuższa, najkrótsza piosenka oraz średnia trwania utworów

# In[18]:


df['duration_min']=(df['duration_ms']/60000).round(2)

najdluzsza_piosenka=df.loc[df['duration_min'].idxmax(),["artist","song","duration_min"]]
najkrotsza_piosenka=df.loc[df['duration_min'].idxmin(),["artist","song","duration_min"]]
sredni_czas=(df['duration_ms'].mean()/60000).round(2)

tabela = pd.DataFrame([{
        "Typ": "Najkrótsza piosenka",
        "Artysta": najkrotsza_piosenka["artist"],
        "Utwór": najkrotsza_piosenka["song"],
        "Czas [min]": najkrotsza_piosenka["duration_min"]},
    {
        "Typ": "Najdłuższa piosenka",
        "Artysta": najdluzsza_piosenka["artist"],
        "Utwór": najdluzsza_piosenka["song"],
        "Czas [min]": najdluzsza_piosenka["duration_min"]},
    {
        "Typ": "Średnia",
        "Artysta": "-",
        "Utwór": "-",
        "Czas [min]": sredni_czas}])

TabelaCzas = (tabela.style
        .set_caption("Czasy trwania utworów Spotify")
        .background_gradient(subset=["Czas [min]"], cmap=sns.color_palette("Set2", as_cmap=True))
        .format({"Czas [min]": "{:.2f}"}))

TabelaCzas


# ## Interaktywny wykres liczby wydanych utworów danego artysty w zależności od przedziału lat

# In[19]:


output_notebook()
artysci = artysci.head(10)
top10_artists = artysci.index.tolist()
df_top10 = df[df['artist'].isin(top10_artists)]
utwory_lata = df_top10.groupby(["artist", "year"]).size().reset_index(name="song_count")
colors = sns.color_palette("Set2", len(top10_artists)).as_hex()

source = ColumnDataSource(data=dict(artist=top10_artists,song_count=[0]*len(top10_artists),color=colors))

plot = figure(x_range=top10_artists, width=800, height=400,
              title=f"Ilość piosenek danego artysty od {df['year'].min()} do {df['year'].max()} roku",
              y_axis_label="Łączna liczba piosenek")

plot.vbar(x='artist', top='song_count', width=0.8,source=source, fill_color='color')

start_slider = Slider(start=df["year"].min(), end=df["year"].max(),value=df["year"].min(), step=1, title="Początkowy rok")
end_slider = Slider(start=df["year"].min(), end=df["year"].max(),value=df["year"].max(), step=1, title="Końcowy rok")

callback = CustomJS(args=dict(source=source,start=start_slider,end=end_slider,
                              full_artists=utwory_lata["artist"].tolist(),
                              full_years=utwory_lata["year"].tolist(),
                              full_counts=utwory_lata["song_count"].tolist(),
                              top10=top10_artists,
                              plot=plot),
    code="""
    const s = start.value, e = end.value;
    const artists = full_artists, years = full_years, counts = full_counts;

    const agg = {};
    top10.forEach(a => agg[a] = 0);

    for (let i = 0; i < artists.length; i++) {
        if (years[i] >= s && years[i] <= e) {
            agg[artists[i]] += counts[i];
        }t
    }

    source.data = {
        artist: top10,
        song_count: top10.map(a => agg[a]),
        color: source.data['color']   // kolory zostają bez zmian
    };
    source.change.emit();

    plot.title.text = `Ilość wydanych piosenek danego artysty od ${s} do ${e} roku`;
""")

start_slider.js_on_change('value', callback)
end_slider.js_on_change('value', callback)

show(row(plot, column(start_slider, end_slider)))


# In[ ]:




