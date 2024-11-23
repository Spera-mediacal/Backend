# Spera

## How to run it

```
git clone https://github.com/Spera-mediacal/Backend
cd Backend
```

```
docker build spera .
```

```
docker run -d --name spera -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -p 33060:33060 spera
```

```
uvicorn main:app --reload
```