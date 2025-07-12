# Määrittelydokumentti

Projektin dokumentaatio kirjoitetaan suomeksi, mutta koodi englanniksi. Käytän projektin ohjelmointikielenä Pythonia, ja hallitsen pelkästään Pythonia niin, että voisin vertaisarvioimaan muita projekteja. Kuulun tietojenkäsittelytieteen kandidaattiohjelmaan.

## Projektin kuvaus

### Aihe 

Projektin tarkoituksena on rakentaa tieteellinen laskin, joka laskee annetun matemaattisen lausekkeen arvon. Annettu lauseke eli ohjelman saama syöte voi sisältää lukuarvoja, peruslaskutoimituksia ja joitakin funktioita, kuten sqrt, sin, min ja max. Laskin ei laske virheellisiä lausekkeita ja antaa käyttäjälle virheilmoituksen, jos lauseke on virheellinen. 

### Toteutus

Työssä tullaan käyttämään Shunting yard algoritmia ja pinoja, sekä todennäköisesti myös sanakirjoja ja listoja. 

Ohjelma saa syötteeksi matemaattisia lausekkeita infix-muodossa (esim. 3 + 4), jonka se jäsentää Shunting yard algoritmin avulla. Lauseke jaetaan tokeneihin ja järjestetään tämän jälkeen postfix-muotoon, jonka avulla voidaan laskea lausekkeen arvo. Shunting yard algoritmi ei kuitenkaan suodata virheellisiä matemaattisia lausekkeita, joten tälle ongelmalle täytyy löytää erillinen ratkaisu.

Shunting yard algoritmin aikavaativuus on O(n), joten näitä algoritmeja ja tietorakenteita käyttäen, tavoitteena on, että ohjelman aikavaativuus olisi O(n). Tilavaativuuden tulisi myös olla O(n), ottaen huomioon, että pinot ovat ohjelman keskiössä.

### Ydin

Projektin ytimenä on Shunting yard algoritmin toteuttaminen ja sen hyödyntäminen matemaattisten lauseiden laskentaan. Tavoitteena on tunnistaa virheelliset syötteet ja laskea hyväksytyt syötteet oikein. 

## Lähteet

Alla on listattu ainakin osa niistä lähteitä, joita tulen käyttämään projektin aikana.

[Shunting yard algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)
[Shunting yard algorithm (Emory Oxford College)](https://mathcenter.oxford.emory.edu/site/cs171/shuntingYardAlgorithm/)
[Reverse Polish notation (Wikipedia)](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
[Parsing (Wikipedia)](https://en.wikipedia.org/wiki/Parsing)
[Stack in Python (Geeks for Geeks)](https://www.geeksforgeeks.org/python/stack-in-python/)
[Stacks in Python (W3Schools)](https://www.w3schools.com/python/python_dsa_stacks.asp)
[Tkinter dokumentaatio](https://docs.python.org/3/library/tkinter.html)
