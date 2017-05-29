from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import scipy.ndimage.filters
import datetime as dt
import random
import pandas as pd
import django

data = pd.read_csv('data_train.csv', sep=";")
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].map(dt.date.toordinal)
print(df['spent_money'])

X_train = df[['date']]
Y_train = df['spent_money']

# wczytanie danych testowych

data2 = pd.read_csv('data_test.csv', sep=";")
df2 = pd.DataFrame(data2)
df2['date'] = pd.to_datetime(df2['date'])
df2['date'] = df2['date'].map(dt.date.toordinal)

X_test = df2[['date']]
Y_test = df2['spent_money']

def showplot(response):
    plt.figure(figsize=(9, 4))
    plt.plot(X_train, Y_train, color='green')
    plt.xticks((df['date'][::48]),(df['date'].map(dt.date.fromordinal)[::48]))

    fig = plt.gcf()
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response

def prediction(response):
    plt.figure(figsize=(9, 4))
    # wczytanie danych uczących
    pred = LinearRegression()
    pred.fit(X_train, Y_train)  # uczenie modelu
    print('Współczynnik: \n', pred.coef_)
    plt.scatter(X_train, Y_train, color='green')  # dane wejściowe

    filtered = scipy.ndimage.filters.gaussian_filter1d(Y_train.get_values(), sigma=10)

    plt.plot(X_train, filtered, color='red')
    plt.plot(X_test[:350], pred.predict(X_test[:350]), color='blue')  # linia trendu
    plt.plot(X_test[350::], pred.predict(X_test[350::]), color='purple')  # predykcja linii trendu

    Y_pred = pred.predict(X_test)

    for i in range(Y_pred.size):
        Y_pred[i] *= random.randint(1,225)/100

    plt.scatter(X_test[350::], Y_pred[350::], color='black', label='Dane prognozowane')
    plt.xticks((df2['date'][::90]), (df2['date'].map(dt.date.fromordinal)[::90]))

    fig = plt.gcf()
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def coefficient(response):
    pred = LinearRegression()
    pred.fit(X_train, Y_train)

    return pred.coef_
