from turtle import mode, tracer, color, write, goto, update, done

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
    #print(f"zdarzenie={zdarzenie_myszki}, x={x_myszki}, y={y_myszki}")
    pom, zdarzenie_myszki = zdarzenie_myszki, ""
    return pom, x_myszki, y_myszki


def ini_myszki():
    for guzik, numer in zip(["l_klik", "m_klik", "r_klik"], range(1, 4)):
        # print("ustawiam zdarzenie: " + guzik)
        onscreenclick(ustaw_guziki_myszy(guzik.lower()), numer)


# ------------- Obsługa myszki - koniec-------------

def ini_grafiki():
    mode("logo")
    tracer(0, 0)


def picasso():
    wena = True
    color("green")
    write("Klikaj lewym guzikiem żeby rysować, prawym żeby skończyć", align="center", font=("Arial", 20, "normal"))
    update()

    while wena:
        zdarzenie, x, y = daj_zdarzenie()

        if zdarzenie == "l_klik":
            goto(x, y)
            update()
        elif zdarzenie == "r_klik":
            print("No co Ty, już?")
            wena = False
        elif zdarzenie == "m_klik":
            print("Skąd Ty wziąłeś taki guzik?")
        else:
            print("Nieobsługiwane zdarzenie: " + zdarzenie)


def main():
    ini_grafiki()
    ini_myszki()
    picasso()
    done()


main()
