# Actividad 25: Elementos del Aprendizaje por Refuerzo (RL)

**Tecnológico Nacional de México**  
**Instituto Tecnológico Superior de Uruapan**  
**División de Estudios de Posgrado e Investigación**  
**Maestría en Inteligencia Artificial**  

* **Asignatura:** Aprendizaje Automático  
* **Catedrático:** Dr. Roberto Loaeza Valerio  
* **Alumno:** Juan Pablo Figueroa Moran  
* **Matrícula:** M26040059  
* **Repositorio:** [https://github.com/juanpablofm92/Actividad25.git](https://github.com/juanpablofm92/Actividad25.git)  

---

## 📌 1. Descripción del Proyecto

Este proyecto implementa una simulación interactiva y estocástica de los **Elementos Fundamentales del Aprendizaje por Refuerzo (Reinforcement Learning - RL)** en tres escenarios aplicados del mundo real:

1. 🚗 **Coche Autónomo en Maniobra de Estacionamiento:** Toma de decisiones de control de velocidad, giro y reversa evitando colisiones.
2. 🎮 **Videojuego de Recolección de Monedas:** Navegación en laberinto recolectando recompensas y eludiendo peligros/trampas.
3. 🎬 **Sistema de Recomendación de Películas:** Personalización de catálogo multimedia según retroalimentación implícita y retención del usuario.

El simulador despliega la trayectoria temporal de estados, las acciones seleccionadas y la acumulación de la señal de recompensa escalar $G_t = \sum \gamma^k R_{t+k+1}$.

---

## 🧠 2. Los 7 Elementos Clave del Aprendizaje por Refuerzo

| # | Elemento | Notación | Descripción Teórica y Rol en el Sistema |
|---|---|---|---|
| **1** | **Agente (Agent)** | Agente | Entidad tomadora de decisiones con capacidad de percibir y actuar sobre el medio circundante. |
| **2** | **Entorno (Environment)** | Entorno | Todo lo exterior al agente; mundo dinámico que responde a las acciones transicionando de estado. |
| **3** | **Estado (State)** | $S_t \in \mathcal{S}$ | Representación cuantitativa de la situación actual del entorno percibida en el tiempo $t$. |
| **4** | **Acción (Action)** | $A_t \in \mathcal{A}(S_t)$ | Conjunto de decisiones u operaciones motoras/lógicas disponibles que el agente puede emitir. |
| **5** | **Recompensa (Reward)** | $R_{t+1} \in \mathbb{R}$ | Señal escalar numérica inmediata de retroalimentación que califica el éxito o costo de una acción. |
| **6** | **Política (Policy)** | $\pi(a\|s)$ | Estrategia de mapeo o distribución de probabilidad entre estados observados y acciones a tomar. |
| **7** | **Función de Valor (Value Function)** | $V(s)$ o $Q(s,a)$ | Estimación del retorno acumulado esperado a largo plazo partiendo de un estado o par estado-acción. |

---

## 📁 3. Estructura del Repositorio

```
Actividad25/
├── README.md
├── requirements.txt
├── .gitignore
└── src/
    └── main.py
```

---

## 🚀 4. Guía de Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/juanpablofm92/Actividad25.git
cd Actividad25

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Modo Interactivo (menú por consola)
python src/main.py

# 4. Modo Demostración Automática (ejecuta los 3 escenarios consecutivamente)
python src/main.py --auto
```
