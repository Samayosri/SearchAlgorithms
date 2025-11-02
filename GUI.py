"""
8-Puzzle Solver GUI - Nature/Game Theme (CLEAN VERSION)
Improved DFS/IDFS handling, removed subtitle and solution field
"""

import sys
import time
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                             QTabWidget, QComboBox, QTextEdit, 
                             QGroupBox, QMessageBox, QSlider, QLineEdit, QFrame,
                             QScrollArea)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont

# Import algorithm modules
from BFS import BFS, is_solvable as bfs_solvable
from DFS import DfS, checkinstances as dfs_solvable, calculate_solution_depth
from IDFS import IDFS, checkinstances as idfs_solvable
from A_star import A_Star, manhattan_distance, euclidean_distance, is_solvable as astar_solvable


class WoodenTile(QPushButton):
    """Game-style wooden tile with nature theme"""
    
    COLORS = [
        ('#2c3e50', '#1a252f'),  # Dark for empty (0)
        ('#e74c3c', '#c0392b'),  # Red (1)
        ('#9b59b6', '#8e44ad'),  # Purple (2)
        ('#3498db', '#2980b9'),  # Blue (3)
        ('#f39c12', '#e67e22'),  # Orange (4)
        ('#e91e63', '#c2185b'),  # Pink (5)
        ('#1abc9c', '#16a085'),  # Teal (6)
        ('#f1c40f', '#f39c12'),  # Yellow (7)
        ('#2ecc71', '#27ae60'),  # Green (8)
    ]
    
    def __init__(self, value=0):
        super().__init__()
        self.value = value
        self.setFixedSize(90, 90)
        self.setFont(QFont("Arial Black", 32, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor if value != 0 else Qt.ArrowCursor)
        self.update_style()
    
    def set_value(self, value):
        """Update tile value and appearance"""
        self.value = value
        self.update_style()
    
    def update_style(self):
        """Apply wooden game-style appearance"""
        if self.value == 0:
            self.setText("")
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3a3a3a, stop:1 #1a1a1a);
                    border: 4px solid #5a4a3a;
                    border-radius: 12px;
                }
            """)
        else:
            self.setText(str(self.value))
            color1, color2 = self.COLORS[self.value]
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {color1}, stop:0.5 {color2}, stop:1 {color1});
                    color: white;
                    border: 5px solid #8B6F47;
                    border-radius: 12px;
                    font-weight: bold;
                    text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8);
                }}
                QPushButton:hover {{
                    border: 5px solid #D4AF37;
                }}
            """)


class WoodenPanel(QFrame):
    """Wooden panel background"""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D2691E, stop:0.5 #8B4513, stop:1 #A0522D);
                border: 6px solid #5a3a1a;
                border-radius: 20px;
            }
        """)


class GamePuzzleBoard(QWidget):
    """Game-style puzzle board"""
    
    def __init__(self):
        super().__init__()
        self.current_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.tiles = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the puzzle board UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Wooden panel background
        panel = WoodenPanel()
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(20, 20, 20, 20)
        
        # Grid for tiles
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Create 9 tiles in a 3x3 grid
        for i in range(9):
            tile = WoodenTile(i)
            self.tiles.append(tile)
            row, col = divmod(i, 3)
            grid.addWidget(tile, row, col)
        
        panel_layout.addLayout(grid)
        panel.setLayout(panel_layout)
        
        main_layout.addWidget(panel)
        self.setLayout(main_layout)
        
        self.update_display()
    
    def update_display(self):
        """Update the visual display based on current state"""
        for i, value in enumerate(self.current_state):
            self.tiles[i].set_value(value)
    
    def set_state(self, state):
        """Set the board to a specific state"""
        self.current_state = state.copy() if isinstance(state, list) else list(state)
        self.update_display()


class NatureButton(QPushButton):
    """Nature-themed game button"""
    
    def __init__(self, text, color='green'):
        super().__init__(text)
        self.color = color
        self.setMinimumHeight(45)
        self.setFont(QFont("Arial Black", 11, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()
    
    def update_style(self):
        """Apply nature game-style button styling"""
        colors = {
            'green': ('#7CB342', '#558B2F'),
            'blue': ('#42A5F5', '#1976D2'),
            'orange': ('#FFA726', '#F57C00'),
            'red': ('#EF5350', '#C62828'),
            'purple': ('#AB47BC', '#7B1FA2'),
            'pink': ('#EC407A', '#C2185B'),
        }
        
        color1, color2 = colors.get(self.color, colors['green'])
        
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color1}, stop:0.5 {color2}, stop:1 {color1});
                color: white;
                border: 5px solid #8B6F47;
                border-radius: 15px;
                padding: 8px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            }}
            QPushButton:hover {{
                border: 5px solid #D4AF37;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color2}, stop:0.5 {color1}, stop:1 {color2});
            }}
            QPushButton:pressed {{
                background: {color2};
            }}
            QPushButton:disabled {{
                background: #757575;
                color: #BDBDBD;
                border: 5px solid #5a5a5a;
            }}
        """)


class CompactInputGrid(QWidget):
    """Compact 3x3 input grid for puzzle state"""
    
    def __init__(self):
        super().__init__()
        self.inputs = []
        self.init_ui()
    
    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(5)
        
        for i in range(9):
            input_field = QLineEdit()
            input_field.setFixedSize(40, 40)
            input_field.setAlignment(Qt.AlignCenter)
            input_field.setFont(QFont("Arial Black", 13, QFont.Bold))
            input_field.setText(str(i))
            input_field.setMaxLength(1)
            input_field.setStyleSheet("""
                QLineEdit {
                    background: #FFF8DC;
                    border: 3px solid #8B6F47;
                    border-radius: 8px;
                    color: #3E2723;
                }
                QLineEdit:focus {
                    border: 3px solid #D4AF37;
                }
            """)
            self.inputs.append(input_field)
            row, col = divmod(i, 3)
            layout.addWidget(input_field, row, col)
        
        self.setLayout(layout)
    
    def get_state(self):
        """Get current state from inputs"""
        return [int(inp.text()) if inp.text().isdigit() else 0 for inp in self.inputs]
    
    def set_state(self, state):
        """Set input values"""
        for i, value in enumerate(state):
            self.inputs[i].setText(str(value))


class StatsPanel(QFrame):
    """Statistics display panel with wooden theme"""
    
    def __init__(self):
        super().__init__()
        self.stats_labels = {}
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8B4513, stop:0.5 #A0522D, stop:1 #8B4513);
                border: 5px solid #5a3a1a;
                border-radius: 15px;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(6)
        
        # Title
        title = QLabel("📊 STATISTICS")
        title.setFont(QFont("Arial Black", 13, QFont.Bold))
        title.setStyleSheet("color: #FFD700; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Stats items
        stat_items = [
            ('path', '🎯 Path to Goal'),
            ('cost', '💰 Cost of Path'),
            ('expanded', '🔍 Nodes Expanded'),
            ('depth', '📏 Search Depth'),
            ('time', '⏱️ Running Time')
        ]
        
        for key, label in stat_items:
            stat_label = QLabel(f"{label}: -")
            stat_label.setFont(QFont("Arial", 10, QFont.Bold))
            stat_label.setStyleSheet("""
                color: #FFF8DC; 
                padding: 4px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 5px;
            """)
            self.stats_labels[key] = stat_label
            layout.addWidget(stat_label)
        
        self.setLayout(layout)
    
    def update_stats(self, stats):
        """Update statistics display"""
        self.stats_labels['path'].setText(f"🎯 Path to Goal: {stats.get('cost', '-')} moves")
        self.stats_labels['cost'].setText(f"💰 Cost of Path: {stats.get('cost', '-')}")
        self.stats_labels['expanded'].setText(f"🔍 Nodes Expanded: {stats.get('expanded', '-')}")
        self.stats_labels['depth'].setText(f"📏 Search Depth: {stats.get('depth', '-')}")
        self.stats_labels['time'].setText(f"⏱️ Running Time: {stats.get('time', '-'):.4f}s")
    
    def clear_stats(self):
        """Clear all statistics"""
        for key in self.stats_labels:
            text = self.stats_labels[key].text().split(':')[0]
            self.stats_labels[key].setText(f"{text}: -")


class AlgorithmTab(QWidget):
    """Algorithm tab with nature theme"""
    
    def __init__(self, algorithm_name, color='green'):
        super().__init__()
        self.algorithm_name = algorithm_name
        self.color = color
        self.puzzle_board = GamePuzzleBoard()
        self.stats_panel = StatsPanel()
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_step)
        self.solution_path = []
        self.current_step = 0
        self.is_animating = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the tab UI"""
        # Set background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4A148C, stop:0.5 #6A1B9A, stop:1 #4A148C);
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Left panel: Game board
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)
        
        # Title
        title = QLabel(f"🎮 {self.algorithm_name}")
        title.setFont(QFont("Arial Black", 16, QFont.Bold))
        title.setStyleSheet("color: #FFD700; text-shadow: 3px 3px 6px rgba(0,0,0,0.8);")
        title.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(title)
        
        # Puzzle board
        left_panel.addWidget(self.puzzle_board, alignment=Qt.AlignCenter)
        left_panel.addStretch()
        
        # Right panel with scroll area
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        right_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        right_widget = QWidget()
        right_panel = QVBoxLayout()
        right_panel.setSpacing(10)
        right_panel.setContentsMargins(5, 5, 5, 5)
        
        # Input section
        input_frame = WoodenPanel()
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(12, 12, 12, 12)
        
        input_label = QLabel("⚙️ INITIAL STATE")
        input_label.setFont(QFont("Arial Black", 10, QFont.Bold))
        input_label.setStyleSheet("color: #FFD700;")
        input_label.setAlignment(Qt.AlignCenter)
        input_layout.addWidget(input_label)
        
        self.input_grid = CompactInputGrid()
        input_layout.addWidget(self.input_grid, alignment=Qt.AlignCenter)
        
        input_btn_layout = QHBoxLayout()
        load_btn = NatureButton("LOAD", 'blue')
        load_btn.clicked.connect(self.load_state)
        random_btn = NatureButton("RANDOM", 'purple')
        random_btn.clicked.connect(self.randomize_state)
        input_btn_layout.addWidget(load_btn)
        input_btn_layout.addWidget(random_btn)
        input_layout.addLayout(input_btn_layout)
        
        input_frame.setLayout(input_layout)
        right_panel.addWidget(input_frame)
        
        # Control buttons
        self.run_btn = NatureButton("▶ START", 'green')
        self.run_btn.clicked.connect(self.run_algorithm)
        right_panel.addWidget(self.run_btn)
        
        control_layout = QHBoxLayout()
        self.step_btn = NatureButton("⏯ STEP", 'orange')
        self.step_btn.setEnabled(False)
        self.step_btn.clicked.connect(self.step_forward)
        
        self.reset_btn = NatureButton("↻ RESET", 'red')
        self.reset_btn.clicked.connect(self.reset_board)
        
        control_layout.addWidget(self.step_btn)
        control_layout.addWidget(self.reset_btn)
        right_panel.addLayout(control_layout)
        
        # Speed control
        speed_frame = WoodenPanel()
        speed_layout = QVBoxLayout()
        speed_layout.setContentsMargins(12, 12, 12, 12)
        
        speed_label = QLabel("⚡ ANIMATION SPEED")
        speed_label.setFont(QFont("Arial Black", 10, QFont.Bold))
        speed_label.setStyleSheet("color: #FFD700;")
        speed_label.setAlignment(Qt.AlignCenter)
        speed_layout.addWidget(speed_label)
        
        slider_container = QHBoxLayout()
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(20)
        self.speed_slider.setValue(5)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 10px;
                background: #5a3a1a;
                border-radius: 5px;
                border: 2px solid #3a2a1a;
            }
            QSlider::handle:horizontal {
                background: #FFD700;
                width: 22px;
                height: 22px;
                margin: -6px 0;
                border-radius: 11px;
                border: 3px solid #8B6F47;
            }
            QSlider::handle:horizontal:hover {
                background: #FFA500;
            }
        """)
        
        self.speed_value_label = QLabel("5")
        self.speed_value_label.setFont(QFont("Arial Black", 11, QFont.Bold))
        self.speed_value_label.setStyleSheet("color: #FFD700; min-width: 25px;")
        self.speed_value_label.setAlignment(Qt.AlignCenter)
        
        self.speed_slider.valueChanged.connect(lambda v: self.speed_value_label.setText(str(v)))
        
        slider_container.addWidget(self.speed_slider)
        slider_container.addWidget(self.speed_value_label)
        
        speed_layout.addLayout(slider_container)
        
        speed_frame.setLayout(speed_layout)
        right_panel.addWidget(speed_frame)
        
        # Stats panel
        right_panel.addWidget(self.stats_panel)
        
        # Add stretch at the end
        right_panel.addStretch()
        
        right_widget.setLayout(right_panel)
        right_scroll.setWidget(right_widget)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 2)
        main_layout.addWidget(right_scroll, 1)
        
        self.setLayout(main_layout)
    
    def load_state(self):
        """Load state from input fields"""
        try:
            state = self.input_grid.get_state()
            
            if sorted(state) != list(range(9)):
                raise ValueError("State must contain all values from 0 to 8")
            
            self.puzzle_board.set_state(state)
            
            # Update parent window's shared state if available
            parent_window = self.window()
            if hasattr(parent_window, 'shared_state'):
                parent_window.shared_state = state
            
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
    
    def randomize_state(self):
        """Generate a random solvable state"""
        while True:
            state = list(range(9))
            random.shuffle(state)
            if self.check_solvable(state):
                break
        
        self.input_grid.set_state(state)
        self.puzzle_board.set_state(state)
        
        # Update parent window's shared state if available
        parent_window = self.window()
        if hasattr(parent_window, 'shared_state'):
            parent_window.shared_state = state
    
    def check_solvable(self, state):
        """Check if a state is solvable"""
        return True
    
    def reset_board(self):
        """Reset the board to the initial state from input grid"""
        initial_state = self.input_grid.get_state()
        self.puzzle_board.set_state(initial_state)
        self.solution_path = []
        self.current_step = 0
        self.animation_timer.stop()
        self.is_animating = False
        self.step_btn.setEnabled(False)
        self.clear_output()
    
    def run_algorithm(self):
        """Run the algorithm (to be overridden)"""
        pass
    
    def animate_solution(self, path):
        """Start animating the solution path"""
        self.solution_path = path
        self.current_step = 0
        self.step_btn.setEnabled(True)
        self.is_animating = True
        
        speed = self.speed_slider.value()
        delay = int(1000 / speed)
        self.animation_timer.start(delay)
    
    def animate_step(self):
        """Animate one step of the solution"""
        if self.current_step < len(self.solution_path):
            state = self.solution_path[self.current_step]
            self.puzzle_board.set_state(state)
            self.current_step += 1
        else:
            self.animation_timer.stop()
            self.is_animating = False
            self.step_btn.setEnabled(False)
    
    def step_forward(self):
        """Manually step forward one move"""
        self.animation_timer.stop()
        if self.current_step < len(self.solution_path):
            state = self.solution_path[self.current_step]
            self.puzzle_board.set_state(state)
            self.current_step += 1
            if self.current_step >= len(self.solution_path):
                self.step_btn.setEnabled(False)
    
    def display_stats(self, stats):
        """Display algorithm statistics"""
        self.stats_panel.update_stats(stats)
    
    def clear_output(self):
        """Clear all output displays"""
        self.stats_panel.clear_stats()


class BFSTab(AlgorithmTab):
    def __init__(self):
        super().__init__("Breadth-First Search", 'blue')
    
    def check_solvable(self, state):
        return bfs_solvable(state)
    
    def run_algorithm(self):
        start_state = self.puzzle_board.current_state.copy()
        
        if not self.check_solvable(start_state):
            QMessageBox.warning(self, "Unsolvable", "This puzzle is unsolvable!")
            return
        
        # Store the initial state in input grid AND shared state
        self.input_grid.set_state(start_state)
        parent_window = self.window()
        if hasattr(parent_window, 'shared_state'):
            parent_window.shared_state = start_state
        
        self.clear_output()
        self.run_btn.setEnabled(False)
        start_time = time.time()
        
        try:
            parent, expanded, cost, depth = BFS(start_state)
            end_time = time.time()
            
            goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            path = []
            current = goal
            while current is not None:
                path.append(current)
                current = parent[tuple(current)]
            path.reverse()
            
            stats = {'cost': cost, 'expanded': expanded, 'depth': depth, 'time': end_time - start_time}
            self.display_stats(stats)
            self.animate_solution(path)
            
            print("\n" + "="*50)
            print("BFS Algorithm Results")
            print("="*50)
            print(f"Path to Goal: {len(path) - 1} moves")
            print(f"Cost of Path: {cost}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Search Depth: {depth}")
            print(f"Running Time: {end_time - start_time:.4f} seconds")
            print("="*50 + "\n")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
        finally:
            self.run_btn.setEnabled(True)


class DFSTab(AlgorithmTab):
    def __init__(self):
        super().__init__("Depth-First Search", 'purple')
    
    def check_solvable(self, state):
        return dfs_solvable(state)
    
    def run_algorithm(self):
        start_state = self.puzzle_board.current_state.copy()
        
        if not self.check_solvable(start_state):
            QMessageBox.warning(self, "Unsolvable", "This puzzle is unsolvable!")
            return
        
        # Store the initial state in input grid AND shared state
        self.input_grid.set_state(start_state)
        parent_window = self.window()
        if hasattr(parent_window, 'shared_state'):
            parent_window.shared_state = start_state
        
        self.clear_output()
        self.run_btn.setEnabled(False)
        start_time = time.time()
        
        try:
            goal, parent, expanded, max_depth = DfS(start_state)
            end_time = time.time()
            
            if goal is None:
                QMessageBox.warning(self, "No Solution", "No solution found!")
                self.run_btn.setEnabled(True)
                return
            
            # Build path from parent dictionary
            path = []
            key = tuple(goal)
            while key in parent:
                path.append(list(key))
                key = parent[key]
            path.append(list(key))  # Add start state
            path.reverse()
            
            solution_depth = calculate_solution_depth(goal, parent)
            
            stats = {'cost': solution_depth, 'expanded': expanded, 'depth': max_depth, 'time': end_time - start_time}
            self.display_stats(stats)
            self.animate_solution(path)
            
            print("\n" + "="*50)
            print("DFS Algorithm Results")
            print("="*50)
            print(f"Path to Goal: {len(path) - 1} moves")
            print(f"Cost of Path: {solution_depth}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Max Search Depth: {max_depth}")
            print(f"Running Time: {end_time - start_time:.4f} seconds")
            print("="*50 + "\n")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
        finally:
            self.run_btn.setEnabled(True)


class IDFSTab(AlgorithmTab):
    def __init__(self):
        super().__init__("Iterative Deepening DFS", 'orange')
    
    def check_solvable(self, state):
        return idfs_solvable(state)
    
    def run_algorithm(self):
        start_state = self.puzzle_board.current_state.copy()
        
        if not self.check_solvable(start_state):
            QMessageBox.warning(self, "Unsolvable", "This puzzle is unsolvable!")
            return
        
        # Store the initial state in input grid AND shared state
        self.input_grid.set_state(start_state)
        parent_window = self.window()
        if hasattr(parent_window, 'shared_state'):
            parent_window.shared_state = start_state
        
        self.clear_output()
        self.run_btn.setEnabled(False)
        start_time = time.time()
        
        try:
            import IDFS as idfs_module
            result = idfs_module.IDFS(start_state)
            end_time = time.time()
            
            if result is None or result[0] is None:
                QMessageBox.warning(self, "No Solution", "No solution found!")
                self.run_btn.setEnabled(True)
                return
            
            # result is (path, depth)
            path_tuples, solution_depth = result
            path = [list(state) for state in path_tuples]
            
            stats = {
                'cost': len(path) - 1, 
                'expanded': idfs_module.total_expanded, 
                'depth': solution_depth, 
                'time': end_time - start_time
            }
            self.display_stats(stats)
            self.animate_solution(path)
            
            print("\n" + "="*50)
            print("Iterative Deepening DFS Algorithm Results")
            print("="*50)
            print(f"Path to Goal: {len(path) - 1} moves")
            print(f"Cost of Path: {len(path) - 1}")
            print(f"Nodes Expanded: {idfs_module.total_expanded}")
            print(f"Search Depth: {solution_depth}")
            print(f"Running Time: {end_time - start_time:.4f} seconds")
            print("="*50 + "\n")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.run_btn.setEnabled(True)


class AStarTab(AlgorithmTab):
    def __init__(self):
        super().__init__("A* Search", 'green')
        self.heuristic_combo = None
        self.add_heuristic_selector()
    
    def add_heuristic_selector(self):
        """Add heuristic selection combo box"""
        # Find the right panel layout
        right_scroll = self.layout().itemAt(1).widget()
        if isinstance(right_scroll, QScrollArea):
            right_widget = right_scroll.widget()
            right_layout = right_widget.layout()
            
            # Create heuristic frame
            heuristic_frame = WoodenPanel()
            h_layout = QVBoxLayout()
            h_layout.setContentsMargins(12, 12, 12, 12)
            
            h_label = QLabel("🎯 HEURISTIC")
            h_label.setFont(QFont("Arial Black", 10, QFont.Bold))
            h_label.setStyleSheet("color: #FFD700;")
            h_label.setAlignment(Qt.AlignCenter)
            h_layout.addWidget(h_label)
            
            self.heuristic_combo = QComboBox()
            self.heuristic_combo.addItems(["Manhattan", "Euclidean"])
            self.heuristic_combo.setFont(QFont("Arial", 9, QFont.Bold))
            self.heuristic_combo.setStyleSheet("""
                QComboBox {
                    background: #FFF8DC;
                    border: 3px solid #8B6F47;
                    border-radius: 8px;
                    padding: 6px;
                    color: #3E2723;
                }
                QComboBox:hover {
                    border: 3px solid #D4AF37;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid #8B6F47;
                    margin-right: 6px;
                }
                QComboBox QAbstractItemView {
                    background: #FFF8DC;
                    border: 3px solid #8B6F47;
                    selection-background-color: #D4AF37;
                    selection-color: #3E2723;
                }
            """)
            h_layout.addWidget(self.heuristic_combo)
            
            heuristic_frame.setLayout(h_layout)
            
            # Insert after input frame (position 1)
            right_layout.insertWidget(1, heuristic_frame)
    
    def check_solvable(self, state):
        return astar_solvable(state)
    
    def run_algorithm(self):
        start_state = self.puzzle_board.current_state.copy()
        
        if not self.check_solvable(start_state):
            QMessageBox.warning(self, "Unsolvable", "This puzzle is unsolvable!")
            return
        
        heuristic = manhattan_distance if self.heuristic_combo.currentIndex() == 0 else euclidean_distance
        heuristic_name = "Manhattan" if self.heuristic_combo.currentIndex() == 0 else "Euclidean"
        
        # Store the initial state in input grid AND shared state
        self.input_grid.set_state(start_state)
        parent_window = self.window()
        if hasattr(parent_window, 'shared_state'):
            parent_window.shared_state = start_state
        
        self.clear_output()
        self.run_btn.setEnabled(False)
        start_time = time.time()
        
        try:
            parent, expanded, cost, depth = A_Star(start_state, heuristic)
            end_time = time.time()
            
            goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            path = []
            current = goal
            while current is not None:
                path.append(current)
                current = parent[tuple(current)]
            path.reverse()
            
            stats = {'cost': cost, 'expanded': expanded, 'depth': depth, 'time': end_time - start_time}
            self.display_stats(stats)
            self.animate_solution(path)
            
            print("\n" + "="*50)
            print(f"A* Algorithm Results ({heuristic_name} Heuristic)")
            print("="*50)
            print(f"Path to Goal: {len(path) - 1} moves")
            print(f"Cost of Path: {cost}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Search Depth: {depth}")
            print(f"Running Time: {end_time - start_time:.4f} seconds")
            print("="*50 + "\n")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
        finally:
            self.run_btn.setEnabled(True)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.shared_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Shared state across all tabs
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main window UI"""
        self.setWindowTitle("🎮 8-PUZZLE GAME SOLVER")
        self.setGeometry(50, 50, 1400, 850)
        
        # Nature-themed background
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a237e, stop:0.5 #311b92, stop:1 #1a237e);
            }
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8B4513, stop:0.5 #A0522D, stop:1 #8B4513);
                color: #FFD700;
                padding: 12px 25px;
                margin: 2px;
                border: 4px solid #5a3a1a;
                border-radius: 12px 12px 0 0;
                font-size: 12px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D2691E, stop:0.5 #CD853F, stop:1 #D2691E);
                color: white;
                border: 4px solid #D4AF37;
            }
            QTabBar::tab:hover {
                border: 4px solid #D4AF37;
            }
            QScrollBar:vertical {
                background: #5a3a1a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #D4AF37;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #FFD700;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Header with wooden panel (REMOVED SUBTITLE)
        header = WoodenPanel()
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("🎮 8-PUZZLE GAME SOLVER")
        title.setFont(QFont("Arial Black", 24, QFont.Bold))
        title.setStyleSheet("""
            color: #FFD700; 
            text-shadow: 4px 4px 8px rgba(0,0,0,0.8);
        """)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle REMOVED - no longer displayed
        
        header.setLayout(header_layout)
        layout.addWidget(header)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial Black", 10))
        
        self.bfs_tab = BFSTab()
        self.dfs_tab = DFSTab()
        self.idfs_tab = IDFSTab()
        self.astar_tab = AStarTab()
        
        # Connect tab change signal to sync states
        self.tabs.currentChanged.connect(self.sync_tab_states)
        
        self.tabs.addTab(self.bfs_tab, "🔵 BFS")
        self.tabs.addTab(self.dfs_tab, "🟣 DFS")
        self.tabs.addTab(self.idfs_tab, "🟠 IDFS")
        self.tabs.addTab(self.astar_tab, "🟢 A*")
        
        # Initialize all tabs with shared state
        for tab in [self.bfs_tab, self.dfs_tab, self.idfs_tab, self.astar_tab]:
            tab.input_grid.set_state(self.shared_state)
            tab.puzzle_board.set_state(self.shared_state)
        
        layout.addWidget(self.tabs)
        

        
        central_widget.setLayout(layout)
    
    def sync_tab_states(self, index):
        """Sync the input state across all tabs when switching"""
        # Get the tab we're switching TO
        new_tab = self.tabs.widget(index)
        
        # Set the new tab's input grid to the shared state
        new_tab.input_grid.set_state(self.shared_state)
        
        # Also set the puzzle board to the shared state
        new_tab.puzzle_board.set_state(self.shared_state)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application-wide font
    app.setFont(QFont("Arial", 10))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()