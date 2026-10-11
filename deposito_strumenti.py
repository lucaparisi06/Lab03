from operator import attrgetter
class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.id_prestito}: strumento {self.id_strumento}, allievo {self.cognome_allievo}, data {self.data}"
class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return f"{self.codice} - {self.tipo}, marca {self.marca}, anno {self.anno_acquisto}, valore {self.valore:.2f} euro"
class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti={}
        self.prestiti = {}
        self.contatore_prestiti = 1


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for r in file:
                    riga = r.rstrip('\n').split(',')
                    codice = riga[0]
                    tipo = riga[1]
                    marca = riga[2]
                    anno_acquisto = int(riga[3])
                    valore = float(riga[4])
                    strumento = Strumento(codice, tipo, marca, anno_acquisto, valore)
                    self.strumenti[codice] = strumento
        except FileNotFoundError:
            raise


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        lista_codici = []

        if len(self.strumenti) == 0:
                codice_nuovo = 'S1'
        else:
            for codice in self.strumenti:
                lista_codici.append(int(codice[1:]))

            codice_massimo = max(lista_codici)
            codice_nuovo = 'S' + str(codice_massimo + 1)
        strumento = Strumento(codice_nuovo, tipo, marca, anno_acquisto, valore)

        self.strumenti[codice_nuovo] = strumento
        return strumento


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista_strumenti = []
        for codice in self.strumenti:
            lista_strumenti.append(self.strumenti[codice])
        lista_strumenti.sort(key=attrgetter('marca'))
        return lista_strumenti
    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise ValueError("Lo strumento non esiste.")

        for codice in self.prestiti:
            if self.prestiti[codice].id_strumento == id_strumento:
                raise ValueError("Lo strumento è già in prestito.")

        codice_prestito = 'P' + str(self.contatore_prestiti)

        prestito = Prestito(
            codice_prestito, data, id_strumento, cognome_allievo
        )

        self.prestiti[codice_prestito] = prestito
        self.contatore_prestiti += 1

        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise ValueError("Il prestito non esiste.")

        del self.prestiti[id_prestito]
