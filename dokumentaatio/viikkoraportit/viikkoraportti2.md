# Viikkoraportti 2

Aloitin käyttöliittymän luomista tällä viikolla. Tutustuin Shunting yard algoritmiin lisää ja lisäsin myös laskimelle perustoiminnallisuutta. Laskimella voidaan laskea peruslaskutoimituksia (käyttäen operaattoreita +, -, × ja ÷, ja sulkeita). Laskin toimii niin, että se tokenisoi annetun matemaattisen lausekkeen ja kääntää sen infix-muodosta RPN/postfix-muotoon, josta lausekkeen arvo saadaan laskettua. Luodulle toiminnallisuudelle on myös luotu yksinkertaisia yksikkötestejä, joita on tarkoitus laajentaa myöhemmin. 

Laskin ei kuitenkaan huomioi virheellisiä matemaattisia lausekkeita tällä hetkellä. Laskin toimii lisäksi vain positiivisten lukuarvojen kanssa, ja se on ongelma, jota työstän tällä hetkellä. Ajattelin, että järkevin ratkaisu tähän on uudelleenmuotoilla laskimen syöte ennen syötteen tokenisoimista, mutta en ole vielä varma miten. Kun saan ongelman ratkaistua, lisään joko virheilmoituksia virheellisille syötteille tai lisätoiminnallisuuksia laskimelle, kuten sqrt, sin, cos, tan, yms.. 

Käytin harjoitustyöhön noin 11-12 tuntia tällä viikolla.
