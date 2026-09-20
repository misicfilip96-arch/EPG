EPG ZA SPARKLE - 4 IZVORA
===========================

Ovaj paket spaja samo ova 4 izvora:

1. epg_ripper_RS1.xml.gz
2. epg_ripper_SPORTKLUB1.xml.gz
3. epg_ripper_BA1.xml.gz
4. epg_ripper_HR1.xml.gz

Nema nemackog EPG izvora.

KAKO SE POSTAVLJA
-----------------

1. Napravi PUBLIC GitHub repository.
2. Raspakuj ovaj ZIP i uploaduj:
   - merge_epg.py
   - .github folder
   - sources.txt
3. Otvori GitHub -> Actions.
4. Pokreni "Update merged XMLTV" -> Run workflow.
5. Posle zavrsetka bice napravljen branch "epg".

Jedini EPG URL za Sparkle je:

https://raw.githubusercontent.com/TVOJ_USERNAME/IME_REPO/epg/epg.xml.gz

Zameni TVOJ_USERNAME i IME_REPO svojim podacima.

Workflow automatski osvezava objedinjeni EPG na svakih 6 sati.
Branch "epg" se svaki put prepisuje, pa se Git istorija ne puni
desetinama megabajta EPG podataka.

M3U
---

Uz paket je dodat i fajl:

kanali_sparkle_4EPG.m3u

U njemu su tvg-id vrednosti prilagodjene tacnim ID-jevima iz ova
cetiri EPG izvora. Stari providerov url-tvg je uklonjen, da Sparkle
ne pokusava da koristi pogresan EPG.

Sport Klub SR i HR verzije istog broja namerno koriste isti EPG ID.
FOX/Fox Life/Fox Crime/Fox Movies tretirani su kao novi STAR brendovi.
