# Autolx - IP 2019

Imitatie de autovit de cea mai buna calitate

## Clonare Proiect

Din linia de comanda, prin https:

```bash
git clone https://github.com/ionut97/ip-2019.git
```


## Setup

*Instalare python 3 + django*:

[Django Quick Install](https://docs.djangoproject.com/en/2.1/intro/install/)

*IDE*:

[PyCharm Community](https://www.jetbrains.com/pycharm/download/)

Baza de date default este SQLite, nu este nevoie de alte drivere instalate.

*Client pentru lucrul baze de date sqlite*:

[DB Browser for SQLite](https://sqlitebrowser.org/)

*Din linia de comanda, intram in directorul cu proiectul*:
```bash
cd ip-2019
```

*Instalare dependente*:
```bash
pip install -r requirements.txt
```

*Creare modele*:
```bash
python manage.py makemigrations web_app
```

*Aplica modificari*:
```bash
python manage.py migrate
```

## Verificare


```bash
python manage.py runserver
```

Daca totul functioneaza, o sa avem un server web la adresa: [http://127.0.0.1:8000/](http://127.0.0.1:8000)
