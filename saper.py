#Marta Markocka
#indeks nr 408932
#gra Saper

#-------Stałe - parametry trudności gry----------
liczba_pol_poz = 10 #liczba pól na planszy poziomo
liczba_pol_pion = 10 #liczba pól na planszy pionowo
liczba_min = 10 #liczba min na planszy

# ----- Stałe - inne ------------
marg_poz    = 20  # Szerokość marginesów w poziomie
marg_pion    = 20  # Wysokość marginesów w pionie
wiad_wys = 60  # Wysokość pola na wiadomość
ekran_wys = 0 #wysokość ekranu z planszą
ekran_szer = 0 #szerokość ekranu z planszą
plansza_szer = 0 #szerokość planszy - wyliczona w trakcie trwania programu
plansza_wys = 0 #wysokość planszy - wyliczona w trakcie trwania programu
pole_szer = 0 #szerokość pola - wyliczona w trakcie trwania programu
pole_wys = 0 #wysokość pola - wyliczona w trakcie trwania programu
liczba_nieozn = 0 #liczba min nieoznaczonych na planszy - wyliczona na początku trwania programu
czy_koniec_gry = 0 #0 znaczy ze gra trwa, 1 ze jest skonczona
wynik = 0 #pomocnicza zmienna - liczona na biezaco w trakcie trwania programu

from turtle import *
from math import sqrt, asin, pi
from random import randint

# ------------- Obsługa myszki - początek-------------
from turtle import onscreenclick
from time import sleep
import tkinter

zdarzenie_myszki = ""
x_myszki = 0
y_myszki = 0

def ustaw_guziki_myszy(guzik):
	def result(x, y):
		global zdarzenie_myszki, x_myszki, y_myszki
		zdarzenie_myszki, x_myszki, y_myszki = guzik, x, y

	return result

def daj_zdarzenie():
	global zdarzenie_myszki, x_myszki, y_myszki
	while zdarzenie_myszki == "":
		tkinter._default_root.update()
		sleep(0.01)
	pom, zdarzenie_myszki = zdarzenie_myszki, ""
	return pom, x_myszki, y_myszki

def ini_myszki():
	for guzik, numer in zip(["l_klik", "m_klik", "r_klik"], range(1, 4)):
		onscreenclick(ustaw_guziki_myszy(guzik.lower()), numer)

# ------------- Obsługa myszki - koniec-------------

def ini_grafiki():
	mode("logo")
	tracer(0, 0)
	setup(ekran_szer, ekran_wys)

def rysuj_prostokat(szer, wys):
	fd(szer)
	right(90)
	fd(wys)
	right(90)
	fd(szer)
	right(90)
	fd(wys)
	right(90)

def rysuj_pole_wiadomosci():
	color("CadetBlue3")
	fillcolor("CadetBlue3")
	begin_fill()
	rysuj_prostokat(plansza_szer, wiad_wys)
	end_fill()
	right(90)
	up()
	fd(wiad_wys+3)
	left(90)
	down()
	
def koloruj_plansze():
	color("CadetBlue2")
	fillcolor("CadetBlue2")
	begin_fill()
	rysuj_prostokat(plansza_szer, plansza_wys)
	end_fill()
	
def rysuj_pola():
	color("CadetBlue4")
	global pole_szer
	global pole_wys
	pole_szer = plansza_szer / liczba_pol_poz
	pole_wys = plansza_wys / liczba_pol_pion
	for i in range(liczba_pol_pion):
		for j in range(liczba_pol_poz):
			rysuj_prostokat(pole_szer, pole_wys)
			fd(pole_szer)
		right(90)
		fd(pole_wys)
		right(90)
		fd(plansza_szer)
		right(180)

def rysuj_zaznaczenie_miny(kolumna, wiersz):
	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2 - wiad_wys) #idzie do lewego, górnego rogu planszy
	right(90)
	fd(pole_szer*kolumna - pole_szer/2)
	right(90)
	fd(pole_wys*wiersz - pole_wys/3)
	left(90)
	down()
	#teraz jest na środku wybranego pola
	
	color("DarkOrchid4")
	fillcolor("DarkOrchid4")
	begin_fill()
	circle(pole_wys/6)
	end_fill()
	left(90)
	update()
	
def rysuj_mine(kolumna, wiersz):
	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2 - wiad_wys) #idzie do lewego, górnego rogu planszy
	right(90)
	fd(pole_szer*kolumna - pole_szer/2)
	right(90)
	fd(pole_wys*wiersz - pole_wys/5)
	left(90)
	down()
	#teraz jest na środku wybranego pola
	
	color("DarkOrchid2")
	fillcolor("DarkOrchid2")
	begin_fill()
	circle(pole_wys*3/10)
	end_fill()
	left(90)
	update()

def rysuj_przekreslenie(kolumna, wiersz):
	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2 - wiad_wys) #idzie do lewego, górnego rogu planszy
	right(90)
	fd(pole_szer*kolumna)
	right(90)
	fd(pole_wys*wiersz)
	left(180)
	down()
	#teraz jest w prawym, dolnym rogu wybranego pola
	
	color("DarkOrchid2")
	pensize(2)
	dlugosc_przekatnej = sqrt(pole_wys*pole_wys + pole_szer*pole_szer)
	kat = asin(pole_szer/dlugosc_przekatnej)
	kat = kat/pi *180
	left(kat)
	fd(dlugosc_przekatnej)
	up()
	right(90+kat)
	fd(pole_szer)
	right(90+kat)
	down()
	fd(dlugosc_przekatnej)
	right(180-kat)
	pensize(1)
	update()
	
def wypisz_cyfre_na_polu(cyfra, kolumna, wiersz):
	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2 - wiad_wys) #idzie do lewego, górnego rogu planszy
	right(90)
	fd(pole_szer*kolumna)
	right(90)
	fd(pole_wys*wiersz)
	left(90)
	#teraz jest w lewym, gornym rogu wybranego pola
	
	down()
	color("CadetBlue4")
	fillcolor("CadetBlue1")
	begin_fill()
	rysuj_prostokat(pole_szer, pole_wys)
	end_fill()
	up()

	fd(pole_szer/2)
	right(90)
	fd((pole_wys*3)/4)
	right(180)
	if (cyfra == "0"):
		cyfra = ""
	write(cyfra, align="center", font=("Arial", 20, "normal"))
	update()

def wypisz_status():
	color("CadetBlue4")
	up()
	goto(-(plansza_szer/2)+10, (plansza_wys+wiad_wys)/2+3 -wiad_wys*5/6)
	down()
	status = "Łącznie min: " + str(liczba_min) + "\nzostało nieoznaczonych: " + str(liczba_nieozn)
	write(status, align="left", font=("Arial", 15, "normal"))
	update()
	
def wypisz_koniec(czy_wygral):
	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2+3)
	right(90)
	down()
	rysuj_pole_wiadomosci()
	left(90)
	
	color("CadetBlue4")
	up()
	goto(-(plansza_szer/2)+30, (plansza_wys+wiad_wys)/2+3 -wiad_wys*2/3)
	down()
	status = czy_wygral + " Koniec gry."
	write(status, align="left", font=("Arial", 15, "normal"))
	update()
				
def rysuj_plansze():
	global plansza_szer, plansza_wys, liczba_nieozn
	plansza_szer = ekran_szer - 2*marg_poz
	plansza_wys = ekran_wys - 2*marg_pion - wiad_wys

	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2+3)
	down()
	right(90)
	
	rysuj_pole_wiadomosci()
	koloruj_plansze()
	rysuj_pola()
	left(90)
	liczba_nieozn = liczba_min
	wypisz_status()
	update()

def uaktualnij_status():
	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2+3)
	right(90)
	down()
	rysuj_pole_wiadomosci()
	left(90)
	wypisz_status()
	
def ktore_pole(x, y):
	global kolumna, wiersz
	if (x < -plansza_szer/2 or x > plansza_szer/2):
		print("Kliknąłeś poza planszą")
	elif (y < -(plansza_wys+wiad_wys)/2 or y > (plansza_wys+wiad_wys)/2 - wiad_wys):
		print("Kliknąłeś poza planszą")
	else:		
		x += plansza_szer/2
		y += (plansza_wys+wiad_wys)/2
		y -= plansza_wys
		y = -y
		
		x /= pole_szer
		y /= pole_wys
		
		kolumna = (int)(x)
		wiersz = (int)(y)

def zliczaj_pole_skrajne_nie_w_rogu(kolumna, wiersz, tab_min):
	#ta ifologia sprawdza z iloma minami sasiaduje pole
	#jesli jest na ktorejs krawedzi planszy, ale nie w jej rogu
	global wynik
	
	if (kolumna == 0): #lewa krawedz
		if (tab_min[wiersz-1][kolumna] == 1 or tab_min[wiersz-1][kolumna] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna+1] == 1 or tab_min[wiersz-1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz][kolumna+1] == 1 or tab_min[wiersz][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna+1] == 1 or tab_min[wiersz+1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna] == 1 or tab_min[wiersz+1][kolumna] == 3):
			wynik +=1
			
	elif (kolumna == liczba_pol_poz-1): #prawa krawedz
		if (tab_min[wiersz-1][kolumna] == 1 or tab_min[wiersz-1][kolumna] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna-1] == 1 or tab_min[wiersz-1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz][kolumna-1] == 1 or tab_min[wiersz][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna-1] == 1 or tab_min[wiersz+1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna] == 1 or tab_min[wiersz+1][kolumna] == 3):
			wynik +=1
			
	elif (wiersz == 0): #gorna krawedz
		if (tab_min[wiersz][kolumna-1] == 1 or tab_min[wiersz][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna-1] == 1 or tab_min[wiersz+1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna] == 1 or tab_min[wiersz+1][kolumna] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna+1] == 1 or tab_min[wiersz+1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz][kolumna+1] == 1 or tab_min[wiersz][kolumna+1] == 3):
			wynik +=1
			
	elif (wiersz == liczba_pol_pion-1): #dolna krawedz
		if (tab_min[wiersz][kolumna-1] == 1 or tab_min[wiersz][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna-1] == 1 or tab_min[wiersz-1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna] == 1 or tab_min[wiersz-1][kolumna] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna+1] == 1 or tab_min[wiersz-1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz][kolumna+1] == 1 or tab_min[wiersz][kolumna+1] == 3):
			wynik +=1
			
def zliczaj_pole_skrajne(kolumna, wiersz, tab_min):
	#ta ifologia sprawdza z iloma minami sasiaduje pole jesli jest w rogu
	global wynik
	
	if (kolumna == 0 and wiersz == 0): #lewy, gorny rog
		if (tab_min[wiersz][kolumna+1] == 1 or tab_min[wiersz][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna+1] == 1 or tab_min[wiersz+1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna] == 1 or tab_min[wiersz+1][kolumna] == 3):
			wynik +=1
			
	elif (kolumna == 0 and wiersz == liczba_pol_pion-1): #lewy, dolny rog
		if (tab_min[wiersz][kolumna+1] == 1 or tab_min[wiersz][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna+1] == 1 or tab_min[wiersz-1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna] == 1 or tab_min[wiersz-1][kolumna] == 3):
			wynik +=1
			
	elif (kolumna == liczba_pol_poz-1 and wiersz == 0): #prawy, gorny rog
		if (tab_min[wiersz][kolumna-1] == 1 or tab_min[wiersz][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna-1] == 1 or tab_min[wiersz+1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna] == 1 or tab_min[wiersz+1][kolumna] == 3):
			wynik +=1
			
	elif (kolumna == liczba_pol_poz-1 and wiersz == liczba_pol_pion-1): #prawy, dolny rog
		if (tab_min[wiersz][kolumna-1] == 1 or tab_min[wiersz][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna-1] == 1 or tab_min[wiersz-1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna] == 1 or tab_min[wiersz-1][kolumna] == 3):
			wynik +=1
			
	else:
		zliczaj_pole_skrajne_nie_w_rogu(kolumna, wiersz, tab_min)

def odkryj_pole_skrajne_nie_w_rogu(kolumna, wiersz, tab_min):
	#ta ifologia sprawdza czy mozna odkryc pola sasiadujace
	#dla pol, ktore sa na krawedzi, ale nie w rogu
	
	if (kolumna == 0):
		if (tab_min[wiersz-1][kolumna] != 1 and tab_min[wiersz-1][kolumna] != 3 and tab_min[wiersz-1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna+1] != 1 and tab_min[wiersz-1][kolumna+1] != 3 and tab_min[wiersz-1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz-1, tab_min)
		if (tab_min[wiersz][kolumna+1] != 1 and tab_min[wiersz][kolumna+1] != 3 and tab_min[wiersz][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz, tab_min)
		if (tab_min[wiersz+1][kolumna+1] != 1 and tab_min[wiersz+1][kolumna+1] != 3 and tab_min[wiersz+1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna] != 1 and tab_min[wiersz+1][kolumna] != 3 and tab_min[wiersz+1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz+1, tab_min)
			
	elif (kolumna == liczba_pol_poz-1):
		if (tab_min[wiersz-1][kolumna] != 1 and tab_min[wiersz-1][kolumna] != 3 and tab_min[wiersz-1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna-1] != 1 and tab_min[wiersz-1][kolumna-1] != 3 and tab_min[wiersz-1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz-1, tab_min)
		if (tab_min[wiersz][kolumna-1] != 1 and tab_min[wiersz][kolumna-1] != 3 and tab_min[wiersz][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz, tab_min)
		if (tab_min[wiersz+1][kolumna-1] != 1 and tab_min[wiersz+1][kolumna-1] != 3 and tab_min[wiersz+1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna] != 1 and tab_min[wiersz+1][kolumna] != 3 and tab_min[wiersz+1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz+1, tab_min)
			
	elif (wiersz == 0):
		if (tab_min[wiersz][kolumna-1] != 1 and tab_min[wiersz][kolumna-1] != 3 and tab_min[wiersz][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz, tab_min)
		if (tab_min[wiersz+1][kolumna-1] != 1 and tab_min[wiersz+1][kolumna-1] != 3 and tab_min[wiersz+1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna] != 1 and tab_min[wiersz+1][kolumna] != 3 and tab_min[wiersz+1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna+1] != 1 and tab_min[wiersz+1][kolumna+1] != 3 and tab_min[wiersz+1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz+1, tab_min)
		if (tab_min[wiersz][kolumna+1] != 1 and tab_min[wiersz][kolumna+1] != 3 and tab_min[wiersz][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz, tab_min)
			
	elif (wiersz == liczba_pol_pion-1):
		if (tab_min[wiersz][kolumna-1] != 1 and tab_min[wiersz][kolumna-1] != 3 and tab_min[wiersz][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz, tab_min)
		if (tab_min[wiersz-1][kolumna-1] != 1 and tab_min[wiersz-1][kolumna-1] != 3 and tab_min[wiersz-1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna] != 1 and tab_min[wiersz-1][kolumna] != 3 and tab_min[wiersz-1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna+1] != 1 and tab_min[wiersz-1][kolumna+1] != 3 and tab_min[wiersz-1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz-1, tab_min)
		if (tab_min[wiersz][kolumna+1] != 1 and tab_min[wiersz][kolumna+1] != 3 and tab_min[wiersz][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz, tab_min)
					
def odkryj_pole_skrajne(kolumna, wiersz, tab_min):
	#ta ifologia sprawdza czy mozna odkryc pola sasiadujace z polami, ktore sa w rogu
	
	if (kolumna == 0 and wiersz == 0):
		if (tab_min[wiersz][kolumna+1] != 1 and tab_min[wiersz][kolumna+1] != 3 and tab_min[wiersz][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz, tab_min)
		if (tab_min[wiersz+1][kolumna+1] != 1 and tab_min[wiersz+1][kolumna+1] != 3 and tab_min[wiersz+1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna] != 1 and tab_min[wiersz+1][kolumna] != 3 and tab_min[wiersz+1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz+1, tab_min)
			
	elif (kolumna == 0 and wiersz == liczba_pol_pion-1):
		if (tab_min[wiersz][kolumna+1] != 1 and tab_min[wiersz][kolumna+1] != 3 and tab_min[wiersz][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz, tab_min)
		if (tab_min[wiersz-1][kolumna+1] != 1 and tab_min[wiersz-1][kolumna+1] != 3 and tab_min[wiersz-1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna] != 1 and tab_min[wiersz-1][kolumna] != 3 and tab_min[wiersz-1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz-1, tab_min)
			
	elif (kolumna == liczba_pol_poz-1 and wiersz == 0):
		if (tab_min[wiersz][kolumna-1] != 1 and tab_min[wiersz][kolumna-1] != 3 and tab_min[wiersz][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz, tab_min)
		if (tab_min[wiersz+1][kolumna-1] != 1 and tab_min[wiersz+1][kolumna-1] != 3 and tab_min[wiersz+1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna] != 1 and tab_min[wiersz+1][kolumna] != 3 and tab_min[wiersz+1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz+1, tab_min)
			
	elif (kolumna == liczba_pol_poz-1 and wiersz == liczba_pol_pion-1):
		if (tab_min[wiersz][kolumna-1] != 1 and tab_min[wiersz][kolumna-1] != 3 and tab_min[wiersz][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz, tab_min)
		if (tab_min[wiersz-1][kolumna-1] != 1 and tab_min[wiersz-1][kolumna-1] != 3 and tab_min[wiersz-1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna] != 1 and tab_min[wiersz-1][kolumna] != 3 and tab_min[wiersz-1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz-1, tab_min)
			
	else:
		odkryj_pole_skrajne_nie_w_rogu(kolumna, wiersz, tab_min)
	
def odkryj_sasiednie_puste(kolumna, wiersz, tab_min):
	#ta ifologia sprawdza czy mozna odkryc pola sasiadujace z polem ktore nie jest przy krawedzi
	
	if (kolumna == 0 or wiersz == 0 or kolumna == liczba_pol_poz-1 or wiersz == liczba_pol_pion-1):
		odkryj_pole_skrajne(kolumna, wiersz, tab_min)
	
	else:
		if (tab_min[wiersz-1][kolumna-1] != 1 and tab_min[wiersz-1][kolumna-1] != 3 and tab_min[wiersz-1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna] != 1 and tab_min[wiersz-1][kolumna] != 3 and tab_min[wiersz-1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz-1, tab_min)
		if (tab_min[wiersz-1][kolumna+1] != 1 and tab_min[wiersz-1][kolumna+1] != 3 and tab_min[wiersz-1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz-1, tab_min)
		if (tab_min[wiersz][kolumna+1] != 1 and tab_min[wiersz][kolumna+1] != 3 and tab_min[wiersz][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz, tab_min)
		if (tab_min[wiersz+1][kolumna+1] != 1 and tab_min[wiersz+1][kolumna+1] != 3 and tab_min[wiersz+1][kolumna+1] != -1):
			zliczaj_sasiednie_miny(kolumna+1, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna] != 1 and tab_min[wiersz+1][kolumna] != 3 and tab_min[wiersz+1][kolumna] != -1):
			zliczaj_sasiednie_miny(kolumna, wiersz+1, tab_min)
		if (tab_min[wiersz+1][kolumna-1] != 1 and tab_min[wiersz+1][kolumna-1] != 3 and tab_min[wiersz+1][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz+1, tab_min)
		if (tab_min[wiersz][kolumna-1] != 1 and tab_min[wiersz][kolumna-1] != 3 and tab_min[wiersz][kolumna-1] != -1):
			zliczaj_sasiednie_miny(kolumna-1, wiersz, tab_min)
	
def zliczaj_sasiednie_miny(kolumna, wiersz, tab_min):
	#ta ifologia zlicza miny na polach sasiadujacych z polem ktore nie jest przy krawedzi
	global wynik
	wynik = 0
	
	if (kolumna == 0 or wiersz == 0 or kolumna == liczba_pol_poz-1 or wiersz == liczba_pol_pion-1):
		zliczaj_pole_skrajne(kolumna, wiersz, tab_min)
	
	else:
		if (tab_min[wiersz-1][kolumna-1] == 1 or tab_min[wiersz-1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna] == 1 or tab_min[wiersz-1][kolumna] == 3):
			wynik +=1
		if (tab_min[wiersz-1][kolumna+1] == 1 or tab_min[wiersz-1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz][kolumna+1] == 1 or tab_min[wiersz][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna+1] == 1 or tab_min[wiersz+1][kolumna+1] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna] == 1 or tab_min[wiersz+1][kolumna] == 3):
			wynik +=1
		if (tab_min[wiersz+1][kolumna-1] == 1 or tab_min[wiersz+1][kolumna-1] == 3):
			wynik +=1
		if (tab_min[wiersz][kolumna-1] == 1 or tab_min[wiersz][kolumna-1] == 3):
			wynik +=1
			
	wypisz_cyfre_na_polu(str(wynik), kolumna, wiersz)
	tab_min[wiersz][kolumna] = -1
	
	if (wynik == 0):
		odkryj_sasiednie_puste(kolumna, wiersz, tab_min)
			
def odkryj_pole(kolumna, wiersz, tab_min):
	liczba = tab_min[wiersz][kolumna]
	if (liczba == -1):
		print("Już tu klikałeś. Spróbuj kliknąć gdzie indziej.")
	elif (liczba == 2 or liczba == 3):
		print("Zaznaczyłeś, że tu spodziewasz się miny. Spróbuj kliknąć gdzie indziej.")
	elif (liczba == 1):
		global czy_koniec_gry
		czy_koniec_gry = 1
		wypisz_koniec("PRZEGRAŁEŚ.")
		odkryj_cala_plansze(tab_min)
	else:
		zliczaj_sasiednie_miny(kolumna, wiersz, tab_min)

def odkryj_cala_plansze(tab_min):
	#odkrywa na koncu gry cala plansze odpowiednio oznaczajac pola
	for i in range(liczba_pol_pion):
		for j in range(liczba_pol_poz):
			if (tab_min[i][j] == 1):
				rysuj_mine(j+1, i+1)
			elif (tab_min[i][j] == 2):
				rysuj_przekreslenie(j+1, i+1)
			elif (tab_min[i][j] == 3):
				rysuj_mine(j+1, i+1)
				rysuj_zaznaczenie_miny(j+1, i+1)
			elif (tab_min[i][j] == 0):
				zliczaj_sasiednie_miny(j, i, tab_min)
					
def sprawdz_czy_wygrana(tab_min):
	global czy_koniec_gry
	
	for i in range(liczba_pol_pion):
		for j in range(liczba_pol_poz):
			if (tab_min[i][j] == 2 or tab_min[i][j] == 1):
				czy_koniec_gry = 1
	
	if (czy_koniec_gry == 1):
		wypisz_koniec("PRZEGRAŁEŚ.")
	else:
		wypisz_koniec("WYGRAŁEŚ!")
	
	czy_koniec_gry = 1
	odkryj_cala_plansze(tab_min)

def usun_zaznaczenie(kolumna, wiersz):
	up()
	goto(-plansza_szer/2, (plansza_wys+wiad_wys)/2 - wiad_wys) #idzie do lewego, górnego rogu planszy
	right(90)
	fd(pole_szer*kolumna)
	right(90)
	fd(pole_wys*wiersz)
	left(90)
	#teraz jest w lewym, gornym rogu wybranego pola
	
	down()
	color("CadetBlue4")
	fillcolor("CadetBlue2")
	begin_fill()
	rysuj_prostokat(pole_szer, pole_wys)
	end_fill()
	up()
	left(90)
	update()
	
	uaktualnij_status()
	
def klikniecie(tab_min):
	global liczba_nieozn
	zdarzenie, x, y = daj_zdarzenie()
	ktore_pole(x,y)
	
	if zdarzenie == "l_klik":
		odkryj_pole(kolumna, wiersz, tab_min)
		
	elif zdarzenie == "r_klik":
		if (tab_min[wiersz][kolumna] == 2 or tab_min[wiersz][kolumna] == 3):
			tab_min[wiersz][kolumna] -=2
			liczba_nieozn +=1
			usun_zaznaczenie(kolumna, wiersz)
		elif (tab_min[wiersz][kolumna] == -1):
			print("Juz odkryłeś to pole. Spróbuj kliknąć gdzie indziej.")
		else:
			rysuj_zaznaczenie_miny(kolumna+1, wiersz+1)
			tab_min[wiersz][kolumna] += 2
			liczba_nieozn -=1
			uaktualnij_status()
			if (liczba_nieozn == 0):
				sprawdz_czy_wygrana(tab_min)			
		
	elif zdarzenie == "m_klik":
		print("Skąd Ty wziąłeś taki guzik?")
	else:
		print("Nieobsługiwane zdarzenie: " + zdarzenie)

def rozegraj(tab_min):
	
	while (czy_koniec_gry == 0):
		klikniecie(tab_min)

def losuj_mine(tab_min):
	
	wybrana = 0
	
	while (wybrana == 0):
		liczba = randint(0, liczba_pol_pion*liczba_pol_poz-1)
		kolumna = (liczba % liczba_pol_poz)
		wiersz = (int)((liczba - kolumna) / liczba_pol_poz)
		
		if tab_min[wiersz][kolumna] == 0:
			tab_min[wiersz][kolumna] = 1
			wybrana = 1

def losuj_miny(tab_min):
	
	for i in range(liczba_min):
		losuj_mine(tab_min)
			
def main():
	global ekran_wys, ekran_szer
	ekran_wys = liczba_pol_pion*50 + marg_pion*2 + wiad_wys
	ekran_szer = liczba_pol_poz*50 + marg_poz*2
	
	ini_grafiki()
	ini_myszki()
	rysuj_plansze()
	
	tab_min = [[0 for i in range(liczba_pol_poz)] for j in range(liczba_pol_pion)]
	losuj_miny(tab_min)
	
	rozegraj(tab_min)
	done()

main()
