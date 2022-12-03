from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref

import datetime
import os, platform

Base = declarative_base()

class Città(Base):
    __tablename__ = 'città'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String, nullable=False, unique=True)

    def view(self):
        return (self.Id, self.Nome)

class Proprietario(Base):
    __tablename__ = 'proprietario'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String, nullable=False)
    Cognome = Column(String, nullable=False)
    Email = Column(String, unique=True)
    Telefono = Column(String, nullable=False)
    IdCittà = Column(Integer, ForeignKey('città.Id', onupdate="CASCADE", ondelete="SET NULL"))

    def view(self):
        return (self.Id, self.Nome, self.Cognome, self.Email, self.Telefono, self.IdCittà)

class Marca(Base):
    __tablename__ = 'marca'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String, nullable=False)

    def view(self):
        return (self.Id, self.Nome)

class Modello(Base):
    __tablename__ = 'modello'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String, nullable=False)
    IdMarca = Column(Integer, ForeignKey('marca.Id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    marca = relationship('Marca', backref = backref('Modello', cascade='all, delete'))

    def view(self):
        return (self.Id, self.Nome, self.IdMarca)

class Meccanico(Base):
    __tablename__ = 'meccanico'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String, nullable=False)
    Cognome = Column(String, nullable=False)
    CF = Column(String, unique=True)

    def view(self):
        return (self.Id, self.Nome, self.Cognome, self.CF)

class Automobile(Base):
    __tablename__ = 'automobile'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Targa = Column(String, unique=True, nullable=False)
    IdProprietario = Column(Integer, ForeignKey('proprietario.Id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    IdModello = Column(Integer, ForeignKey('modello.Id', onupdate='CASCADE', ondelete='SET NULL'))
    proprietario = relationship('Proprietario', backref = backref('Automobile', cascade='all, delete'))

    def view(self):
        return (self.Id, self.Targa, self.IdProprietario, self.IdModello)

class Pezzo(Base):
    __tablename__ = 'pezzo'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String, nullable=False)

    def view(self):
        return (self.Id, self.Nome)

class Intervento(Base):
    __tablename__ = 'intervento'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Durata = Column(Integer)
    Descrizione = Column(String)
    IdMeccanico = Column(Integer, ForeignKey('meccanico.Id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    IdAutomobile = Column(Integer, ForeignKey('automobile.Id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    meccanico = relationship('Meccanico', backref = backref('Intervento', cascade='all,delete'))
    automobile = relationship('Automobile', backref = backref('Intervento', cascade='all, delete'))

    def view(self):
        return (self.Id, self.Durata, self.Descrizione, self.IdMeccanico, self.IdAutomobile)

class Recensione(Base):
    __tablename__ = 'recensione'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Commento = Column(String)
    Voto = Column(Integer, CheckConstraint('Voto>=0 and Voto<=5'))
    IdProprietario = Column(Integer, ForeignKey('proprietario.Id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    IdIntervento = Column(Integer, ForeignKey('intervento.Id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    proprietario = relationship('Proprietario', backref = backref('Recensione', cascade='all, delete'))
    intervento = relationship('Intervento', backref = backref('Recensione', cascade='all,delete'))

    def view(self):
        return (self.Id, self.Commento, self.Voto, self.IdProprietario, self.IdIntervento)

class Fornitore(Base):
    __tablename__ = 'fornitore'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String, nullable='False', unique=True)

    def view(self):
        return (self.Id, self.Nome)

class Spedizione(Base):
    __tablename__ = 'spedizione'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Prezzo = Column(Integer)
    DataSpedizione = Column(Date, nullable=False)
    QuantitàSpedita = Column(Integer)
    IdPezzo = Column(Integer, ForeignKey('pezzo.Id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    IdFornitore = Column(Integer, ForeignKey('fornitore.Id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    pezzo = relationship('Pezzo', backref = backref('Spedizione', cascade='all, delete'))
    fornitore = relationship('Fornitore', backref = backref('Spedizione', cascade='all, delete'))

    def view(self):
        return (self.Id, self.Prezzo, self.DataSpedizione, self.QuantitàSpedita, self.IdPezzo, self.IdFornitore)

class Usando(Base):
    __tablename__ = 'usando'
    IdIntervento = Column(Integer, ForeignKey('intervento.Id', onupdate='CASCADE', ondelete='CASCADE'), primary_key = True, nullable=False)
    IdPezzo = Column(Integer, ForeignKey('pezzo.Id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True, nullable=False)
    Quantità = Column(Integer)
    PrezzoUnitario = Column(Integer)
    intervento = relationship('Intervento', backref = backref('Usando', cascade = 'all, delete'))
    pezzo = relationship('Pezzo', backref = backref('Usando', cascade='all,delete'))

    def view(self):
        return (self.IdIntervento, self.IdPezzo, self.Quantità, self.PrezzoUnitario)

def elimina(tabella, i):
    try:
        x = session.query(tabella).get(i)
        session.delete(x)
        session.commit()
    except:
        input("Errore")
        session.rollback()

def inserimento(stringa):
    ris = -1
    try:
        ris = eval(input(stringa))
    except:
        input("Errore\n")
    return ris

def controllo(tabella, i):
    try:
        s = session.query(tabella).filter(tabella.Id==i).first()
        return s
    except:
        input("Errore!")
        session.rollback()

def visualizza(tabella):
    result = session.query(tabella).all()
    for i in result:
        print(i.view())
    input()

def pulisci():
    if platform.system()=='Linux' or platform.system()=='Darwin': os.system('clear')
    else: os.system('cls')

def menu2():
    pulisci()
    risp=input('\nCosa vuoi fare?\n0.Visualizzare dati inseriti\n1.Inserire nuovi dati\n2.Aggiornare dati già presenti\n3.Cancellare dati già presenti\n\
4.Visualizzare specifici dati\n5.Chiudi\n')

    while risp.isnumeric()==False:
        pulisci()
        risp=input('\nCosa vuoi fare?\n0.Visualizzare dati inseriti\n1.Inserire nuovi dati\n2.Aggiornare dati già presenti\n3.Cancellare dati già presenti\n\
4.Visualizzare specifici dati\n5.Chiudi\n')

    risp = eval(risp)
    return risp

def menu():
    pulisci()
    table = input("In quale tabella?\n\
1.Città\n\
2.Proprietario\n\
3.Automobile\n\
4.Fornitore\n\
5.Intervento\n\
6.Marca\n\
7.Meccanico\n\
8.Modello\n\
9.Pezzo\n\
10.Recensione\n\
11.Usando\n\
12.Spedizione\n\
")
    while table.isnumeric() == False:
        pulisci()
        table = input("In quale tabella?\n\
1.Città\n\
2.Proprietario\n\
3.Automobile\n\
4.Fornitore\n\
5.Intervento\n\
6.Marca\n\
7.Meccanico\n\
8.Modello\n\
9.Pezzo\n\
10.Recensione\n\
11.Usando\n\
12.Spedizione\n\
")
    table = eval(table)
    if table not in range(1,13):
        input("Valore non accettabile!")
        table = menu()

    return table

engine = create_engine("mysql+mysqlconnector://root:Fabio123@127.0.0.1/Officina")
meta = MetaData()

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

pulisci()

risp = menu2()
while risp!=5:

    if risp==0:
        table = menu()

        if table==1:
            print("(Id, Nome)")
            visualizza(Città)
        
        elif table==2:
            print("(Id, Nome, Cognome, Email, Telefono, IdCittà)")
            visualizza(Proprietario)

        elif table==3:
            print("(Id, Targa, IdProprietario, IdModello)")
            visualizza(Automobile)

        elif table==4:
            print("Id, Nome")
            visualizza(Fornitore)
        
        elif table==5:
            print("(Id, Durata, Descrizione, IdMeccanico, IdAutomobile)")
            visualizza(Intervento)

        elif table==6:
            print("(Id, Nome)")
            visualizza(Marca)
        
        elif table==7:
            print("(Id, Nome, Cognome, CF)")
            visualizza(Meccanico)

        elif table==8:
            print("(Id, Nome, IdMarca)")
            visualizza(Modello)

        elif table==9:
            print("(Id, Nome)")
            visualizza(Pezzo)

        elif table==10:
            print("(Id, Commento, Voto, IdProprietario, IdIntervento)")
            visualizza(Recensione)

        elif table==11:
            print("(IdIntervento, IdPezzo, Quantità, PrezzoUnitario)")
            visualizza(Usando)
        
        elif table==12:
            print("(Id, Prezzo, DataSpedizione, IdPezzo, IdFornitore)")
            visualizza(Spedizione)

        else: input("ERRORE")

    elif risp==1:
        table = menu()

        if table==1:
            a = input("Inserire nome città: ")
            if a!='':
                try:
                    c = Città(Nome=a)
                    session.add(c)
                    session.commit()
                except: 
                    session.rollback()
                    input("Valore già inserito!")
            else: 
                session.rollback()
                input("Valore non accettabile!")
            
        elif table==2:
            n, c = '', ''
            while n=='': n = input("Inserire nome: ")
            while c=='': c = input("Inserire cognome: ")
            e = input("Inserire email: ")
            if e=='': e = None
            t=''
            while t=='': t = input("Inserire telefono: ")
            citta = input("Inserire città: ")
            try:
                citt = session.query(Città).filter(Città.Nome==citta).first()
                if citt is None and citta!='':
                    input("ERRORE! Inserire città nel database!")
                else:
                    if citta=='': i=None
                    else: i=citt.Id
                    p = Proprietario(Nome=n, Cognome=c, Email=e, Telefono=t, IdCittà=i)
                    session.add(p)
                    session.commit()
            except:
                session.rollback()
            
        elif table==3:
            t = ''
            while t=='': t = input("Inserire targa: ")
            idp = inserimento("Inserire id proprietario: ")
            modello = input("Inserire modello: ")
            m = session.query(Modello).filter(Modello.Nome==modello).first()
            if not m and modello!='':
                input('ERRORE! Inserire modello %s nel database' % (modello))
            else:
                if modello=='': i=None 
                else: i = m.Id
                try:
                    a = Automobile(Targa=t, IdProprietario=idp, IdModello=i)
                    session.add(a)
                    session.commit()
                except:
                    input("Errore!")
                    session.rollback()

        elif table==4:
            n = ''
            while n=='': n = input('Inserire nome fornitore: ')
            f = session.query(Fornitore).filter(Fornitore.Nome==n).first()
            if not f:
                try:
                    f = Fornitore(Nome=n)
                    session.add(f)
                    session.commit()
                except:
                    session.rollback()
                    input("Errore!")
            else:
                input("Fornitore già inserito")

        elif table==5:
            d = input("Inserire durata: ")
            if d.isnumeric(): d = eval(d)
            else: d = None
            desc = input("Inserire descrizione: ")
            if desc=='': desc = None
            idm = inserimento("Inserire id meccanico: ")
            t = input("Inserire targa della macchina: ")
            s = session.query(Automobile).filter(Automobile.Targa==t).first()
            if not s:
                input("ERRORE! Inserire macchina nel database!")
            else:
                i = s.Id
                try:
                    i = Intervento(Durata=d, Descrizione=desc, IdMeccanico=idm, IdAutomobile=i)
                    session.add(i)
                    session.commit()
                except:
                    session.rollback
                    input("Errore!")

        elif table==6:
            n = ''
            while n=='': n = input("Inserire nome marca: ")
            s = session.query(Marca).filter(Marca.Nome==n).first()
            if not s:
                try:
                    m = Marca(Nome=n)
                    session.add(m)
                    session.commit()
                except:
                    session.rollback()
                    input("Errore!")
            else:
                verifica = input("Marca già inserita. Sicuro di volerne inserire un'altra (S o N)? ")
                if verifica=="S":
                    try:
                        m = Marca(Nome=n)
                        session.add(m)
                        session.commit()
                    except:
                        session.rollback()
                        input("Errore")
                else:
                    print("OK")

        elif table==7:
            n, c = '', ''
            while n=='': n = input("Inserire nome: ")
            while c=='': c = input("Inserire cognome: ")
            cfisc = input("Inserire codice fiscale: ")
            if cfisc=='': cfisc = None
            s = session.query(Meccanico).filter(Meccanico.CF==cfisc).first()
            if not s:
                try:
                    m = Meccanico(Nome=n, Cognome=c, CF=cfisc)
                    session.add(m)
                    session.commit()
                except:
                    session.rollback
                    input("Errore!")
            else:
                input("Meccanico già presente!")

        elif table==8:
            n = ''
            while n=='': n = input("Inserire nome modello: ")
            idm = inserimento("Inserire id marca: ")
            s = session.query(Modello).filter(Modello.Nome==n and Modello.IdMarca==idm).first()
            if not s:
                try:
                    m = Modello(Nome=n, IdMarca=idm)
                    session.add(m)
                    session.commit()
                except:
                    session.rollback()
                    input("Errore!")
            else:
                conf = input("Modello già inserito. Sicuro di voler procedere (S o N)? ")
                if conf=='S':
                    try:
                        m = Modello(Nome=n, IdMarca=idm)
                        session.add(m)
                        session.commit()
                    except:
                        session.rollback()
                        input("Errore")
                else:
                    input("Nessun inserimento fatto!")

        elif table==9:
            n = ''
            while n=='': n = input("Inserire nome pezzo: ")
            try:
                p = Pezzo(Nome=n)
                session.add(p)
                session.commit()
            except:
                session.rollback()
                input("Errore!")

        elif table==10:
            c = input("Inserire commento: ")
            if c=='': c = None
            v = input("Inserire voto da 0 a 5: ")
            if v.isnumeric(): v = eval(v)
            else: v=None
            i = inserimento("Inserire id proprietario: ")
            idi = eval(input("Inserire id intervento: "))
            try:
                r = Recensione(Commento=c, Voto=v, IdProprietario=i, IdIntervento=idi)
                session.add(r)
                session.commit()
            except:
                session.rollback()
                input("Errore! Voto tra 0 e 5? Id proprietario e IdIntervento sono corretti?")

        elif table==11:
            idi = inserimento("Inserire id intervento")
            idp = inserimento("Inserire id pezzo: ")
            q = input("Inserire quantità: ")
            if q.isnumeric(): q = eval(q)
            else: q = None
            p = input("Inserire prezzo unitario pezzo: ")
            if p.isnumeric(): p = eval(p)
            else: p = None
            try:
                u = Usando(IdIntervento=idi, IdPezzo=idp, Quantità=q, PrezzoUnitario=p)
                session.add(u)
                session.commit()
            except:
                session.rollback()
                input("Errore!")
            
        elif table==12:
            p = input("Inserire prezzo: ")
            if p.isnumeric(): p = eval(p)
            else: p = None
            data = input("Inserire data spedizione (yyyy-mm-dd): ")
            anno, mese, giorno = eval(data.split('-')[0]), eval(data.split('-')[1]), eval(data.split('-')[2])
            d = datetime.date(anno, mese, giorno)
            q = input("Inserire quantità spedita: ")
            if q.isnumeric(): q = eval(q)
            else: q = None
            idf = inserimento("Inserire id fornitore: ")
            idp = inserimento("Inserire id pezzo: ")
            try:
                s = Spedizione(Prezzo=p, DataSpedizione=d, QuantitàSpedita=q, IdFornitore=idf, IdPezzo=idp)
                session.add(s)
                session.commit()
            except:
                session.rollback()
                input("Errore!")

    elif risp==2:
        table = menu()
        print("Se non si desidera cambiare certi dati basta premere INVIO")

        if table==1:
            idc = inserimento("Inserire id città: ")
            if controllo(Città, idc):
                n = input("Inserire nuovo nome: ")
                if n=='': n = controllo(Città, idc).Nome
                try:
                    session.execute(update(Città).where(Città.Id==idc).values(Nome=n))
                    session.commit()
                except:
                    session.rollback()
                    input("Errore")
            else:
                input("Città non trovata")
        
        elif table==2:
            idp = inserimento("Inserire id proprietario: ")
            if controllo(Proprietario, idp):
                n = input("Inserire nuovo nome: ")
                if n=='': n = controllo(Proprietario, idp).Nome
                c = input("Inserire nuovo cognome: ")
                if c=='': c = controllo(Proprietario, idp).Cognome
                e = input("Inserire nuova email: ")
                if e=='': e = controllo(Proprietario, idp).Email
                t = input("Inserire nuovo telefono: ")
                if t=='': t = controllo(Proprietario, idp).Telefono
                citt = input("Inserire nuova città: ")
                try:
                    citta = session.query(Città).filter(Città.Nome==citt).first()
                    if not citta and citt!='':
                        input("ERRORE! Inserire città nel database!")
                    else:
                        if citt=='': i = controllo(Proprietario, idp).IdCittà
                        else: i=citta.Id
                        session.execute(update(Proprietario).where(Proprietario.Id==idp).values(Nome=n, Cognome=c, Email=e, Telefono=t, IdCittà=i))
                        session.commit()
                except: 
                    session.rollback()
                    input("Errore")
            else:
                input("Proprietario non trovato!")
        
        elif table==3:
            ida = inserimento("Inserire id automobile: ")
            if controllo(Automobile, ida):
                t = input("Inserire nuova targa: ")
                if t=='': t = controllo(Automobile, ida).Targa
                idp = input("Inserire nuovo id proprietario: ")
                if idp.isnumeric(): idp=eval(idp)
                else: idp = controllo(Automobile, ida).IdProprietario
                idm = input("Inserire id modello: ")
                if idm.isnumeric(): idm=eval(idm)
                else: idm = controllo(Automobile, ida).IdModello
                try:
                    session.execute(update(Automobile).where(Automobile.Id==ida).values(Targa=t, IdProprietario=idp, IdModello=idm))
                    session.commit()
                except:
                    input("Errore")
                    session.rollback()

        elif table==4:
            idf = inserimento("Inserire id fornitore: ")
            if controllo(Fornitore, idf):
                n = input("Inserire nuovo nome: ")
                try:
                    session.execute(update(Fornitore).where(Fornitore.Id==idf).values(Nome=n))
                    session.commit()
                except:
                    session.rollback()
                    input("Errore")
            else:
                input("Fornitore non trovato!")
        
        elif table==5:
            idi = inserimento("Inserire id intervento: ")
            if controllo(Intervento, idi):
                d = input("Inserire nuova durata: ")
                if d.isnumeric(): d = eval(d)
                else: d = controllo(Intervento, idi).Durata
                desc = input("Inserire nuova descrizione: ")
                if desc=='': desc = controllo(Intervento, idi).Descrizione
                idm = input("Inserire nuovo id meccanico: ")
                if idm.isnumeric(): idm = eval(idm)
                else: idm = controllo(Intervento, idi).IdMeccanico
                ida = input("Inserire nuovo id automobile: ")
                if ida.isnumeric(): ida = eval(ida)
                else: ida = controllo(Intervento, idi).IdAutomobile
                try:
                    session.execute(update(Intervento).where(Intervento.Id==idi).values(Durata=d, Descrizione=desc, IdMeccanico=idm, IdAutomobile=ida))
                    session.commit()
                except:
                    session.rollback()
                    input("Errore")

        elif table==6:
            idm = inserimento("Inserire id marca: ")
            if controllo(Marca, idm):
                n = input("Inserire nuovo nome: ")
                if n=='': n = controllo(Marca, idm).Nome
                try:
                    session.execute(update(Marca).where(Marca.Id==idm).values(Nome=n))
                    session.commit()
                except:
                    session.rollback()
                    input("Errore")

        elif table==7:
            idm = inserimento("Inserire id meccanico: ")
            if controllo(Meccanico, idm):
                n = input("Inserire nuovo nome: ")
                if n=='': n = controllo(Meccanico, idm).Nome
                c = input("Inserire nuovo cognome: ")
                if c=='': c = controllo(Meccanico, idm).Cognome
                cf = input("Inserire nuovo codice fiscale: ")
                if cf=='': cf = controllo(Meccanico, idm).CF
                try:
                    session.execute(update(Meccanico).where(Meccanico.Id==idm).values(Nome=n, Cognome=c, CF=cf))
                    session.commit()
                except:
                    session.rollback()
                    input("Errore")

        elif table==8:
            idm = inserimento("Inserire id modello: ")
            if controllo(Modello, idm):
                n = input("Inserire nuovo modello: ")
                if n=='': n = controllo(Modello, idm).Nome
                idmarca = input("Inserire nuovo id marca: ")
                if idmarca.isnumeric(): idmarca = eval(idmarca)
                else: idmarca = controllo(Modello, idm).IdMarca
                try:
                    session.execute(update(Modello).where(Modello.Id==idm).values(Nome=n, IdMarca=idmarca))
                    session.commit()
                except:
                    session.rollback()
                    input('Errore')
        
        elif table==9:
            idp = inserimento("Inserire id pezzo: ")
            if controllo(Pezzo, idp):
                n = input("Inserire nuovo nome: ")
                if n=='': n = controllo(Pezzo, idp).Nome
                try:
                    session.execute(update(Pezzo).where(Pezzo.Id==idp).values(Nome=n))
                    session.commit()
                except:
                    session.rollback()
                    input("Errore")
        
        elif table==10:
            idr = inserimento("Inserire id recensione: ")
            if controllo(Recensione, idr):
                c = input("Inserire nuovo commento: ")
                if c=='': c = controllo(Recensione, idr).Commento
                v = input("Inserire nuovo voto (tra 0 e 5 compresi): ")
                if v.isnumeric(): v = eval(v)
                elif v=='': v = controllo(Recensione, idr).Voto
                else: 
                    print("Errore")
                    break;
                idp = input("Inserire nuovo id proprietario: ")
                if idp.isnumeric(): idp = eval(idp)
                else: idp = controllo(Recensione, idr).IdProprietario
                idi = input("Inserire nuovo id intervento: ")
                if idi.isnumeric(): idi = eval(idi)
                else: idi = controllo(Recensione, idr).IdIntervento
                try:
                    session.execute(update(Recensione).where(Recensione.Id==idr).values(Commento=c, Voto=v, IdProprietario=idp, IdIntervento=idi))
                    session.commit()
                except:
                    session.rollback()
                    input("Errore")

        elif table==11:
            idp = inserimento("Inserire id pezzo: ")
            idi = inserimento("Inserire id intervento: ")
            try:
                s = session.query(Usando).filter(Usando.IdPezzo==idp and Usando.IdIntervento==idi).first()
                if s:
                    q = input("Inserire nuova quantità: ")
                    if q.isnumeric(): q = eval(q)
                    else: q = s.Quantità
                    p = input("Inserire nuovo prezzo unitario: ")
                    if p.isnumeric(): p = eval(p)
                    else: p = s.PrezzoUnitario
                    session.execute(update(Usando).where(Usando.IdPezzo==idp and Usando.IdIntervento==idi).values(Quantità=q, PrezzoUnitario=p))
                    session.commit()
            except: 
                session.rollback()
                input("Errore")
            
        elif table==12:
            ids = inserimento("Inserire id spedizione: ")
            if controllo(Spedizione, ids):
                p = input("Inserire nuovo prezzo: ")
                if p.isnumeric(): p = eval(p)
                else: p = controllo(Spedizione, ids).Prezzo
                data = input("Inserire nuova data spedizione (yyyy-mm-dd): ")
                anno, mese, giorno = eval(data.split('-')[0]), eval(data.split('-')[1]), eval(data.split('-')[2])
                d = datetime.date(anno, mese, giorno)
                q = input("Inserire nuova quantità spedita: ")
                if q.isnumeric(): q = eval(q)
                else: q = controllo(Spedizione, ids).QuantitàSpedita
                idp = input("Inserire nuovo id pezzo: ")
                if idp.isnumeric(): idp = eval(idp)
                else: idp = controllo(Spedizione, ids).IdPezzo
                idf = input("Inserire nuovo id fornitore: ")
                if idf.isnumeric(): idf = eval(idf)
                else: idf = controllo(Spedizione, ids).IdFornitore
                try:
                    session.execute(update(Spedizione).where(Spedizione.Id==ids).values(Prezzo=p, DataSpedizione=d, QuantitàSpedita=q, IdPezzo=idp, IdFornitore=idf))
                    session.commit()
                except: 
                    session.rollback()
                    input("Errore")

    elif risp==3:
        table = menu()

        if table==1:
            n = input("Inserire nome della città da eliminare: ")
            try:
                c = session.query(Città).filter(Città.Nome==n).first()
                elimina(Città, c.Id)
            except: 
                session.rollback()
                input("Errore!")
        
        elif table==2:
            idp=eval(input("Inserire id del proprietario da eliminare: "))
            elimina(Proprietario, idp)
        
        elif table==3:
            t = input("Inserire targa dell'automobile da eliminare: ")
            try:
                a = session.query(Automobile).filter(Automobile.Targa==t).first()
                if a: elimina(Automobile, a.Id)
                else: input("Automobile non trovata")
            except:
                input("Errore")
                session.rollback()
        
        elif table==4:
            n = input("Inserire nome fornitore: ")
            try:
                f = session.query(Fornitore).filter(Fornitore.Nome==n).first()
                if f: elimina(Fornitore, f.Id)
                else: input("Fornitore non trovato!")
            except: 
                session.rollback()
                input("Errore!")
        
        elif table==5:
            idi = inserimento("Inserire id intervento: ")
            elimina(Intervento, idi)
        
        elif table==6:
            idm = inserimento("Inserire id marca: ")
            elimina(Marca, idm)

        elif table==7:
            idm = inserimento("Inserire id meccanico: ")
            elimina(Meccanico, idm)

        elif table==8:
            idm = inserimento("Inserire id modello: ")
            elimina(Modello, idm)
        
        elif table==9:
            idp = inserimento("Inserire id pezzo: ")
            elimina(Pezzo, idp)
        
        elif table==10:
            idr = inserimento("Inserire id recensione: ")
            elimina(Recensione, idr)

        elif table==11:
            idi = inserimento("Inserire id intervento: ")
            idp = inserimento("Inserire id pezzo: ")
            try:
                x = session.query(Usando).filter(Usando.IdIntervento==idi and Usando.IdPezzo==idp).first()
                session.delete(x)
                session.commit()
            except:
                session.rollback()
                input('Errore')
        
        elif table==12:
            ids = inserimento("Inserire id spedizione: ")
            elimina(Spedizione, ids)

    elif risp==4:
        v = eval(input("1. Il nome e il cognome dei proprietari delle automobili con la targa che inizia per E\n\
2. Le targhe delle automobili i cui proprietari vivono a Roma\n\
3. Il nome dei meccanici accompagnato dal numero di interventi fatti in ordine decrescente\n"))

        if v==1:
            p = session.query(Proprietario.Nome, Proprietario.Cognome).where(and_(Proprietario.Id==Automobile.IdProprietario, Automobile.Targa.like('E%'))).all()
            for i in p:
                print(i)
            input()
        
        if v==2:
            a = session.query(Automobile.Targa).where(and_(Proprietario.Id==Automobile.IdProprietario, Proprietario.IdCittà==Città.Id, Città.Nome=='Roma')).all()
            for i in a:
                print(i)
            input()

        if v==3:
            m = session.query(Meccanico.Nome, func.count()).where(Meccanico.Id==Intervento.IdMeccanico).group_by(Meccanico.Id).order_by(desc(func.count())).all()
            for i in m:
                print(i)
            input()
    
    risp=menu2()

