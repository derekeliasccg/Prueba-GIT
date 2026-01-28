import glob
import os
from typing import List
from juego import JuegoUno


def listar_partidas_guardadas() -> List[str]:
    return glob.glob("*.pkl")


def menu_principal() -> None:
    print("\n" + "="*50)
    print("       BIENVENIDO AL JUEGO UNO")
    print("="*50)
    print("\n1. Nueva Partida")
    print("2. Cargar Partida")
    print("3. Salir\n")
    
    opcion = input("Selecciona una opción: ").strip()

    juego = None

    if opcion == "1":
        juego = JuegoUno()
        juego.iniciar()
    
    elif opcion == "2":
        archivos = listar_partidas_guardadas()
        
        if not archivos:
            print("No hay partidas guardadas.")
            print("Iniciando partida nueva...\n")
            juego = JuegoUno()
            juego.iniciar()
        else:
            print("\nPartidas encontradas:")
            for i, archivo in enumerate(archivos, 1):
                print(f"  {i}. {archivo}")
            
            try:
                seleccion = int(input("\nElige el número: ")) - 1
                if 0 <= seleccion < len(archivos):
                    juego = JuegoUno.cargar_partida(archivos[seleccion])
                    if juego:
                        print(f"Cargando {archivos[seleccion]}...\n")
                        juego.iniciar()
                    else:
                        print("Error al cargar la partida.")
                else:
                    print("Selección inválida.")
            except ValueError:
                print("Entrada no válida.")
    elif opcion == "3":
        print("¡Hasta luego!")
    else:
        print("Opción no válida.")
if __name__ == "__main__":
    menu_principal()
