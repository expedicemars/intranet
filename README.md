# Intranet Expedice Mars

 
## Hosting

- používám hosting na [python anywhere](https://eu.pythonanywhere.com).
- přístupová data mám a můžu je poskytnout, ale hlavní je, že kód je zde na bitbucketu

## Struktura a styl

- Složky jsou strukturovány tak, jak mě to naučili v [tomhle videu v tomhle čase](https://youtu.be/dam0GPOAvVI?t=275)
- Při programování byl používán [PEP 8](https://www.python.org/dev/peps/pep-0008/) styl pro formátování python kódu.
- Komentáře v kódu často vedou k nepřesnostem. Zastarávají a stávají se irelevantními. V případě Pythonu se správně napsaný kód dá číst (s trochou nadsázky) jako kniha. O to se také snažím, tedy dokumentace v kódu místo nemá. Jedinou výjimou jsou TypeHints, které v kódu pomáhají mimojiné nahlédnout na typ proměnných.
- Řada souborů se sama vytváří při spuštění a nejsou součástí version control. Jsou to:
    - instance/database.db
    - user_data
    - data/known_bugs.json
    - data/logs.txt
    - data/faze.json
    - data/mailing_list.json
    - data/terminy.txt
    - data/velitele_odbornosti_data.json
    - data/odkazy.json
    - zadani
- soubor .env se sám nevytváří, je nutné ho založit ručně. Obsahuje secret key k flask appce, jmeno a heslo pro odesilani mailu.

## Spuštění

růčo založit `.env` soubor v root složce, populate SECRET_KEY, MAIL_USERNAME, MAIL_PASSWORD


## Použité knihovny

- instalované přes pip
    - [Flask](https://flask.palletsprojects.com/en/2.0.x/) - framework pro web development
    - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - extension Flasku pro práci s databázemi
    - [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - extension flasku pro podporu přihlašování userů
    - [Requests](https://docs.python-requests.org/en/latest/) - Pro vytváření HTTP requestů a jejich obsahu
    -[PyJWT](https://pyjwt.readthedocs.io/en/stable/) - Pro vytváření Timed tokenů
- součástí standard library:
    - [json](https://docs.python.org/3/library/json.html) - pomáhá správně zapisovat dict proměnné do souborů
    - [typing](https://docs.python.org/3/library/typing.html) - pomáhá mít pořádek v typech proměnných nebo třeba v return values funkcí
    - [pathlib](https://docs.python.org/3/library/pathlib.html) - lepší práce s cestami k souborům než jen "/path/to/file". Hlavně má zaručit funkčnost na různých OS.
    - [datetime](https://docs.python.org/3/library/datetime.html) - pro získávání informací o aktuálním čase
    - [shutil](https://docs.python.org/3/library/shutil.html) - pro manipulaci se složkami a soubory (zde využíváno k odstraňování složek při mazání odhadů)
    - [uuid](https://docs.python.org/3/library/uuid.html) - pro generování Universaly Unique IDentifierů = id odhadů

# Pár slov k rolím

Vedle rolí user a admin je hromada  dalších rolí, které plní svůj účel. Všechny ostatní jsou vždy mutace admina. Omezují, kam admin může a co všechno smí.

Pro přidání admina:
1. Registrace usera.
2. Existující admin s povolením typu editing_admins_allowed vleze do admin prostředí.
3. najde usera a upraví mu role na to, co je třeba.


Pro jmenování prvního admina s rolí editing_admins_allowed:
1. Registrace Usera
2. v Pythonanywhere najít skript "jmenovani_admina_editing_admins_allowed.py"s
3. upravit v něm email_na_jmenovani
4. v konzoli to pustit

# Pár slov k fázím

Expedice mars má (zatím) 4 fáze: 
- otevřená registrace
- zpřístupněné zadání
- uzavřená registrace
- ukončený ročník
Admini s povolením prepinani_fazi_allowed může hru posouvat do dalších fází, nebo zpět, je-li to možné.