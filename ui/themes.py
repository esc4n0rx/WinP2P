THEMES = {
    'Windows95': """
        QWidget { 
            background: #C0C0C0; 
            font-family: 'Tahoma'; 
            font-size: 10pt;
        }
        QPushButton { 
            border: 2px outset #A0A0A0; 
            padding: 4px; 
            background-color: #C0C0C0;
        }
        QPushButton:hover {
            background-color: #D0D0D0;
        }
        QPushButton:pressed { 
            border-style: inset; 
            background-color: #B0B0B0;
        }
        QTextEdit, QLineEdit { 
            background: white; 
            border: 1px inset #A0A0A0;
        }
        QLabel { 
            background: transparent; 
        }
        QListWidget {
            background: white;
            border: 1px inset #A0A0A0;
        }
        QScrollArea {
            border: 1px inset #A0A0A0;
            background: white;
        }
    """,
    
    'XP': """
        QWidget { 
            background: #ECE9D8; 
            font-family: 'Verdana'; 
            font-size: 10pt;
        }
        QPushButton { 
            border: 2px outset #4080D0; 
            border-radius: 3px;
            padding: 4px; 
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #F0F6FD, stop: 1 #C2DFFF);
        }
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #F8FCFF, stop: 1 #D0E8FF);
        }
        QPushButton:pressed { 
            border-style: inset; 
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #C0D0E5, stop: 1 #A0C0E0);
        }
        QTextEdit, QLineEdit { 
            background: white; 
            border: 1px solid #7A9FBF;
            border-radius: 2px;
        }
        QLabel { 
            background: transparent; 
        }
        QListWidget {
            background: white;
            border: 1px solid #7A9FBF;
            border-radius: 2px;
        }
        QScrollArea {
            border: 1px solid #7A9FBF;
            border-radius: 2px;
            background: white;
        }
    """,
    
    'Modern': """
        QWidget { 
            background: #F5F5F5; 
            font-family: 'Segoe UI', 'Arial'; 
            font-size: 10pt;
        }
        QPushButton { 
            border: none; 
            border-radius: 4px;
            padding: 8px 16px; 
            background-color: #2196F3;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1E88E5;
        }
        QPushButton:pressed { 
            background-color: #1976D2;
        }
        QTextEdit, QLineEdit { 
            background: white; 
            border: 1px solid #DDDDDD;
            border-radius: 4px;
            padding: 4px;
        }
        QLineEdit:focus {
            border: 1px solid #2196F3;
        }
        QLabel { 
            background: transparent; 
        }
        QListWidget {
            background: white;
            border: 1px solid #DDDDDD;
            border-radius: 4px;
        }
        QScrollArea {
            border: 1px solid #DDDDDD;
            border-radius: 4px;
            background: white;
        }
    """,
    
    'Dark': """
        QWidget { 
            background: #2D2D30; 
            color: #FFFFFF;
            font-family: 'Segoe UI', 'Arial'; 
            font-size: 10pt;
        }
        QPushButton { 
            border: none; 
            border-radius: 4px;
            padding: 8px 16px; 
            background-color: #0D7377;
            color: white;
        }
        QPushButton:hover {
            background-color: #14FFEC;
            color: #2D2D30;
        }
        QPushButton:pressed { 
            background-color: #14FFEC;
            color: #2D2D30;
        }
        QTextEdit, QLineEdit { 
            background: #1E1E1E; 
            color: #FFFFFF;
            border: 1px solid #3E3E42;
            border-radius: 4px;
            padding: 4px;
        }
        QLineEdit:focus {
            border: 1px solid #0D7377;
        }
        QLabel { 
            background: transparent; 
            color: #FFFFFF;
        }
        QListWidget {
            background: #1E1E1E;
            color: #FFFFFF;
            border: 1px solid #3E3E42;
            border-radius: 4px;
        }
        QScrollArea {
            border: 1px solid #3E3E42;
            border-radius: 4px;
            background: #1E1E1E;
        }
    """,
    
    'Vintage Terminal': """
        QWidget { 
            background: #000000; 
            color: #33FF33;
            font-family: 'Courier New', monospace; 
            font-size: 11pt;
        }
        QPushButton { 
            border: 1px solid #33FF33; 
            border-radius: 0px;
            padding: 5px 10px; 
            background-color: #000000;
            color: #33FF33;
        }
        QPushButton:hover {
            background-color: #003300;
        }
        QPushButton:pressed { 
            background-color: #006600;
        }
        QTextEdit, QLineEdit { 
            background: #000000; 
            color: #33FF33;
            border: 1px solid #33FF33;
            border-radius: 0px;
            padding: 4px;
        }
        QLabel { 
            background: transparent; 
            color: #33FF33;
        }
        QListWidget {
            background: #000000;
            color: #33FF33;
            border: 1px solid #33FF33;
            border-radius: 0px;
        }
        QScrollArea {
            border: 1px solid #33FF33;
            border-radius: 0px;
            background: #000000;
        }
    """
}