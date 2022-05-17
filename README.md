# Šablona stránek

Máš tu funkční stránky s login, admin a bugtracking systémem.

## Zakládání všeho

### Dostat věci na bitbucket
1. Založit repo na bitbucketu
2. zkopírovat SSH adresu (něco jako git@bitbucket.org:piipecek/sablona.git)
3. git init v mé složce na lokálu
4. git remote add origin \<SSH adresa\>
5. git push -u origin master

### Subdoména

1. Forpsi -> administrace -> domény -> klik na moojí (asi piipovostranky.cz) -> editace DNS záznamů
2. Na pythonanywhere zalozit novou app, dostat z ni cname
3. nový DNS záznam: typ CNAME, napsat subdomenu, paste CNAME

### Rozeběhnout app na python anywhere

1. `git clone` do PA do normalne nejvyssi slozky (vytvori to svoji slozku na repo)
2. `cd` in
3. `mkvirtualenv ENV_JMENO --python='/usr/bin/python3.9'`
4. `pip install -r requirements.txt`
5. Na webabb stránce
- do virtualenv napsat to jmeno virtual_envu
- working environment do slozky s repem
- do code/source code napsat tu samou slozku
-WSGI: ve Flask sekci uncommentnout:
  - import sys
  - path = 
  - ten if block
  - dal: `from website import create_app`
  - `application = create_app()`

- Force HTTPS on
- HTTPS certificate - auto Let's encrypt




## Hosting

- používám hosting na [python anywhere](https://eu.pythonanywhere.com).
- přístupová data mám a můžu je poskytnout, ale hlavní je, že kód je zde na bitbucketu

## Struktura a styl

- Složky jsou strukturovány tak, jak mě to naučili v [tomhle videu v tomhle čase](https://youtu.be/dam0GPOAvVI?t=275)
- Při programování byl používán [PEP 8](https://www.python.org/dev/peps/pep-0008/) styl pro formátování python kódu.
- Komentáře v kódu často vedou k nepřesnostem. Zastarávají a stávají se irelevantními. V případě Pythonu se správně napsaný kód dá číst (s trochou nadsázky) jako kniha. O to se také snažím, tedy dokumentace v kódu místo nemá. Jedinou výjimou jsou TypeHints, které v kódu pomáhají mimojiné nahlédnout na typ proměnných.
- Řada souborů se sama vytváří při spuštění a nejsou součástí version control. Jsou to:
  - known_bugs.json
  - website/database.db
  - logs.txt
  - user_data

## Použité knihovny

- instalované přes pip
  - [Flask](https://flask.palletsprojects.com/en/2.0.x/) - framework pro web development
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - extension Flasku pro práci s databázemi
  - [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - extension flasku pro podporu přihlašování userů
  - [Requests](https://docs.python-requests.org/en/latest/) - Pro vytváření HTTP requestů a jejich obsahu
- součástí standard library:
  - [json](https://docs.python.org/3/library/json.html) - pomáhá správně zapisovat dict proměnné do souborů
  - [typing](https://docs.python.org/3/library/typing.html) - pomáhá mít pořádek v typech proměnných nebo třeba v return values funkcí
  - [pathlib](https://docs.python.org/3/library/pathlib.html) - lepší práce s cestami k souborům než jen "/path/to/file". Hlavně má zaručit funkčnost na různých OS.
  - [datetime](https://docs.python.org/3/library/datetime.html) - pro získávání informací o aktuálním čase
  - [shutil](https://docs.python.org/3/library/shutil.html) - pro manipulaci se složkami a soubory (zde využíváno k odstraňování složek při mazání odhadů)
  - [uuid](https://docs.python.org/3/library/uuid.html) - pro generování Universaly Unique IDentifierů = id odhadů
- [Stl JS Plugin](https://www.viewstl.com/plugin/#p_models) - pro zobrazování .stl souborů


## Local build

bohužel neumím přesně syntax příkazů, tak to popíšu slovy:

Pro spuštění flask serveru je potřeba

- mít local verzi tohoto repa
- mít naistalovaný Python a pip
- pomocí pip instalovat všechny knihovny v requirements.txt
- spustit skript main.py

## Pro přístě

- pro správné nastavení Python anywhere WSGI aplikace doporučuju [tohle video](https://youtu.be/5jbdkOlf4cY)
- na [tomhle čase](https://youtu.be/dam0GPOAvVI?t=4367) mě naučili login support
- úprava SQLite databaze z terminalu:
sqlite 3
.open database.db -rw
DELETE FROM user WHERE id=6;

- zjištění IP místo CNAME: v pythonanywhere přejmenuju app na joseflat.eu.pythonanywhere.com a v nějakym online IP lookupu to lookupnu