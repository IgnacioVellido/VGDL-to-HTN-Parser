(define (problem mia-p2-visita)
 (:domain mia-p2-visita)
 (:objects
  ;;lugares
  Casa_de_las_Rocas 
  Casa_Museo_Benlliure 
  Casa_Museo_de_San_Vicente 
  Centro_cultural_Fundacion_Bancaja
  Centro_del_Carmen_IVAM
  Centro_Julio_Gonzalez_IVAM
  Centro_La_Beneficencia 
  Museo_de_Bellas_Artes_de_Valencia
  Museo_de_Ceramica
  Museo_de_la_Catedral
  Museo_de_la_Ciudad
  Museo_de_prehistoria_y_de_las_culturas_de_Valencia
  Museo_del_Patriarca
  Museo_Fallero
  Museo_Paleontologico
  Museo_Taurino
  Museo_valenciano_de_la_ilustracion_y_la_modernidad
  Ayuntamiento
  Biblioteca
  Correos_y_Telegrafos
  Cortes_Valencianas_Palacio_de_Benicarlo
  El_Almudín
  Estación_del_Norte
  Estadio_de_Mestalla
  Fundacion_Bancaja
  La_Carcel_de_San_Vicente
  La_Lonja
  Mercado_Central
  Mercado_de_Colón
  Pabellon_Fuente_San_Luis
  Palacio_Arzobispal
  Palacio_de_Justicia
  Palacio_de_la_Generalitat
  Palacio_de_los_Condes_de_Alpuente
  Palacio_del_Almirante
  Palacio_del_Marques_de_Dos_Aguas
  Palacio_del_Marques_del_Campo
  Plaza_de_Toros
  Teatro_Principal
  Torre_del_Miguelete
  Basilica_de_la_Virgen
  Catedral
  Iglesia_de_San_Juan_de_la_Cruz
  Iglesia_de_San_Juan_del_Hospital
  Iglesia_Santos_Juanes
  Iglesia_y_Torre_de_Santa_Catalina
  Porta_del_Mar
  Torres_de_Quart
  Torres_de_Serranos
  Jardin_Botanico
  Jardin_de_Monforte
  Jardines_de_la_Glorieta
  Paseo_de_la_Alameda
  Plaza_de_la_Virgen
  Plaza_Redonda
  Tribunal_de_las_Aguas
  Jardines_de_Viveros
  
  turista1
  taxi
 )
 (:init
    ;; lugares de visita
    (museo Casa_de_las_Rocas 0)
    (museo Casa_Museo_Benlliure 1)
    (museo Casa_Museo_de_San_Vicente 2)
    (exposicion Centro_cultural_Fundacion_Bancaja 3)
    (museo Centro_del_Carmen_IVAM 4)
    (museo Centro_Julio_Gonzalez_IVAM 5)
    (edificio Centro_La_Beneficencia 6)
    (museo Museo_de_Bellas_Artes_de_Valencia 7)
    (museo Museo_de_Ceramica 8)
    (museo Museo_de_la_Catedral 9)
    (museo Museo_de_la_Ciudad 10)
    (museo Museo_de_prehistoria_y_de_las_culturas_de_Valencia 11)
    (museo Museo_del_Patriarca 12)
    (museo Museo_Fallero 13)
    (museo Museo_Paleontologico 14)
    (museo Museo_Taurino 15)
    (museo Museo_valenciano_de_la_ilustracion_y_la_modernidad 16)
    (edificio Ayuntamiento 17)
    (edificio Biblioteca 18)
    (edificio Correos_y_Telegrafos 20)
    (edificio Cortes_Valencianas_Palacio_de_Benicarlo 21)
    (edificio El_Almudín 22)
    (edificio Estación_del_Norte 23)
    (edificio Estadio_de_Mestalla 24)
    (exposicion Fundacion_Bancaja 25)
    (edificio La_Carcel_de_San_Vicente 26)
    (edificio La_Lonja 27)
    (edificio Mercado_Central 28)
    (edificio Mercado_de_Colón 29)
    (edificio Pabellon_Fuente_San_Luis 30)
    (palacio Palacio_Arzobispal 31)
    (palacio Palacio_de_Justicia 32)
    (palacio Palacio_de_la_Generalitat 33)
    (palacio Palacio_de_los_Condes_de_Alpuente 34)
    (palacio Palacio_del_Almirante 35)
    (palacio Palacio_del_Marques_de_Dos_Aguas 36)
    (palacio Palacio_del_Marques_del_Campo 37)
    (edificio Plaza_de_Toros 38)
    (espectaculo Teatro_Principal 39)
    (edificio Torre_del_Miguelete 40)
    (iglesia Basilica_de_la_Virgen 41)
    (iglesia Catedral 42)
    (iglesia Iglesia_de_San_Juan_de_la_Cruz 43)
    (iglesia Iglesia_de_San_Juan_del_Hospital 44)
    (iglesia Iglesia_Santos_Juanes 45)
    (iglesia Iglesia_y_Torre_de_Santa_Catalina 46)
    (edificio Porta_del_Mar 47)
    (edificio Torres_de_Quart 48)
    (edificio Torres_de_Serranos 49)
    (parque Jardin_Botanico 50)
    (parque Jardin_de_Monforte 51)
    (parque Jardines_de_la_Glorieta 52)
    (parque Paseo_de_la_Alameda 53)
    (plaza Plaza_de_la_Virgen 54)
    (plaza Plaza_Redonda 55)
    (edificio Tribunal_de_las_Aguas 56)
    (parque Jardines_de_Viveros 57)

    ;; Precio de las visitas
    (= (precio Casa_de_las_Rocas) 0)
    (= (precio Casa_Museo_Benlliure) 0)
    (= (precio Casa_Museo_de_San_Vicente) 0)
    (= (precio Centro_cultural_Fundacion_Bancaja) 0)
    (= (precio Centro_del_Carmen_IVAM) 0)
    (= (precio Centro_Julio_Gonzalez_IVAM) 0)
    (= (precio Centro_La_Beneficencia) 0)
    (= (precio Museo_de_Bellas_Artes_de_Valencia) 3)
    (= (precio Museo_de_Ceramica) 3)
    (= (precio Museo_de_la_Catedral) 3)
    (= (precio Museo_de_la_Ciudad) 6)
    (= (precio Museo_de_prehistoria_y_de_las_culturas_de_Valencia) 3)
    (= (precio Museo_del_Patriarca) 1)
    (= (precio Museo_Fallero) 10)
    (= (precio Museo_Paleontologico) 3)
    (= (precio Museo_Taurino) 3)
    (= (precio Museo_valenciano_de_la_ilustracion_y_la_modernidad) 0)
    (= (precio Ayuntamiento) 0)
    (= (precio Biblioteca) 0)
    (= (precio Correos_y_Telegrafos) 0)
    (= (precio Cortes_Valencianas_Palacio_de_Benicarlo) 0)
    (= (precio El_Almudín) 0)
    (= (precio Estación_del_Norte) 0)
    (= (precio Estadio_de_Mestalla) 0)
    (= (precio Fundacion_Bancaja) 0)
    (= (precio La_Carcel_de_San_Vicente) 0)
    (= (precio La_Lonja) 0)
    (= (precio Mercado_Central) 0)
    (= (precio Mercado_de_Colón) 0)
    (= (precio Pabellon_Fuente_San_Luis) 0)
    (= (precio Palacio_Arzobispal) 4)
    (= (precio Palacio_de_Justicia) 3)
    (= (precio Palacio_de_la_Generalitat) 0)
    (= (precio Palacio_de_los_Condes_de_Alpuente) 3)
    (= (precio Palacio_del_Almirante) 3)
    (= (precio Palacio_del_Marques_de_Dos_Aguas) 3)
    (= (precio Palacio_del_Marques_del_Campo) 3)
    (= (precio Plaza_de_Toros) 0)
    (= (precio Teatro_Principal) 0)
    (= (precio Torre_del_Miguelete) 0)
    (= (precio Basilica_de_la_Virgen) 0)
    (= (precio Catedral) 0)
    (= (precio Iglesia_de_San_Juan_de_la_Cruz) 0)
    (= (precio Iglesia_de_San_Juan_del_Hospital) 0)
    (= (precio Iglesia_Santos_Juanes) 0)
    (= (precio Iglesia_y_Torre_de_Santa_Catalina) 0)
    (= (precio Porta_del_Mar) 0)
    (= (precio Torres_de_Quart) 0)
    (= (precio Torres_de_Serranos) 0)
    (= (precio Jardin_Botanico) 0)
    (= (precio Jardin_de_Monforte) 0)
    (= (precio Jardines_de_la_Glorieta) 0)
    (= (precio Paseo_de_la_Alameda) 0)
    (= (precio Plaza_de_la_Virgen) 0)
    (= (precio Plaza_Redonda) 0)
    (= (precio Tribunal_de_las_Aguas) 0)
    (= (precio Jardines_de_Viveros) 0)

    ;; Localización de los lugares de interés
    (= (posicion Casa_de_las_Rocas) 2465)
    (= (posicion Casa_Museo_Benlliure) 2244)
    (= (posicion Casa_Museo_de_San_Vicente) 1964)
    (= (posicion Centro_cultural_Fundacion_Bancaja) 1997)
    (= (posicion Centro_del_Carmen_IVAM) 2491)
    (= (posicion Centro_Julio_Gonzalez_IVAM) 1306)
    (= (posicion Centro_La_Beneficencia) 2411)
    (= (posicion Museo_de_Bellas_Artes_de_Valencia) 986)
    (= (posicion Museo_de_Ceramica) 1832)
    (= (posicion Museo_de_la_Catedral) 2244)
    (= (posicion Museo_de_la_Ciudad) 2235)
    (= (posicion Museo_de_prehistoria_y_de_las_culturas_de_Valencia) 2411)
    (= (posicion Museo_del_Patriarca) 1835)
    (= (posicion Museo_Fallero) 537)
    (= (posicion Museo_Paleontologico) 1662)
    (= (posicion Museo_Taurino) 1501)
    (= (posicion Museo_valenciano_de_la_ilustracion_y_la_modernidad) 1633)
    (= (posicion Ayuntamiento) 1657)
    (= (posicion Biblioteca) 1706)
    (= (posicion Correos_y_Telegrafos) 1667)
    (= (posicion Cortes_Valencianas_Palacio_de_Benicarlo) 2418)
    (= (posicion El_Almudín) 2267)
    (= (posicion Estación_del_Norte) 1527)
    (= (posicion Estadio_de_Mestalla) 883)
    (= (posicion Fundacion_Bancaja) 1997)
    (= (posicion La_Carcel_de_San_Vicente) 2186)
    (= (posicion La_Lonja) 2060)
    (= (posicion Mercado_Central) 2020)
    (= (posicion Mercado_de_Colón) 1590)
    (= (posicion Pabellon_Fuente_San_Luis) 363)
    (= (posicion Palacio_Arzobispal) 2186)
    (= (posicion Palacio_de_Justicia) 1834)
    (= (posicion Palacio_de_la_Generalitat) 2275)
    (= (posicion Palacio_de_los_Condes_de_Alpuente) 2278)
    (= (posicion Palacio_del_Almirante) 2164)
    (= (posicion Palacio_del_Marques_de_Dos_Aguas) 1832)
    (= (posicion Palacio_del_Marques_del_Campo) 2235)
    (= (posicion Plaza_de_Toros) 1611)
    (= (posicion Teatro_Principal) 1698)
    (= (posicion Torre_del_Miguelete) 2244)
    (= (posicion Basilica_de_la_Virgen) 2244)
    (= (posicion Catedral) 2244)
    (= (posicion Iglesia_de_San_Juan_de_la_Cruz) 1794)
    (= (posicion Iglesia_de_San_Juan_del_Hospital) 2096)
    (= (posicion Iglesia_Santos_Juanes) 2068)
    (= (posicion Iglesia_y_Torre_de_Santa_Catalina) 2005)
    (= (posicion Porta_del_Mar) 1802)
    (= (posicion Torres_de_Quart) 2141)
    (= (posicion Torres_de_Serranos) 2457)
    (= (posicion Jardin_Botanico) 1283)
    (= (posicion Jardin_de_Monforte) 907)
    (= (posicion Jardines_de_la_Glorieta) 1888)
    (= (posicion Paseo_de_la_Alameda) 902)
    (= (posicion Plaza_de_la_Virgen) 2237)
    (= (posicion Plaza_Redonda) 1957)
    (= (posicion Tribunal_de_las_Aguas) 2237)
    (= (posicion Jardines_de_Viveros) 986)

    (= (precio taxi) 3)
    (prefiere turista1 palacios)
    (prefiere turista1 edificios)
    (= (dinero_disponible turista1) 100)
    (= (limite_andando turista1) 350) 
    (= (posicion turista1) 2263)
 )
 (:tasks-goal
  :tasks(
      (visitar_palacio turista1 Palacio_de_la_Generalitat)
      (visitar_palacio turista1 Palacio_de_los_Condes_de_Alpuente)
      (visitar_edificio turista1 Torres_de_Quart))
 )
)
