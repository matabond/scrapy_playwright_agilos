# Note: the module name is psycopg, not psycopg3
import psycopg
import re

cijenaEUR='(10,62 EUR)'
cijenaEUR=re.findall(r"\d+\,\d*", cijenaEUR)[0].replace(',','.')
print(cijenaEUR)

# Connect to an existing database
with psycopg.connect("dbname=scraping user=postgres password=mysecretpassword host=localhost port=5432") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        print(cur)
        # Execute a command: this creates a new table
        # cur.execute("""
        #     CREATE TABLE test (
        #         id serial PRIMARY KEY,
        #         num integer,
        #         data text)
        #     """)

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        # cur.execute(
        #     "INSERT INTO public.rog_joma(source_link, cijena_hrk, cijena_eur, url, opis, kategorija, slika_url, ime_artikla) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        #     ('source_link', 2.1, 0.5, 'url', 'opis', 'kategorija', 'slika_url', 'ime_artikla'))
        # conn.commit()
        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM public.rog_joma")
        cur.fetchmany()
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(record)

        # Make the changes to the database persistent
        # conn.commit()