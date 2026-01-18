# NB.01 – Wahlkampf mit Naive Bayes

Der Klassifikator arbeitet, indem er zunächst aus den Trainingsdaten die
Grundwahrscheinlichkeiten (vor merkmalen) der Kandidaten sowie die bedingten
Wahrscheinlichkeiten der einzelnen Merkmale für jeden Kandidaten schätzt.
Dabei wird angenommen, dass die Merkmale gegeben die Klasse unabhängig
voneinander sind.  
Für einen neuen Wähler berechnet der Klassifikator für jeden Kandidaten das
Produkt aus der Grundwahrscheinlichkeit und den bedingten
Wahrscheinlichkeiten der beobachteten Merkmale.  
Der Kandidat mit der höheren Wahrscheinlichkeit
wird anschließend ausgewählt.



## NB.02 – Textklassifikation mit Naive Bayes (Antwortsätze)

### Was sind mögliche Merkmale?

Als Merkmale eignen sich Wort- bzw. n-Gramm-Häufigkeiten aus dem Text der E-Mails.  
Dazu wird ein Bag-of-Words-Modell verwendet, bei dem jede E-Mail als Vektor von Wortzählungen dargestellt wird.  
Typische Vorverarbeitungsschritte sind Kleinschreibung, Entfernen von Stopwörtern und  die Nutzung von Unigrammen und Bigrammen (z.B "Das - ist", "ein Beispiel,..."), um häufige Wortkombinationen abzubilden.

---

### Wie sieht der Klassifikator aus und was sind die wichtigsten Begriffe für spam bzw. ham?
Der Klassifikator ist ein Multinomial Naive Bayes, der auf Bag-of-Words-Features trainiert wurde.  
Er schätzt für jede Klasse (spam bzw. ham) die Wahrscheinlichkeit einzelner Wörter und entscheidet anhand der höchsten Wahrscheinlichkeit.
Wichtige Begriffe für die Klasse sind vor allem werbliche und betrügerische Wörter wie free, money, pills, viagra, investment oder HTML-/Link-Begriffe wie www und href.  
Für die Klasse ham sind typische Begriffe der regulären Kommunikation charakteristisch, z. B. meeting, thanks oder personen- und projektspezifische Wörter.

---

### Bewertung des Testergebnisses
Der Klassifikator erreicht eine Genauigkeit von etwa 97,7 % auf der Testmenge.  
Insbesondere der Recall für Spam ist hoch, sodass nur sehr wenige Spam-Mails als Ham klassifiziert werden (fehlerhaft, 2,3%).  
Insgesamt zeigt das Ergebnis, dass der Naive-Bayes-Klassifikator mit Bag-of-Words-Merkmalen gut für die Spam-Erkennung geeignet ist.
