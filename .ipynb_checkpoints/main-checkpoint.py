import netCDF4 as nc
import sqlite3
import numpy as np
from copy import deepcopy
import os
import folium
from folium.plugins import HeatMap
import pandas as pd
import io
from PIL import Image
from matplotlib import pyplot as plt




from scipy import stats





class ClimaTempo:
    def __init__(self, pathDB, precisionCoord, ff, fo):
        self.nameFileObservation=fo
        self.nameFileForecast=ff
        self.precisionCoord=precisionCoord
        self.pathDB = pathDB
        self.con = None
        self.point = None
        self.centerMap=[-22.309144, -48.405080]
        
    def Conectar(self):
        self.con = sqlite3.connect(self.pathDB)
        self.point = self.con.cursor()
    
    def EncerrarCon(self):
        self.point.close()
        self.con.close()
        
    def ConvKtoC(self, value):
        return (value-273.15)
    
    def ETL(self):
        self.Conectar()
        self.point.execute('''
            create table if not exists dataObservation(
            id integer primary key autoincrement,
            time float,
            lat float,
            lon float,
            temperatura float)
            ''')
        self.point.execute('''
            create table if not exists dataForecast(
            id integer primary key autoincrement,
            time float,
            lat float,
            lon float,
            temperatura float)
            ''')
        self.point.execute('''
            create table if not exists CoordObservation(
            id integer primary key autoincrement,
            lat float,
            lon float)
            ''')
        self.point.execute('''
            create table if not exists CoordForecast(
            id integer primary key autoincrement,
            lat float,
            lon float)
            ''')
        print("Tabelas verificadas")
        print("Extração de dados observados")
        self.Observation = nc.Dataset(self.nameFileObservation)
        for lat in range(len(self.Observation['lat'][:])):
            for lon in range(len(self.Observation['lon'][:])):
                self.count=0
                for value in self.Observation['temperatura'][:,lat,lon]:
                    self.point.execute('''insert into dataObservation(
                    time,lat,lon,temperatura) values(?,?,?,?)''', (self.count, np.round(float(self.Observation['lat'][lat]), self.precisionCoord), np.round(float(self.Observation['lon'][lon]), self.precisionCoord), float(value)))
                    self.con.commit()
                    self.point.execute('''insert into CoordObservation(
                    lat,lon) values(?,?)''', (np.round(float(self.Observation['lat'][lat]), self.precisionCoord), np.round(float(self.Observation['lon'][lon]), self.precisionCoord)))
                    self.con.commit()
                    self.count+=1
        self.Observation.close()
        print("Concluído extração de dados observados")
        print("Extração de dados previstos")
        self.Forecast = nc.Dataset(self.nameFileForecast)
        for lat in range(len(self.Forecast['lat'][:])):
            for lon in range(len(self.Forecast['lon'][:])):
                self.count=0
                for value in self.Forecast['t2m'][:,lat,lon]:
                    self.point.execute('''insert into dataForecast(time,lat,lon,temperatura) values(?,?,?,?)''', (self.count, np.round(float(self.Forecast['lat'][lat]), self.precisionCoord), np.round(float(self.Forecast['lon'][lon]), self.precisionCoord), float(self.ConvKtoC(value))))
                    self.con.commit()
                    self.point.execute('''insert into CoordForecast(
                    lat,lon) values(?,?)''', (np.round(float(self.Forecast['lat'][lat]), self.precisionCoord), np.round(float(self.Forecast['lon'][lon]), self.precisionCoord)))
                    self.con.commit()
                    self.count+=1
        self.Forecast.close()
        print("Concluído extração de dados previstos")
        self.EncerrarCon()

        
    def NonePara0(self, registro):
        registro=list(registro)
        registro[len(registro)-1]=0.0
        return tuple(registro)
    
    def checaNone(self, registros):
        for i in range(len(registros)):
            if None in registros[i]:
                registros[i]=self.NonePara0(registros[i])
        return registros
    
    def RMSE(self, regs1, regs2):
        if len(regs1) != len(regs1):
            print("Calculo não realizado")
            return False
        resultado=0
        janela=len(regs1)
        for ind in range(len(regs1)):
            resultado+=(regs1[ind][len(regs1[ind])-1] - regs2[ind][len(regs2[ind])-1])**2
        resultado=(resultado/janela)**0.5
        return resultado
    
    def criaTabelaRMSE(self):
        self.Conectar()
        self.point.execute('''
            create table if not exists RMSE(
            id integer primary key autoincrement,
            janelaTempo text,
            lat float,
            lon float,
            rmse float)
            ''')
        self.EncerrarCon()
        return True
    
    def RMSEregistros(self, janela):
        self.criaTabelaRMSE()
        self.Conectar()
        self.point.execute('''select DISTINCT lat, lon from CoordObservation''')
        coordObservation = self.point.fetchall()
        self.point.execute('''select DISTINCT lat, lon from CoordForecast''')
        coordForecast = self.point.fetchall()
        
        for coordObs, coordFor in zip(coordObservation, coordForecast):
            self.point.execute('''select * from dataForecast where ROUND(lat,5) = ? and ROUND(lon,5) = ?''', (np.around(coordFor[0], self.precisionCoord), np.around(coordFor[1], self.precisionCoord)))
            regFor = self.point.fetchall()
            self.point.execute('''select * from dataObservation where ROUND(lat,5) = ? and ROUND(lon,5) = ?''', (np.around(coordObs[0], self.precisionCoord), np.around(coordObs[1], self.precisionCoord)))
            regObs = self.point.fetchall()
            regFor=self.checaNone(regFor)
            regObs=self.checaNone(regObs)
            
            if len(regFor) != len(regObs):
                print("Quantidade de registros diferentes")
                print("Pulando para o próximo par de coordenadas")
                break
            
            for ind in range(len(regFor)):
                if (ind+janela) > (len(regFor)-1):
                    break
                rmse=self.RMSE(regFor[ind:ind+janela], regObs[ind:ind+janela])
                tupla=("{}-{}".format(int(regFor[ind][1]), int(regFor[ind+janela][1])), regObs[ind][2], regObs[ind][3], rmse)
                self.point.execute('''insert into RMSE(janelaTempo,lat,lon,rmse) values(?,?,?,?)''', (tupla[0], np.round(float(tupla[1]), self.precisionCoord), np.round(float(tupla[2]), self.precisionCoord), np.round(float(tupla[3]), self.precisionCoord)))
                self.con.commit()
        self.EncerrarCon()
        return True
        
    
    def excluirOutliers(self, veto):
        test=[]
        for regi in veto:
            test.append(regi[2])
        z = np.abs(stats.zscore(test))
        location=np.where(z > 2.4)
        for i in location[0]:
            veto[i]= (veto[i][0], veto[i][1], 0.0)
        return veto
        
        
    def MapsPeriodos(self, png=False, excOutliers=False):
        self.Conectar()
        self.point.execute('''select DISTINCT janelaTempo from RMSE''')
        janelaTempo = self.point.fetchall()
        for periodo in janelaTempo:
            self.point.execute('''select lat, lon, rmse from RMSE where janelaTempo like ?''', (periodo))
            resultado= self.point.fetchall()
            if excOutliers == True:
                resultado = self.excluirOutliers(resultado)
            resultado = np.matrix(resultado)
            resultado = pd.DataFrame(resultado)
            ObjMap = folium.Map(self.centerMap, tiles='OpenStreetMap'.format(periodo[0]), zoom_start=7)
            HeatMap(resultado).add_to(ObjMap)
            ObjMap.save(os.path.join('MapasPeriodos', '{}.html'.format(periodo[0])))
            if png is True:
                img_data = ObjMap._to_png()
                img = Image.open(io.BytesIO(img_data))
                img.save(os.path.join('MapasPeriodos', '{}.png'.format(periodo[0])))
        self.EncerrarCon()
        return True
        

    
    def GrafSaoPaulo(self):
        self.Observation = nc.Dataset(self.nameFileObservation)
        lon=self.Observation["lon"][25]
        lat=self.Observation["lat"][7]
        self.Observation.close()
        self.Conectar()
        self.point.execute('''select * from RMSE where lat = ? and lon = ?''', (np.around(float(lat),self.precisionCoord), np.around(float(lon), self.precisionCoord)))
        registros = self.point.fetchall()
        self.EncerrarCon()
        x=[]
        y=[]
        ind=6
        for registro in registros:
            x.append(ind)
            ind+=1
            y.append(registro[len(registro)-1])
        plt.scatter(x, y, color='red')
        plt.plot(x, y, label='RMSE', linewidth=3)
        plt.grid(True)
        plt.xlabel("Série temporal (janela de 6 horas)")
        plt.ylabel("Root Mean Square Error (RMSE)")
        plt.title("Gráfico do índice RMSE de São Paulo ({},{})".format(np.around(float(lat),self.precisionCoord), np.around(float(lon), self.precisionCoord)))
        plt.savefig(os.path.join('MapasPeriodos', "Gráfico do índice RMSE de São Paulo.png"))

        
        
    def ConsultaRMSE(self):
        self.Conectar()
        self.point.execute('''select * from RMSE''')
        resultado = self.point.fetchall()
        print(resultado)
        self.EncerrarCon()



if __name__ == "__main__":
    fileForecast = 'forecast.nc'
    fileObservation = 'observation.nc'
    precisioncoord=5
    janelaRMSE=6
    clima = ClimaTempo("./data.db", precisioncoord, fileForecast, fileObservation)
    clima.ETL()
    clima.RMSEregistros(janelaRMSE)
    clima.MapsPeriodos(excOutliers=True)
    clima.GrafSaoPaulo()
    clima.ConsultaRMSE()