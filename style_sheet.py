
style_sheet = """ 
                QWidget#main_widget {border : 1px solid rgb(50, 50, 50);
                                    border-radius : 3px;}
                
                QInputDialog QPushButton , QMessageBox QPushButton {background-color : rgb(0, 50, 200);
                                        padding : 7px;
                                        color : white;
                                        font-size : 13px;
                                        width : 40px;}
                
                QInputDialog QDialog {width : 200px;}
                
                QInputDialog QPushButton:hover , QMessageBox QPushButton:hover {background-color : rgb(0, 80, 200);
                                                color : white}
                QInputDialog QLineEdit {padding : 3px;
                                        min-width : 400px;
                                        background-color : rgb(10, 10, 10);
                                        border : 1px solid rgb(50, 50, 50);
                                        border-radius : 2px;}
                        
                QPushButton {background-color : none;
                            color : rgb(0, 250, 150);
                            border-radius : 3px;
                            padding : 5px;
                            border : 1px solid rgb(50, 50, 50);
                            width : 30px;
                            font-size : 20px;}
                QPushButton:hover , QPushButton:pressed {
                                        color : rgb(0, 250, 150);
                                        border : 1px solid rgb(80, 80, 80)}
                                
                QPushButton#addButton {background : none;
                                        color : rgb(0, 250, 120);
                                        font-size : 30px;
                                        border : noen}
                                        
                QPushButton#addButton:hover {color : rgb(0, 250, 180);}
                
                QPushButton#removeButton {background-color : none;
                                        color : rgb(250, 20, 0);
                                        font-size : 35px;
                                        border : none}
                                        
                QPushButton#removeButton:hover {color : rgb(250, 50, 0);}
                            
                QLabel {background : none;
                        color : white}
                        
                QCheckBox::indicator:unchecked {background-color : rgb(250, 50, 0);
                                    border-radius : 2px;
                                    }
                QCheckBox::indicator:checked {background-color : rgb(0, 250, 50);
                                    border-radius : 2px;
                                    } 
                
                QLabel#titleLabel {color : rgb(250, 0, 220)}
                
                QPushButton#delete_all_button {background : none;
                                                color : red;
                                                border : 1px solid rgb(50, 50, 50);
                                                border-radius : 3px;
                                                padding : 7px;
                                                width : 100px;
                                                font-size : 12px;}
                QPushButton#delete_all_button:hover {border : 1px solid rgb(80, 80, 80)}"""