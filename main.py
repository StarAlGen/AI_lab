import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# Оптимизированная функция для вычисления конфликтов
def calculate_conflicts(state):
    n = len(state)
    row_conflicts = np.zeros(n)
    diag1_conflicts = np.zeros(2 * n - 1)
    diag2_conflicts = np.zeros(2 * n - 1)

    for i in range(n):
        row_conflicts[state[i]] += 1
        diag1_conflicts[i + state[i]] += 1
        diag2_conflicts[i - state[i] + n - 1] += 1

    conflicts = (np.sum(row_conflicts * (row_conflicts - 1)) +
                 np.sum(diag1_conflicts * (diag1_conflicts - 1)) +
                 np.sum(diag2_conflicts * (diag2_conflicts - 1))) // 2
    return int(conflicts)

# Алгоритм отжига
def simulated_annealing_n_queens(n, max_temp, min_temp, alpha, steps_per_temp):
    state = np.random.permutation(n)
    best_state = state.copy()
    best_eval = calculate_conflicts(best_state)
    
    current_state = state.copy()
    current_eval = best_eval
    
    temp = max_temp
    accepted_bad_solutions = 0
    
    # Хранение данных для построения графиков
    temperature_history = []
    best_eval_history = []
    bad_solutions_history = []
    
    while temp > min_temp:
        for step in range(steps_per_temp):
            candidate_state = current_state.copy()
            a, b = np.random.randint(0, n, size=2)
            candidate_state[a], candidate_state[b] = candidate_state[b], candidate_state[a]
            candidate_eval = calculate_conflicts(candidate_state)

            if candidate_eval < best_eval:
                best_state, best_eval = candidate_state.copy(), candidate_eval
            
            diff = candidate_eval - current_eval
            metropolis = np.exp(-diff / temp)

            if diff < 0 or np.random.rand() < metropolis:
                if diff > 0:
                    accepted_bad_solutions += 1
                current_state, current_eval = candidate_state.copy(), candidate_eval

        # Сохраняем данные для графиков
        temperature_history.append(temp)
        best_eval_history.append(best_eval)
        bad_solutions_history.append(accepted_bad_solutions)
        
        temp *= alpha
    
    return best_state, best_eval, temperature_history, best_eval_history, bad_solutions_history

# Визуализация шахматной доски с ферзями
def visualize_chessboard(best_state, best_eval):
    fig, ax = plt.subplots(figsize=(6, 6))
    n = len(best_state)
    
    # Изменение размера ферзей в зависимости от числа ферзей на доске
    queen_font_size = max(10, 600 // n)

    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                ax.add_patch(plt.Rectangle((i, j), 1, 1, fill=True, color='lightgray'))
            else:
                ax.add_patch(plt.Rectangle((i, j), 1, 1, fill=True, color='gray'))

    for i in range(n):
        ax.text(i + 0.5, best_state[i] + 0.5, '♕', ha='center', va='center', fontsize=queen_font_size, color='green')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.invert_yaxis()

    ax.set_title(f"Best Conflicts: {best_eval}")
    plt.show()

# Визуализация графиков
def visualize_plots(temp_history, best_eval_history, bad_solutions_history):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))

    # График температуры
    ax1.plot(temp_history, label="Temperature", color='blue')
    ax1.set_ylabel("Temperature", color='blue')
    ax1.set_xlabel("Iterations")
    ax1.legend()

    # График лучшего решения (конфликтов)
    ax2.plot(best_eval_history, label="Best Evaluation", color='green')
    ax2.set_ylabel("Best Conflicts", color='green')
    ax2.set_xlabel("Iterations")
    ax2.legend()

    # График принятых плохих решений
    ax3.plot(bad_solutions_history, label="Accepted Bad Solutions", color='red')
    ax3.set_ylabel("Accepted Bad Solutions", color='red')
    ax3.set_xlabel("Iterations")
    ax3.legend()

    # Настройка отступов между графиками, чтобы избежать перекрытий
    plt.subplots_adjust(hspace=0.4)
    plt.tight_layout()
    plt.show()

# Обработка запуска алгоритма
def run_n_queens():
    n = int(n_var.get())
    max_temp = float(max_temp_var.get())
    min_temp = float(min_temp_var.get())
    alpha = float(alpha_var.get())
    steps_per_temp = int(steps_per_temp_var.get())
    
    best_state, best_eval, temp_history, best_eval_history, bad_solutions_history = simulated_annealing_n_queens(
        n, max_temp, min_temp, alpha, steps_per_temp
    )

    # Визуализируем доску
    visualize_chessboard(best_state, best_eval)

    # Визуализируем графики
    visualize_plots(temp_history, best_eval_history, bad_solutions_history)

if __name__== '__main__':
    # Инициализация графического интерфейса
    root = tk.Tk()
    root.title("Simulated Annealing for N-Queens")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Поля для ввода параметров
    ttk.Label(frame, text="Number of Queens:").grid(row=0, column=0)
    n_var = tk.StringVar(value="8")
    n_entry = ttk.Entry(frame, textvariable=n_var)
    n_entry.grid(row=0, column=1)

    ttk.Label(frame, text="Max Temperature:").grid(row=1, column=0)
    max_temp_var = tk.StringVar(value="1000")
    max_temp_entry = ttk.Entry(frame, textvariable=max_temp_var)
    max_temp_entry.grid(row=1, column=1)

    ttk.Label(frame, text="Min Temperature:").grid(row=2, column=0)
    min_temp_var = tk.StringVar(value="0.01")
    min_temp_entry = ttk.Entry(frame, textvariable=min_temp_var)
    min_temp_entry.grid(row=2, column=1)

    ttk.Label(frame, text="Alpha (Temperature Decay):").grid(row=3, column=0)
    alpha_var = tk.StringVar(value="0.95")
    alpha_entry = ttk.Entry(frame, textvariable=alpha_var)
    alpha_entry.grid(row=3, column=1)

    ttk.Label(frame, text="Steps per Temp:").grid(row=4, column=0)
    steps_per_temp_var = tk.StringVar(value="100")
    steps_per_temp_entry = ttk.Entry(frame, textvariable=steps_per_temp_var)
    steps_per_temp_entry.grid(row=4, column=1)

    # Кнопка для запуска алгоритма
    start_button = ttk.Button(frame, text="Start", command=run_n_queens)
    start_button.grid(row=5, column=0, columnspan=2)

    # Запуск GUI
    root.mainloop()