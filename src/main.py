"""
Actividad 25: Simulación Interactiva de los Elementos del Aprendizaje por Refuerzo
Maestría en Inteligencia Artificial - TecNM / ITSU
Materia: Aprendizaje Automático
Autor: Juan Pablo Figueroa Moran (M26040059)
Repositorio: https://github.com/juanpablofm92/Actividad25.git
"""

import sys
import time
import random
from typing import Dict, List, Tuple

# Asegurar soporte UTF-8 en consola de Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class RLEnvironmentSimulation:
    def __init__(self, name: str, description: str, states: List[str], actions: List[str]):
        self.name = name
        self.description = description
        self.states = states
        self.actions = actions
        self.current_state = states[0]
        self.accumulated_reward = 0.0
        self.trajectory: List[Dict] = []
        self.step_count = 0

    def reset(self, initial_state: str = None):
        self.current_state = initial_state if initial_state else self.states[0]
        self.accumulated_reward = 0.0
        self.trajectory = []
        self.step_count = 0
        return self.current_state

    def step(self, action: str) -> Tuple[str, float, bool, str]:
        raise NotImplementedError


class AutonomousParkingEnv(RLEnvironmentSimulation):
    """Escenario 1: Coche autónomo maniobrando para estacionarse."""
    def __init__(self):
        states = ["Lejos_del_Cajon", "Alineandose", "Espacio_Estrecho", "Estacionado_Exitoso", "Colision"]
        actions = ["Avanzar_Lento", "Girar_Volante", "Frenar", "Reversa_Cuidadosa"]
        super().__init__("Coche Autónomo en Estacionamiento", "Navegación y maniobra de precisión vehicular", states, actions)

    def step(self, action: str) -> Tuple[str, float, bool, str]:
        self.step_count += 1
        done = False
        reward = -1.0  # Costo por paso de tiempo
        info = ""

        if self.current_state == "Lejos_del_Cajon":
            if action in ["Avanzar_Lento", "Girar_Volante"]:
                self.current_state = "Alineandose"
                reward = 5.0
                info = "El vehículo se aproximó al área del cajón de estacionamiento."
            else:
                reward = -2.0
                info = "Frenó o retrocedió innecesariamente."

        elif self.current_state == "Alineandose":
            if action == "Girar_Volante":
                self.current_state = "Espacio_Estrecho"
                reward = 8.0
                info = "Vehículo correctamente perfilado hacia el cajón."
            elif action == "Reversa_Cuidadosa":
                self.current_state = "Lejos_del_Cajon"
                reward = -3.0
                info = "Retrocedió alejándose del objetivo."
            else:
                if random.random() < 0.25:
                    self.current_state = "Colision"
                    reward = -100.0
                    done = True
                    info = "¡Impacto contra la acera por avanzar sin girar!"
                else:
                    self.current_state = "Espacio_Estrecho"
                    reward = 2.0
                    info = "Entró con poco margen de giro."

        elif self.current_state == "Espacio_Estrecho":
            if action == "Reversa_Cuidadosa":
                self.current_state = "Estacionado_Exitoso"
                reward = 100.0
                done = True
                info = "¡Maniobra impecable! Auto centrado y frenado con éxito."
            elif action == "Avanzar_Lento":
                self.current_state = "Colision"
                reward = -100.0
                done = True
                info = "¡Colisión frontal contra el vehículo delantero!"
            else:
                reward = -5.0
                info = "Acción indecisa dentro del espacio estrecho."

        self.accumulated_reward += reward
        self.trajectory.append({
            "step": self.step_count,
            "action": action,
            "next_state": self.current_state,
            "reward": reward,
            "accumulated": self.accumulated_reward,
            "info": info
        })
        return self.current_state, reward, done, info


class CoinCollectorGameEnv(RLEnvironmentSimulation):
    """Escenario 2: Videojuego arcade 2D de recolección de gemas y evasión de trampas."""
    def __init__(self):
        states = ["Pasillo_Inicial", "Zona_Monedas_Bronce", "Bóveda_Moneda_Oro", "Nivel_Superado", "Atrapado_por_Monstruo"]
        actions = ["Mover_Norte", "Mover_Este", "Saltar_Trampa", "Recoger_Item"]
        super().__init__("Videojuego: Recolección de Monedas", "Agente que maximiza puntos evadiendo enemigos", states, actions)

    def step(self, action: str) -> Tuple[str, float, bool, str]:
        self.step_count += 1
        done = False
        reward = -0.5
        info = ""

        if self.current_state == "Pasillo_Inicial":
            if action in ["Mover_Este", "Mover_Norte"]:
                self.current_state = "Zona_Monedas_Bronce"
                reward = 2.0
                info = "Entrando a la cámara de botín menor."
            else:
                reward = -1.0
                info = "Movimiento bloqueado por muro."

        elif self.current_state == "Zona_Monedas_Bronce":
            if action == "Recoger_Item":
                reward = 15.0
                info = "¡Recogiste monedas de bronce (+15 pts)!"
                self.current_state = "Bóveda_Moneda_Oro"
            elif action == "Mover_Norte":
                self.current_state = "Bóveda_Moneda_Oro"
                reward = 5.0
                info = "Avanzaste directo a la cámara dorada."
            else:
                reward = -2.0
                info = "Dando vueltas en el pasillo de bronce."

        elif self.current_state == "Bóveda_Moneda_Oro":
            if action == "Saltar_Trampa":
                reward = 20.0
                info = "¡Esquivaste la trampa de pinchos giratoria!"
            elif action == "Recoger_Item":
                self.current_state = "Nivel_Superado"
                reward = 80.0
                done = True
                info = "¡Tomaste el cofre dorado y alcanzaste la salida triunfal!"
            else:
                if random.random() < 0.4:
                    self.current_state = "Atrapado_por_Monstruo"
                    reward = -60.0
                    done = True
                    info = "¡El guardián del calabozo te interceptó!"
                else:
                    reward = -5.0
                    info = "Peligro: El monstruo se aproxima."

        self.accumulated_reward += reward
        self.trajectory.append({
            "step": self.step_count,
            "action": action,
            "next_state": self.current_state,
            "reward": reward,
            "accumulated": self.accumulated_reward,
            "info": info
        })
        return self.current_state, reward, done, info


class MovieRecommendationEnv(RLEnvironmentSimulation):
    """Escenario 3: Sistema de recomendación que aprende el perfil del usuario."""
    def __init__(self):
        states = ["Usuario_Nuevo", "Sesion_Exploracion", "Perfil_Detectado_SciFi", "Usuario_Satisfecho", "Abandono_Plataforma"]
        actions = ["Recomendar_Top10", "Recomendar_SciFi_Premium", "Recomendar_Comedia", "Recomendar_Documental"]
        super().__init__("Sistema de Recomendación de Películas", "Personalización algorítmica de catálogo multimedia", states, actions)

    def step(self, action: str) -> Tuple[str, float, bool, str]:
        self.step_count += 1
        done = False
        reward = 0.0
        info = ""

        if self.current_state == "Usuario_Nuevo":
            if action == "Recomendar_Top10":
                self.current_state = "Sesion_Exploracion"
                reward = 5.0
                info = "El usuario vio los trailers de la lista de tendencias."
            elif action == "Recomendar_SciFi_Premium":
                self.current_state = "Perfil_Detectado_SciFi"
                reward = 12.0
                info = "¡Clic inmediato! Al usuario le fascina el género de ciencia ficción."
            else:
                reward = -3.0
                info = "El usuario scrolleó sin mostrar interés."

        elif self.current_state == "Sesion_Exploracion":
            if action == "Recomendar_SciFi_Premium":
                self.current_state = "Perfil_Detectado_SciFi"
                reward = 15.0
                info = "El usuario comenzó a reproducir 'Interestelar'."
            elif action == "Recomendar_Documental":
                self.current_state = "Abandono_Plataforma"
                reward = -30.0
                done = True
                info = "Contenido aburrido. Usuario cerró la aplicación."
            else:
                reward = 2.0
                info = "Viendo una película ligera."

        elif self.current_state == "Perfil_Detectado_SciFi":
            if action == "Recomendar_SciFi_Premium":
                self.current_state = "Usuario_Satisfecho"
                reward = 60.0
                done = True
                info = "¡Maratón completada! Usuario otorgó 5 estrellas y renovó suscripción."
            elif action == "Recomendar_Comedia":
                reward = -5.0
                info = "Interrupción de la experiencia personalizada."
            else:
                reward = 1.0
                info = "Consumo estándar de contenido."

        self.accumulated_reward += reward
        self.trajectory.append({
            "step": self.step_count,
            "action": action,
            "next_state": self.current_state,
            "reward": reward,
            "accumulated": self.accumulated_reward,
            "info": info
        })
        return self.current_state, reward, done, info


def print_step_table(trajectory_item: Dict):
    step = trajectory_item['step']
    act = trajectory_item['action']
    state = trajectory_item['next_state']
    rew = trajectory_item['reward']
    acc = trajectory_item['accumulated']
    info = trajectory_item['info']
    rew_str = f"+{rew:.1f}" if rew >= 0 else f"{rew:.1f}"
    print(f"| Paso {step:02d} | Accion: {act:<24} | Nuevo Estado: {state:<24} | R: {rew_str:>6} | Acum: {acc:>7.1f} |")
    print(f"|         -> Retroalimentacion: {info}")


def run_simulation(env: RLEnvironmentSimulation, automated: bool = False):
    print("\n" + "=" * 80)
    print(f" SIMULACIÓN DE ESCENARIO: {env.name.upper()}")
    print(f" Descripción: {env.description}")
    print("=" * 80)

    state = env.reset()
    print(f"[*] Estado Inicial del Entorno: [{state}]")
    print("-" * 80)

    done = False
    step = 0
    max_steps = 10

    while not done and step < max_steps:
        step += 1
        print(f"\n--- Decision Point #{step} (Estado actual: '{env.current_state}') ---")
        if automated:
            action = random.choice(env.actions)
            print(f"[Agente Auto] Acción elegida probabilísticamente: {action}")
        else:
            print("Acciones disponibles:")
            for idx, a in enumerate(env.actions, 1):
                print(f"  [{idx}] {a}")
            print(f"  [A] Elegir automáticamente por política del agente")
            choice = input("Selecciona acción [1-4 o A] (Enter para Auto): ").strip().upper()
            if choice in ["A", ""]:
                action = random.choice(env.actions)
            elif choice.isdigit() and 1 <= int(choice) <= len(env.actions):
                action = env.actions[int(choice) - 1]
            else:
                action = random.choice(env.actions)
            print(f"-> Acción ejecutada: {action}")

        next_state, reward, done, info = env.step(action)
        print_step_table(env.trajectory[-1])

    print("-" * 80)
    print(f"[✔] Episodio Terminado. Pasos totales: {len(env.trajectory)} | Recompensa Final Acumulada: {env.accumulated_reward:.1f}")
    print("=" * 80)


def main():
    print("*" * 80)
    print(" TECNM / INSTITUTO TECNOLÓGICO SUPERIOR DE URUAPAN - MAESTRÍA EN IA")
    print(" ACTIVIDAD 25: ELEMENTOS DEL APRENDIZAJE POR REFUERZO (RL)")
    print(" Alumno: Juan Pablo Figueroa Moran | Matrícula: M26040059")
    print("*" * 80)

    environments = [
        AutonomousParkingEnv(),
        CoinCollectorGameEnv(),
        MovieRecommendationEnv()
    ]

    # Checar argumentos de línea de comandos para modo no interactivo
    if "--auto" in sys.argv or "--demo" in sys.argv or not sys.stdin.isatty():
        print("\n[+] Ejecutando simulación automática de los 3 escenarios...")
        for env in environments:
            run_simulation(env, automated=True)
            time.sleep(0.2)
        print("\n[✔] Los 3 escenarios han sido simulados exitosamente.")
        return

    while True:
        print("\n" + "=" * 50)
        print(" SELECCIÓN DE ESCENARIO DE APRENDIZAJE POR REFUERZO")
        print("=" * 50)
        print(" [1] Coche autónomo en estacionamiento")
        print(" [2] Videojuego de recolección de monedas")
        print(" [3] Sistema de recomendación de películas")
        print(" [4] Ejecutar demostración completa (los 3 escenarios)")
        print(" [0] Salir")
        print("-" * 50)

        opc = input("Ingresa tu opción [0-4]: ").strip()
        if opc == "1":
            run_simulation(environments[0], automated=False)
        elif opc == "2":
            run_simulation(environments[1], automated=False)
        elif opc == "3":
            run_simulation(environments[2], automated=False)
        elif opc == "4":
            for env in environments:
                run_simulation(env, automated=True)
        elif opc == "0":
            print("\nFinalizando simulación. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
