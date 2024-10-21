import copy

färg_katalog= {0: "□", 1: "■",}
sträng_till_kolumn = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
sträng_till_kolumn_reverse = {v: k for k, v in sträng_till_kolumn.items()}
sträng_till_rad = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0, ' ':8}
sträng_till_rad_reverse = {v: k for k, v in sträng_till_rad.items()}
bonde_kan_flytta_två_steg_hit = ()
bonde_har_flyttat_två_steg_hit = ()
en_passant = ()
en_passant_remove = ()
rokad_positiv = ()
rokad_negativ = ()
position_vit_kung = (7, 4)
position_svart_kung = (0, 4)

class piece:
    def __init__(self, namn, karaktär, color, x, y):
        self.namn = namn
        self.karaktär = karaktär
        self.color = color
        self.x = x
        self.y = y
        self.beteende_lista = []
        self.moves = 0
    
    def lägg_till_flytt_beteende(self, flytt_graf, krav=None):
        nytt_flytt_beteende = FlyttBeteende(self, flytt_graf, krav)
        self.beteende_lista.append(nytt_flytt_beteende)
    
    def ge_lista_på_alla_möjliga_flyttar(self):
        alla_möjliga_flyttar = []
        for beteende in self.beteende_lista:
            for e in beteende.ge_lista_på_möjliga_flyttar(self.x, self.y):
                alla_möjliga_flyttar.append(e)
        return alla_möjliga_flyttar


class SchackPosition:
    def __init__(self, färg=0, pjäs=None):
        self.färg = färg
        self.pjäs = pjäs
    
    def placeraPjäs(self, pjäs):
        self.pjäs = pjäs
    
    def ta_bort_pjäs(self):
        self.pjäs = None
    
    def hämta_utseende_sträng(self):
        if self.pjäs == None:
            return färg_katalog[self.färg]
        return self.pjäs.karaktär

class FlyttGraf:
    def __init__(self, x, y, steg):
        self.x = x
        self.y = y
        self.steg = steg
    
    def __str__(self):
        return f"Flytt(dragx={self.x}, dragy={self.y})"

class FlyttBeteende:
    def __init__(self, pjäsFörälder, flytt_graf, krav_funktion=None):
        self.pjäsFörälder = pjäsFörälder
        self.flytt_graf = flytt_graf
        self.krav_funktion = krav_funktion
    
    def __str__(self):
        return f"Person(namn={self.flytt_graf})"
    
    def ge_lista_på_möjliga_flyttar(self, x, y):
        global bonde_kan_flytta_två_steg_hit
        global bonde_har_flyttat_två_steg_hit
        global en_passant
        global en_passant_remove
        global rokad_positiv
        global rokad_negativ
        lista_med_flyttar = []
        if self.krav_funktion == None:
            steg = 0
            x1 = x + (self.flytt_graf.x)
            y1 = y + (self.flytt_graf.y)
            kolliderat_med_samma_färg = kolliderar_med_pjäs_av_samma_färg(x1, y1, self.pjäsFörälder.color)
            tagit_pjäs = False
            while är_drag_på_schackbrädet(x1, y1) and kolliderat_med_samma_färg == False and steg < self.flytt_graf.steg and tagit_pjäs == False:
                lista_med_flyttar.append((x1, y1))
                if tagit_pjäs_funktion(x1, y1, self.pjäsFörälder.color):
                    break
                x1 += (self.flytt_graf.x)
                y1 += (self.flytt_graf.y)
                kolliderat_med_samma_färg = kolliderar_med_pjäs_av_samma_färg(x1, y1, self.pjäsFörälder.color)
                steg += 1
        elif self.krav_funktion == "Bonde_ett_steg":
            if schackbrädet[x+self.flytt_graf.x][y].pjäs == None:
                lista_med_flyttar.append((x+self.flytt_graf.x, y))
        elif self.krav_funktion == "Bonde_två_steg":
            if schackbrädet[x+int(((self.flytt_graf.x)/2))][y].pjäs == None and schackbrädet[x+self.flytt_graf.x][y].pjäs == None and self.pjäsFörälder.moves == 0:
                lista_med_flyttar.append((x+self.flytt_graf.x, y))
                bonde_kan_flytta_två_steg_hit = (x+self.flytt_graf.x, y)
        elif self.krav_funktion == "Bonde_ta_pjäs":
            if är_drag_på_schackbrädet(x+self.flytt_graf.x, y+self.flytt_graf.y) and schackbrädet[x+self.flytt_graf.x][y+self.flytt_graf.y].pjäs != None and schackbrädet[x+self.flytt_graf.x][y+self.flytt_graf.y].pjäs.color != self.pjäsFörälder.color:
                lista_med_flyttar.append((x+self.flytt_graf.x, y+self.flytt_graf.y))
        elif self.krav_funktion == "En_passant":
            if bonde_har_flyttat_två_steg_hit == (x, y+self.flytt_graf.y):
                lista_med_flyttar.append((x+self.flytt_graf.x, y+self.flytt_graf.y))
                en_passant = (x+self.flytt_graf.x, y+self.flytt_graf.y)
                en_passant_remove = (x, y+self.flytt_graf.y)
        elif self.krav_funktion == "rokad_positiv":
            if self.pjäsFörälder.moves == 0 and schackbrädet[x][y+3].pjäs.moves == 0 and schackbrädet[x][y+2].pjäs == None and schackbrädet[x][y+1].pjäs == None:
                lista_med_flyttar.append((x+self.flytt_graf.x, y+self.flytt_graf.y))
                rokad_positiv = (x+self.flytt_graf.x, y+self.flytt_graf.y)
        elif self.krav_funktion == "rokad_negativ":
            if self.pjäsFörälder.moves == 0 and schackbrädet[x][y-4].pjäs.moves == 0 and schackbrädet[x][y-3].pjäs == None and schackbrädet[x][y-2].pjäs == None and schackbrädet[x][y-1].pjäs == None:
                lista_med_flyttar.append((x+self.flytt_graf.x, y+self.flytt_graf.y))
                rokad_negativ = (x+self.flytt_graf.x, y+self.flytt_graf.y)
        return lista_med_flyttar


def är_drag_på_schackbrädet(x, y):
    if x < 0:
        return False
    elif x > 7:
        return False
    elif y < 0:
        return False
    elif y > 7:
        return False
    else:
        return True

def kolliderar_med_pjäs_av_samma_färg(x, y, färg):
    if är_drag_på_schackbrädet(x, y):
        if schackbrädet[x][y].pjäs == None:
            return False
        elif schackbrädet[x][y].pjäs.color == färg:
            return True
        else:
            return False
    else:
        return False

def tagit_pjäs_funktion(x, y, färg):
    if schackbrädet[x][y].pjäs == None:
        return False
    elif schackbrädet[x][y].pjäs.color != färg:
        return True
    else:
        return False

def skapa_standard_schackbräde_matris():
    schackbräde_matris=[[0 for ix in range(8)] for iy in range(8)]
    for ix in range(8):
        for iy in range(8):
            schackbräde_matris[ix][iy]=SchackPosition((ix+iy)%2)
    placera_standard_pjäser_i_shack_position_matris(schackbräde_matris)
    return schackbräde_matris

def skapa_bonde(karaktär, färg, x, y):
    bonde = piece("Bonde", karaktär, färg, x, y)
    if färg == "vit":
        bonde.lägg_till_flytt_beteende(FlyttGraf(-1, 0, 1), "Bonde_ett_steg")
        bonde.lägg_till_flytt_beteende(FlyttGraf(-2, 0, 1), "Bonde_två_steg")
        bonde.lägg_till_flytt_beteende(FlyttGraf(-1, 1, 1), "Bonde_ta_pjäs")
        bonde.lägg_till_flytt_beteende(FlyttGraf(-1, -1, 1), "Bonde_ta_pjäs")
        bonde.lägg_till_flytt_beteende(FlyttGraf(-1, 1, 1), "En_passant")
        bonde.lägg_till_flytt_beteende(FlyttGraf(-1, -1, 1), "En_passant")
    else:
        bonde.lägg_till_flytt_beteende(FlyttGraf(1, 0, 1), "Bonde_ett_steg")
        bonde.lägg_till_flytt_beteende(FlyttGraf(2, 0, 1), "Bonde_två_steg")
        bonde.lägg_till_flytt_beteende(FlyttGraf(1, 1, 1), "Bonde_ta_pjäs")
        bonde.lägg_till_flytt_beteende(FlyttGraf(1, -1, 1), "Bonde_ta_pjäs")
        bonde.lägg_till_flytt_beteende(FlyttGraf(1, 1, 1), "En_passant")
        bonde.lägg_till_flytt_beteende(FlyttGraf(1, -1, 1), "En_passant")
    return bonde

def skapa_torn(karaktär, färg, x, y):
    torn = piece("Torn", karaktär, färg, x, y)
    torn.lägg_till_flytt_beteende(FlyttGraf(0, 1, 7))
    torn.lägg_till_flytt_beteende(FlyttGraf(0, -1, 7))
    torn.lägg_till_flytt_beteende(FlyttGraf(1, 0, 7))
    torn.lägg_till_flytt_beteende(FlyttGraf(-1, 0, 7))
    return torn

def skapa_häst(karaktär, färg, x, y):
    häst = piece("Häst", karaktär, färg, x, y)
    häst.lägg_till_flytt_beteende(FlyttGraf(1, 2, 1))
    häst.lägg_till_flytt_beteende(FlyttGraf(1, -2, 1))
    häst.lägg_till_flytt_beteende(FlyttGraf(-1, 2, 1))
    häst.lägg_till_flytt_beteende(FlyttGraf(-1, -2, 1))
    häst.lägg_till_flytt_beteende(FlyttGraf(2, 1, 1))
    häst.lägg_till_flytt_beteende(FlyttGraf(2, -1, 1))
    häst.lägg_till_flytt_beteende(FlyttGraf(-2, 1, 1))
    häst.lägg_till_flytt_beteende(FlyttGraf(-2, -1, 1))
    return häst

def skapa_löpare(karaktär, färg, x, y):
    löpare = piece("Löpare", karaktär, färg, x, y)
    löpare.lägg_till_flytt_beteende(FlyttGraf(1, 1, 7))
    löpare.lägg_till_flytt_beteende(FlyttGraf(1, -1, 7))
    löpare.lägg_till_flytt_beteende(FlyttGraf(-1, 1, 7))
    löpare.lägg_till_flytt_beteende(FlyttGraf(-1, -1, 7))
    return löpare

def skapa_drottning(karaktär, färg, x, y):
    drottning = piece("Drottning", karaktär, färg, x, y)
    drottning.lägg_till_flytt_beteende(FlyttGraf(0, 1, 7))
    drottning.lägg_till_flytt_beteende(FlyttGraf(0, -1, 7))
    drottning.lägg_till_flytt_beteende(FlyttGraf(1, 0, 7))
    drottning.lägg_till_flytt_beteende(FlyttGraf(-1, 0, 7))
    drottning.lägg_till_flytt_beteende(FlyttGraf(1, 1, 7))
    drottning.lägg_till_flytt_beteende(FlyttGraf(1, -1, 7))
    drottning.lägg_till_flytt_beteende(FlyttGraf(-1, 1, 7))
    drottning.lägg_till_flytt_beteende(FlyttGraf(-1, -1, 7))
    return drottning

def skapa_kung(karaktär, färg, x, y):
    kung = piece("Kung", karaktär, färg, x, y)
    kung.lägg_till_flytt_beteende(FlyttGraf(0, 1, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(0, -1, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(1, 0, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(-1, 0, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(1, 1, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(1, -1, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(-1, 1, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(-1, -1, 1))
    kung.lägg_till_flytt_beteende(FlyttGraf(0, 2, 1), "rokad_positiv")
    kung.lägg_till_flytt_beteende(FlyttGraf(0, -2, 1), "rokad_negativ")
    return kung

def placera_standard_pjäser_i_shack_position_matris(matris):
    for i in range(8):
        matris[1][i].pjäs = skapa_bonde("♙", "svart", 1, i)
    for i in range(8):
        matris[6][i].pjäs = skapa_bonde("♟", "vit", 6, i)
    matris[0][0].pjäs = skapa_torn("♖", "svart", 0, 0)
    matris[0][7].pjäs = skapa_torn("♖", "svart", 0 ,7)
    matris[0][1].pjäs = skapa_häst("♘", "svart", 0, 1)
    matris[0][6].pjäs = skapa_häst("♘", "svart", 0, 6)
    matris[0][2].pjäs = skapa_löpare("♗", "svart", 0, 2)
    matris[0][5].pjäs = skapa_löpare("♗", "svart", 0, 5)
    matris[0][4].pjäs = skapa_kung("♔", "svart", 0, 4)
    matris[0][3].pjäs = skapa_drottning("♕", "svart", 0, 3)
    
    matris[7][0].pjäs = skapa_torn("♜", "vit", 7, 0)
    matris[7][7].pjäs = skapa_torn("♜", "vit", 7, 7)
    matris[7][1].pjäs = skapa_häst("♞", "vit", 7, 1)
    matris[7][6].pjäs = skapa_häst("♞", "vit", 7, 6)
    matris[7][2].pjäs = skapa_löpare("♝", "vit", 7, 2)
    matris[7][5].pjäs = skapa_löpare("♝", "vit", 7, 5)
    matris[7][4].pjäs = skapa_kung("♚", "vit", 7, 4)
    matris[7][3].pjäs = skapa_drottning("♛", "vit", 7, 3)
    return matris

def rita_schack_bräde(matris):
    bräde_sträng=""
    for ix in range(8):
        for iy in range(8):
            schack_position=matris[ix][iy]
            bräde_sträng+=schack_position.hämta_utseende_sträng()
            bräde_sträng += " "
        bräde_sträng+="\n"            
    print(bräde_sträng)

def flytta_pjäs(matris, fx, fy, tx, ty):
    pjäs_i_handen = matris[fx][fy].pjäs
    pjäs_i_handen.moves += 1
    pjäs_i_handen.x = tx
    pjäs_i_handen.y = ty
    matris[fx][fy].pjäs = None
    matris[tx][ty].pjäs = pjäs_i_handen
    return matris

def konvertera_till_notation(tup):
    rad = sträng_till_rad_reverse[tup[0]]
    kolumn = sträng_till_kolumn_reverse[tup[1]]
    return kolumn + str(rad)

def är_det_schack(matris, färg):
    drag = []
    for i in range(8):
        for e in matris[i]:
            if e.pjäs != None:
                if e.pjäs.color != färg:
                    drag = e.pjäs.ge_lista_på_alla_möjliga_flyttar()
                    for j in drag:
                        if matris[j[0]][j[1]].pjäs != None and matris[j[0]][j[1]].pjäs.namn == "Kung":
                            return True
    return False


schackbrädet = skapa_standard_schackbräde_matris()
rita_schack_bräde(schackbrädet)

match_pågår = True
vems_tur = "vit"
while match_pågår:
    print("Vilken pjäs vill du flytta?")
    user_input = input()
    x1 = sträng_till_rad[user_input[1]]
    y1 = sträng_till_kolumn[user_input[0]]
    if är_drag_på_schackbrädet(x1, y1) == True:
        if schackbrädet[x1][y1].pjäs == None:
            print("Ingen pjäs på denna ruta")
        else:
            if schackbrädet[x1][y1].pjäs.color == vems_tur:
                if len(schackbrädet[x1][y1].pjäs.ge_lista_på_alla_möjliga_flyttar()) == 0:
                    print("Inga möjliga drag för denna pjäs")
                else:
                    print("Följande är möjliga drag")
                    drag = schackbrädet[x1][y1].pjäs.ge_lista_på_alla_möjliga_flyttar()
                    for e in drag:
                        print(konvertera_till_notation(e))
                    print("Var vill du flytta pjäsen?")
                    flytta_till_ruta = input()
                    x2 = sträng_till_rad[flytta_till_ruta[1]]
                    y2 = sträng_till_kolumn[flytta_till_ruta[0]]
                    schackbrädet_testa_schack = copy.deepcopy(schackbrädet)
                    flytta_pjäs(schackbrädet_testa_schack, x1, y1, x2, y2)
                    if är_det_schack(schackbrädet_testa_schack, "vit"):
                        print("ogiltigt drag, det är schack")
                    else:
                        if (x2, y2) in drag:
                            if (x2, y2) == bonde_kan_flytta_två_steg_hit:
                                bonde_har_flyttat_två_steg_hit = (x2, y2)
                            else:
                                bonde_har_flyttat_två_steg_hit = ()
                            if (x2, y2) == en_passant:
                                schackbrädet[en_passant_remove[0]][en_passant_remove[1]].pjäs = None
                            else:
                                en_passant = ()
                            if (x2, y2) == rokad_positiv:
                                flytta_pjäs(schackbrädet, x2, y2+1, x2, y2-1)
                            if (x2, y2) == rokad_negativ:
                                flytta_pjäs(schackbrädet, x2, y2-2, x2, y2+1)
                            flytta_pjäs(schackbrädet, x1, y1, x2, y2)
                            if vems_tur == "vit":
                                vems_tur = "svart"
                            else:
                                vems_tur = "vit"
                        else:
                            print("Inte ett giltigt drag")
            else:
                print("Du får inte flytta motståndarens pjäser")
    else:
        print("ruta är inte på schackbrädet")
    rita_schack_bräde(schackbrädet)