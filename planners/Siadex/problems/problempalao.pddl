;;---------------------------------------------
;;Problema de Prueba para el dominio little_siadex

(define (problem problema01)
(:domain mini_siadex)
(:objects
	Rastrillos - Metodo_Ataque
	AguaYRetardantes - Metodo_Ataque

	Vehiculo01 - Vehiculo_Terrestre
	Vehiculo02 - Vehiculo_Terrestre

	Reten01 - Recursos_Humanos
	Reten02 - Recursos_Humanos

    CEDEFO_PuertoLobo - Instalacion
    CEDEFO_Orgiva - Instalacion

    LLanoPerdid - Infoca_GIS
    SierraElvira00 - Infoca_GIS
    SierraElvira01 - Infoca_GIS
    SierraElvira02 - Infoca_GIS
    SierraElvira03 - Infoca_GIS
    SierraElvira04 - Infoca_GIS
    SierraElvira05 - Infoca_GIS
    SierraElvira06 - Infoca_GIS
    SierraElvira07 - Infoca_GIS
    SierraElvira08 - Infoca_GIS
    SierraElvira09 - Infoca_GIS
    
    sierraelvira10 - infoca_gis
    sierraelvira11 - infoca_gis
    SierraElvira12 - Infoca_GIS
    SierraElvira13 - Infoca_GIS
    SierraElvira14 - Infoca_GIS
    SierraElvira15 - Infoca_GIS
    SierraElvira16 - Infoca_GIS
    SierraElvira17 - Infoca_GIS
    SierraElvira18 - Infoca_GIS
    SierraElvira19 - Infoca_GIS
    
    sierraelvira20 - infoca_gis
    sierraelvira21 - infoca_gis
    SierraElvira22 - Infoca_GIS
    SierraElvira23 - Infoca_GIS
    SierraElvira24 - Infoca_GIS
    SierraElvira25 - Infoca_GIS
    SierraElvira26 - Infoca_GIS
    SierraElvira27 - Infoca_GIS
    SierraElvira28 - Infoca_GIS
    SierraElvira29 - Infoca_GIS
    
    sierraelvira30 - infoca_gis
    sierraelvira31 - infoca_gis
    SierraElvira32 - Infoca_GIS
    SierraElvira33 - Infoca_GIS
    SierraElvira34 - Infoca_GIS
    SierraElvira35 - Infoca_GIS
    SierraElvira36 - Infoca_GIS
    SierraElvira37 - Infoca_GIS
    SierraElvira38 - Infoca_GIS
    SierraElvira39 - Infoca_GIS
    
    sierraelvira40 - infoca_gis
    sierraelvira41 - infoca_gis
    SierraElvira42 - Infoca_GIS
    SierraElvira43 - Infoca_GIS
    SierraElvira44 - Infoca_GIS
    SierraElvira45 - Infoca_GIS
    SierraElvira46 - Infoca_GIS
    SierraElvira47 - Infoca_GIS
    SierraElvira48 - Infoca_GIS
    SierraElvira49 - Infoca_GIS
    
    sierraelvira50 - infoca_gis
    sierraelvira51 - infoca_gis
    SierraElvira52 - Infoca_GIS
    SierraElvira53 - Infoca_GIS
    SierraElvira54 - Infoca_GIS
    SierraElvira55 - Infoca_GIS
    SierraElvira56 - Infoca_GIS
    SierraElvira57 - Infoca_GIS
    SierraElvira58 - Infoca_GIS
    SierraElvira59 - Infoca_GIS
    
    sierraelvira60 - infoca_gis
    sierraelvira61 - infoca_gis
    SierraElvira62 - Infoca_GIS
    SierraElvira63 - Infoca_GIS
    SierraElvira64 - Infoca_GIS
    SierraElvira65 - Infoca_GIS
    SierraElvira66 - Infoca_GIS
    SierraElvira67 - Infoca_GIS
    SierraElvira68 - Infoca_GIS
    SierraElvira69 - Infoca_GIS
    
    sierraelvira70 - infoca_gis
    sierraelvira71 - infoca_gis
    SierraElvira72 - Infoca_GIS
    SierraElvira73 - Infoca_GIS
    SierraElvira74 - Infoca_GIS
    SierraElvira75 - Infoca_GIS
    SierraElvira76 - Infoca_GIS
    SierraElvira77 - Infoca_GIS
    SierraElvira78 - Infoca_GIS
    SierraElvira79 - Infoca_GIS
    
    sierraelvira80 - infoca_gis
    sierraelvira81 - infoca_gis
    SierraElvira82 - Infoca_GIS
    SierraElvira83 - Infoca_GIS
    SierraElvira84 - Infoca_GIS
    SierraElvira85 - Infoca_GIS
    SierraElvira86 - Infoca_GIS
    SierraElvira87 - Infoca_GIS
    SierraElvira88 - Infoca_GIS
    SierraElvira89 - Infoca_GIS
    
    sierraelvira90 - infoca_gis
    sierraelvira91 - infoca_gis
    SierraElvira92 - Infoca_GIS
    SierraElvira93 - Infoca_GIS
    SierraElvira94 - Infoca_GIS
    SierraElvira95 - Infoca_GIS
    SierraElvira96 - Infoca_GIS
    SierraElvira97 - Infoca_GIS
    SierraElvira98 - Infoca_GIS
    SierraElvira99 - Infoca_GIS
    
)
(:init
	(asignado_en Vehiculo01 CEDEFO_PuertoLobo)
	(posicion_actual Vehiculo01 CEDEFO_PuertoLobo)
	(asignado_en Vehiculo02 CEDEFO_Orgiva)
	(posicion_actual Vehiculo02 CEDEFO_Orgiva)
	(asignado_en Reten01 CEDEFO_PuertoLobo)
	(posicion_actual Reten01 CEDEFO_PuertoLobo)
	(asignado_en Reten02 CEDEFO_Orgiva)
	(posicion_actual Reten02 CEDEFO_Orgiva)
	(coordenadas CEDEFO_Orgiva 2 2 2)
	(coordenadas LlanoPerdid 3 3 3)

	(coordenadas SierraElvira00 4 4 4)
	(coordenadas SierraElvira01 4 4 4)
	(coordenadas SierraElvira02 4 4 4)
	(coordenadas SierraElvira03 4 4 4)
	(coordenadas SierraElvira04 4 4 4)
	(coordenadas SierraElvira05 4 4 4)
	(coordenadas SierraElvira06 4 4 4)
	(coordenadas SierraElvira07 4 4 4)
	(coordenadas SierraElvira08 4 4 4)
	(coordenadas SierraElvira09 4 4 4)

	(coordenadas SierraElvira10 4 4 4)
	(coordenadas SierraElvira11 4 4 4)
	(coordenadas SierraElvira12 4 4 4)
	(coordenadas SierraElvira13 4 4 4)
	(coordenadas SierraElvira14 4 4 4)
	(coordenadas SierraElvira15 4 4 4)
	(coordenadas SierraElvira16 4 4 4)
	(coordenadas SierraElvira17 4 4 4)
	(coordenadas SierraElvira18 4 4 4)
	(coordenadas SierraElvira19 4 4 4)

	(coordenadas SierraElvira20 4 4 4)
	(coordenadas SierraElvira21 4 4 4)
	(coordenadas SierraElvira22 4 4 4)
	(coordenadas SierraElvira23 4 4 4)
	(coordenadas SierraElvira24 4 4 4)
	(coordenadas SierraElvira25 4 4 4)
	(coordenadas SierraElvira26 4 4 4)
	(coordenadas SierraElvira27 4 4 4)
	(coordenadas SierraElvira28 4 4 4)
	(coordenadas SierraElvira29 4 4 4)

	(coordenadas SierraElvira30 4 4 4)
	(coordenadas SierraElvira31 4 4 4)
	(coordenadas SierraElvira32 4 4 4)
	(coordenadas SierraElvira33 4 4 4)
	(coordenadas SierraElvira34 4 4 4)
	(coordenadas SierraElvira35 4 4 4)
	(coordenadas SierraElvira36 4 4 4)
	(coordenadas SierraElvira37 4 4 4)
	(coordenadas SierraElvira38 4 4 4)
	(coordenadas SierraElvira39 4 4 4)

	(coordenadas SierraElvira40 4 4 4)
	(coordenadas SierraElvira41 4 4 4)
	(coordenadas SierraElvira42 4 4 4)
	(coordenadas SierraElvira43 4 4 4)
	(coordenadas SierraElvira44 4 4 4)
	(coordenadas SierraElvira45 4 4 4)
	(coordenadas SierraElvira46 4 4 4)
	(coordenadas SierraElvira47 4 4 4)
	(coordenadas SierraElvira48 4 4 4)
	(coordenadas SierraElvira49 4 4 4)

	(coordenadas SierraElvira50 4 4 4)
	(coordenadas SierraElvira51 4 4 4)
	(coordenadas SierraElvira52 4 4 4)
	(coordenadas SierraElvira53 4 4 4)
	(coordenadas SierraElvira54 4 4 4)
	(coordenadas SierraElvira55 4 4 4)
	(coordenadas SierraElvira56 4 4 4)
	(coordenadas SierraElvira57 4 4 4)
	(coordenadas SierraElvira58 4 4 4)
	(coordenadas SierraElvira59 4 4 4)

	(coordenadas SierraElvira60 4 4 4)
	(coordenadas SierraElvira61 4 4 4)
	(coordenadas SierraElvira62 4 4 4)
	(coordenadas SierraElvira63 4 4 4)
	(coordenadas SierraElvira64 4 4 4)
	(coordenadas SierraElvira65 4 4 4)
	(coordenadas SierraElvira66 4 4 4)
	(coordenadas SierraElvira67 4 4 4)
	(coordenadas SierraElvira68 4 4 4)
	(coordenadas SierraElvira69 4 4 4)

	(coordenadas SierraElvira70 4 4 4)
	(coordenadas SierraElvira71 4 4 4)
	(coordenadas SierraElvira72 4 4 4)
	(coordenadas SierraElvira73 4 4 4)
	(coordenadas SierraElvira74 4 4 4)
	(coordenadas SierraElvira75 4 4 4)
	(coordenadas SierraElvira76 4 4 4)
	(coordenadas SierraElvira77 4 4 4)
	(coordenadas SierraElvira78 4 4 4)
	(coordenadas SierraElvira79 4 4 4)

	(coordenadas SierraElvira80 4 4 4)
	(coordenadas SierraElvira81 4 4 4)
	(coordenadas SierraElvira82 4 4 4)
	(coordenadas SierraElvira83 4 4 4)
	(coordenadas SierraElvira84 4 4 4)
	(coordenadas SierraElvira85 4 4 4)
	(coordenadas SierraElvira86 4 4 4)
	(coordenadas SierraElvira87 4 4 4)
	(coordenadas SierraElvira88 4 4 4)
	(coordenadas SierraElvira89 4 4 4)

	(coordenadas SierraElvira90 4 4 4)
	(coordenadas SierraElvira91 4 4 4)
	(coordenadas SierraElvira92 4 4 4)
	(coordenadas SierraElvira93 4 4 4)
	(coordenadas SierraElvira94 4 4 4)
	(coordenadas SierraElvira95 4 4 4)
	(coordenadas SierraElvira96 4 4 4)
	(coordenadas SierraElvira97 4 4 4)
	(coordenadas SierraElvira98 4 4 4)
	(coordenadas SierraElvira99 4 4 4)

	(coordenadas CEDEFO_PuertoLobo 1 1 1)

	(fuego_en SierraElvira00)
	(fuego_en SierraElvira01)
	(fuego_en SierraElvira02)
	(fuego_en SierraElvira03)
	(fuego_en SierraElvira04)
	(fuego_en SierraElvira05)
	(fuego_en SierraElvira06)
	(fuego_en SierraElvira07)
	(fuego_en SierraElvira08)
	(fuego_en SierraElvira09)

	(fuego_en SierraElvira10)
	(fuego_en SierraElvira11)
	(fuego_en SierraElvira12)
	(fuego_en SierraElvira13)
	(fuego_en SierraElvira14)
	(fuego_en SierraElvira15)
	(fuego_en SierraElvira16)
	(fuego_en SierraElvira17)
	(fuego_en SierraElvira18)
	(fuego_en SierraElvira19)

	(fuego_en SierraElvira20)
	(fuego_en SierraElvira21)
	(fuego_en SierraElvira22)
	(fuego_en SierraElvira23)
	(fuego_en SierraElvira24)
	(fuego_en SierraElvira25)
	(fuego_en SierraElvira26)
	(fuego_en SierraElvira27)
	(fuego_en SierraElvira28)
	(fuego_en SierraElvira29)

	(fuego_en SierraElvira30)
	(fuego_en SierraElvira31)
	(fuego_en SierraElvira32)
	(fuego_en SierraElvira33)
	(fuego_en SierraElvira34)
	(fuego_en SierraElvira35)
	(fuego_en SierraElvira36)
	(fuego_en SierraElvira37)
	(fuego_en SierraElvira38)
	(fuego_en SierraElvira39)

	(fuego_en SierraElvira40)
	(fuego_en SierraElvira41)
	(fuego_en SierraElvira42)
	(fuego_en SierraElvira43)
	(fuego_en SierraElvira44)
	(fuego_en SierraElvira45)
	(fuego_en SierraElvira46)
	(fuego_en SierraElvira47)
	(fuego_en SierraElvira48)
	(fuego_en SierraElvira49)

	(fuego_en SierraElvira50)
	(fuego_en SierraElvira51)
	(fuego_en SierraElvira52)
	(fuego_en SierraElvira53)
	(fuego_en SierraElvira54)
	(fuego_en SierraElvira55)
	(fuego_en SierraElvira56)
	(fuego_en SierraElvira57)
	(fuego_en SierraElvira58)
	(fuego_en SierraElvira59)

	(fuego_en SierraElvira60)
	(fuego_en SierraElvira61)
	(fuego_en SierraElvira62)
	(fuego_en SierraElvira63)
	(fuego_en SierraElvira64)
	(fuego_en SierraElvira65)
	(fuego_en SierraElvira66)
	(fuego_en SierraElvira67)
	(fuego_en SierraElvira68)
	(fuego_en SierraElvira69)

	(fuego_en SierraElvira70)
	(fuego_en SierraElvira71)
	(fuego_en SierraElvira72)
	(fuego_en SierraElvira73)
	(fuego_en SierraElvira74)
	(fuego_en SierraElvira75)
	(fuego_en SierraElvira76)
	(fuego_en SierraElvira77)
	(fuego_en SierraElvira78)
	(fuego_en SierraElvira79)

	(fuego_en SierraElvira80)
	(fuego_en SierraElvira81)
	(fuego_en SierraElvira82)
	(fuego_en SierraElvira83)
	(fuego_en SierraElvira84)
	(fuego_en SierraElvira85)
	(fuego_en SierraElvira86)
	(fuego_en SierraElvira87)
	(fuego_en SierraElvira88)
	(fuego_en SierraElvira89)

	(fuego_en SierraElvira90)
	(fuego_en SierraElvira91)
	(fuego_en SierraElvira92)
	(fuego_en SierraElvira93)
	(fuego_en SierraElvira94)
	(fuego_en SierraElvira95)
	(fuego_en SierraElvira96)
	(fuego_en SierraElvira97)
	(fuego_en SierraElvira98)
	(fuego_en SierraElvira99)

)
(:tasks-goal
    :tasks
    (
    (extinguir SierraElvira00)
    (extinguir SierraElvira01)
    (extinguir SierraElvira02)
    (extinguir SierraElvira03)
    (extinguir SierraElvira04)
    (extinguir SierraElvira05)
    (extinguir SierraElvira06)
    (extinguir SierraElvira07)
    (extinguir SierraElvira08)
    (extinguir SierraElvira09)

    (extinguir SierraElvira10)
    (extinguir SierraElvira11)
    (extinguir SierraElvira12)
    (extinguir SierraElvira13)
    (extinguir SierraElvira14)
    (extinguir SierraElvira15)
    (extinguir SierraElvira16)
    (extinguir SierraElvira17)
    (extinguir SierraElvira18)
    (extinguir SierraElvira19)

    (extinguir SierraElvira20)
    (extinguir SierraElvira21)
    (extinguir SierraElvira22)
    (extinguir SierraElvira23)
    (extinguir SierraElvira24)
    (extinguir SierraElvira25)
    (extinguir SierraElvira26)
    (extinguir SierraElvira27)
    (extinguir SierraElvira28)
    (extinguir SierraElvira29)

    (extinguir SierraElvira30)
    (extinguir SierraElvira31)
    (extinguir SierraElvira32)
    (extinguir SierraElvira33)
    (extinguir SierraElvira34)
    (extinguir SierraElvira35)
    (extinguir SierraElvira36)
    (extinguir SierraElvira37)
    (extinguir SierraElvira38)
    (extinguir SierraElvira39)

    (extinguir SierraElvira40)
    (extinguir SierraElvira41)
    (extinguir SierraElvira42)
    (extinguir SierraElvira43)
    (extinguir SierraElvira44)
    (extinguir SierraElvira45)
    (extinguir SierraElvira46)
    (extinguir SierraElvira47)
    (extinguir SierraElvira48)
    (extinguir SierraElvira49)

    (extinguir SierraElvira50)
    (extinguir SierraElvira51)
    (extinguir SierraElvira52)
    (extinguir SierraElvira53)
    (extinguir SierraElvira54)
    (extinguir SierraElvira55)
    (extinguir SierraElvira56)
    (extinguir SierraElvira57)
    (extinguir SierraElvira58)
    (extinguir SierraElvira59)

    (extinguir SierraElvira60)
    (extinguir SierraElvira61)
    (extinguir SierraElvira62)
    (extinguir SierraElvira63)
    (extinguir SierraElvira64)
    (extinguir SierraElvira65)
    (extinguir SierraElvira66)
    (extinguir SierraElvira67)
    (extinguir SierraElvira68)
    (extinguir SierraElvira69)

    (extinguir SierraElvira70)
    (extinguir SierraElvira71)
    (extinguir SierraElvira72)
    (extinguir SierraElvira73)
    (extinguir SierraElvira74)
    (extinguir SierraElvira75)
    (extinguir SierraElvira76)
    (extinguir SierraElvira77)
    (extinguir SierraElvira78)
    (extinguir SierraElvira79)

    (extinguir SierraElvira80)
    (extinguir SierraElvira81)
    (extinguir SierraElvira82)
    (extinguir SierraElvira83)
    (extinguir SierraElvira84)
    (extinguir SierraElvira85)
    (extinguir SierraElvira86)
    (extinguir SierraElvira87)
    (extinguir SierraElvira88)
    (extinguir SierraElvira89)

    (extinguir SierraElvira90)
    (extinguir SierraElvira91)
    (extinguir SierraElvira92)
    (extinguir SierraElvira93)
    (extinguir SierraElvira94)
    (extinguir SierraElvira95)
    (extinguir SierraElvira96)
    (extinguir SierraElvira97)
    (extinguir SierraElvira98)
    (extinguir SierraElvira99)

    )
)
)
