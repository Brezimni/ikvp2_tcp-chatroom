# Klepetalnica v terminalu
Preprosta klepetalnica v terminalu, ki uporablja python socket modul za vzpostavitev TCP povezav in threading knjižnico za simultano obravnavanje sporočil več uporabnikov. 

## Funkcionalnosti serverja
Server sprejema ves vhodi promet na vratih, ki jih določimo ob začetku.

### Ukazna vrstica serverja
- ip - Server izpiše svoj ip
- oznani <besedilo> - Server pošlje sporčilo vsem uporabnikom
- odstrani <uporabniško_ime> - Uporabnik je odstranjen iz klepetalnice.
- blokiraj <uporabniško_ime> - Uporabnikov IP je dodan na seznam nezaželenih.
- seznam - Seznam vseh aktivnih in blokiranih uporabnikov.
- izklop - Server zapre socket na katerem posluša.

## Funkcionalnosti clienta

## Inspiracija