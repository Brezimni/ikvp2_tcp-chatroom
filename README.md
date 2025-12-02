# Klepetalnica v terminalu
Preprosta klepetalnica v terminalu, ki uporablja python socket modul za vzpostavitev TCP povezav in threading knjižnico za simultano obravnavanje sporočil več uporabnikov. 

## Funkcionalnosti serverja
Server sprejema ves vhodi promet na vratih, ki jih določimo ob začetku in jih preusmerja na ustrezne cliente.

### Ukazna vrstica serverja
- [x] ip - Server izpiše svoj ip
- [x] oznani <besedilo> - Server pošlje sporčilo vsem uporabnikom
- [x] odstrani <uporabniško_ime> - Uporabnik je odstranjen iz klepetalnice.
- [x] blokiraj <uporabniško_ime> - Uporabnikov IP je dodan na seznam nezaželenih.
- [x] izpis - Server zapre socket na katerem posluša.

## Funkcionalnosti clienta
Lahko pošilja broadcast sporočila drugim, ki so povezani na server.

### Dodatni ukazi
- [x] ::p <uporabniško_ime> <sporočilo> - Pošlje zasebno sporočilo uporabniku.
- [x] ::ime <novo_uporabniško_ime> - Spremeni uporabniško ime, če je tako še na voljo.
- [x] seznam - Seznam vseh aktivnih in blokiranih uporabnikov.
- [x] ::izpis - Client prekine povezavo s strežnikom.

## Inspiracija
[Simple TCP Chatroom in Python - NeutralNine](https://www.youtube.com/watch?v=3UOyky9sEQY)