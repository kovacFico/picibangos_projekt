# POSTAVLJANJE VIRTUALNOG OKRUZENJA:
Prije svega instaliraj virtualni env. da djabe ne zagadjujes uredjaj sa paketima:
1. otvori terminal u folderu projekta
2. pokreni naredbu "python -m venv env" gdje ti je "env" dio naziv tog virtualnog okruzenja
    tj. da pise "python -m venv okrug_zenica", okrug_zenica bi bio naziv foldera gdje je virtualka


# POSTAVLJANJE GITA i PRE-COMMITA:
Postavljas git u virtualki:
1. odes u folder gdje si instalirao virtualni env., tj u folder gdje se nalazi folder od virtualke nazvan "okrug_zenica"
2. pokrenes naredbu "source ./okrug_zenica/bin/activate" i pokrenut ce se virtualni env.
3. odvali nakon "git init"
4. te na kraju postavljas pre-commit za flake i one ostale alate koji ce provjeriti kod jeli dobro napisan, sa
    naredbom "pre-commit install" koju pokrenes u virtualnom okruzenju nakon sto kloniras repo sa gita


# DA BI INSTALIRAO SVE POTREBNE DEPENDENCIE ZA RAD ODVALI "pip install -r backend/requirements.txt"


# POSTAVLJANJE MIGRACIJA BAZE:
Da bi mogao samo updateati bazu kao neki folder u git, koristi se taj almbic. Ukratko sa njime ako promjenis
nesto u tablici ili nadodas novi stupac, samo pokrenes taj alembic i on postavi bazu na tu novu konfiguraciju,
pa tako mozes HEAD od verzije baze (kao u gitu) vracati na stare verzije i vratiti staru konfiguraciju i slicno...
Ukratko git za baze. Pa kako:
1. kada si pokrenuo "pip install -r requirements.txt" da bi se instalirali svi potrebni dependency, AKO SI PROMJENIO
    NEKI OD MODELA BAZE, pokrenes "alembic revision --autogenerate -m "poruka koja objasnjava sta se dodalo" i baza ce se
    postaviti na novu verziju, ali samo u kodu
2. da bi postavio na novu verziju u pgadminu moras pokrenuti naredbu "alembic upgrade head" no mozda nekada nece jer alembic
    sam po sebi ne zna kojim redosljedom rusiti tablice, pa krene rusiti npr. od vrha tj. od tablice usera, a ostale tablice imaju
    imaju foreign key sa userom, pa se treba namjestiti da prvo srusi ove ovisne, pa na kraju usera. To namjestas tako sto odes
    u "alembic" folder, pa u "versions" te otvoris file sa tom verzijom i pod funkcijom "uppgrade" sredis redosljed kojim ces
    rusiti tablice


# !!!PAZI!!!
            - da bi mogao raditi te migracije moras postaviti .env file gdje ces napisati detalje o bazi koji ce se
             spojiti u njezin url, a to ti izgleda ovako:
                POSTGRES_USER=(naziv uloge koju si napravio u pgadminu, uglavnom je to postgres jer je on superuser)
                POSTGRES_PASSWORD=(sifra za tu ulogu)
                POSTGRES_SERVER=localhost
                POSTGRES_PORT=5432
                POSTGRES_DB=(naziv baze u pgadminu)

# SADA PAR OBJAŠNJENJA:
1. razlog za ovakav stil programiranja je "separation of concerns" gdje odvajamo bussinses logiku i orm logiku baze
