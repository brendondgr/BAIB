from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSizePolicy, QTextEdit, QComboBox, QCheckBox, QLineEdit, QSplitter, QLabel
from PySide6.QtCore import Qt, QDateTime, QThreadPool
from BAI import BAI_commands as bc
from BAI import BAI_Bot as bb

# Creates a central widget for QMainWindow
class Menu(QMainWindow):
    def __init__(self):
        import configparser
        super().__init__()
        self.setWindowTitle("Brendon's AI Bot (BAIB)")
        
        # Config
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        
        # Sets the minimum sizes for the window
        self.setMinimumSize(800, 600)
        
        # Creates a BAI Bot For Application
        self.baibot = bb(int(self.config["history"]["max"]))
        
        # Create a central widget and set it to the setCustomCentralWidget function
        central_widget = QSplitter(Qt.Horizontal)
        central_layout = self.setCustomCentralWidget()
        central_widget.addWidget(central_layout)
        self.setCentralWidget(central_widget)
        
        self.show()
        
    def setCustomCentralWidget(self):
        # Create a console widget equal to right box
        right_box = QWidget()
        right_layout = QVBoxLayout()
        console_widget = ConsoleWidget()
        right_layout.addWidget(console_widget)
        right_box.setLayout(right_layout)  # Set the layout of right_box to right_layout
        
        left_box = OptionsPanel(console_widget, self.config, self.baibot)

        # Add the widgets to the splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_box)
        splitter.addWidget(right_box)

        # Set the initial sizes of the widgets
        splitter.setSizes([400, 400])

        # Set the stretch factor of the left_box to 0 and the stretch factor of the right_box to 1
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        return splitter


############################################################################
##   This widget will be used to display what is occuring in the program  ##
##     to a makeshift console that will contain timestamps and other      ##
##           information of what is occuring in the program.              ##
############################################################################
class ConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.text_edit)

    def add_message(self, message):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        formatted_message = f"[{timestamp}] {message}"
        self.text_edit.append(formatted_message)
        
    def add_inquiry(self, inquiry):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        question = f"[{timestamp}] Q > {inquiry}"
        self.text_edit.append(question)
        
    def add_response(self, response):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        answer = f"[{timestamp}] A > {response}"
        self.text_edit.append(answer)
        
    def clear(self):
        self.text_edit.clear()
        
############################################################################
##               Creates a Left Widget for the Application                ##
############################################################################
class OptionsPanel(QWidget):
    def __init__(self, console, config, baibot):
        super().__init__()
        self.messageCount = 0
        self.console = console
        self.config = config
        self.baibot = baibot
        self.init_ui()
        
    def init_ui(self):
        from json import load
        self.layout = QVBoxLayout(self)
        
        # Makes the layout push all items to the top
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(0)
        
        #################################################
        ##                  Title Box                  ##
        #################################################
        # Creates a Centered Title for the Application
        self.title = QTextEdit(self)
        self.title.setReadOnly(True)
        self.title.setText("Brendon's AI Bot (BAIB)")
        # Centers Text in Box
        self.title.setAlignment(Qt.AlignCenter)
        # Sets Font Size to 20
        self.title.setStyleSheet("font-size: 16px;")
        # Set Height to 35 pixels
        self.title.setFixedHeight(35)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.title)
        
        #################################################
        ##                   API Token                 ##
        #################################################
        with open(f"{self.config['folders']['tokens']}/token.txt") as f:
            apitoken = f.read()
        # Creates a Title and Text Box, that reads in current API Token from file
        self.apitoken_block = QWidget(self)
        # Sets the layout for the token block to QV
        self.apitoken_block.setLayout(QHBoxLayout(self))
        # Adds a label to the token block
        self.apitoken_label = QLabel(self)
        self.apitoken_label.setText("API Token:")
        # Sets Sizes for the label
        self.apitoken_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Adds Items to List
        self.apitoken_textbox = QLineEdit(self)
        self.apitoken_textbox.setText(apitoken)
        # Adds Items to Token Block
        self.apitoken_block.layout().addWidget(self.apitoken_label)
        self.apitoken_block.layout().addWidget(self.apitoken_textbox)
        # Adds Token Block to Main Layout
        self.layout.addWidget(self.apitoken_block)
        
        #################################################
        ##                Model Selection              ##
        #################################################
        # Createa a drop down menu based on the list of models returned from BAI_commands
        with open(f'{self.config["folders"]["schemas"]}{self.config["subfolders"]["models"]}') as f:
            self.models = load(f)
        model_list = bc.getModelList(self.models)
        self.model_block = QWidget(self)
        # Sets the layout for the model block to QV
        self.model_block.setLayout(QHBoxLayout(self))
        # Adds a label to the model block
        self.model_label = QLabel(self)
        self.model_label.setText("Model:")
        # Sets Sizes for the label
        self.model_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Adds Items to List
        self.model_dropdown = QComboBox(self)
        self.model_dropdown.addItems(model_list)
        # Adds Items to Model Block
        self.model_block.layout().addWidget(self.model_label)
        self.model_block.layout().addWidget(self.model_dropdown)
        # Adds Model Block to Main Layout
        self.layout.addWidget(self.model_block)
        
        #################################################
        ##               Personality Type              ##
        #################################################
        with open(f"{self.config['folders']['schemas']}{self.config['subfolders']['personality']}") as f:
            self.personalities = load(f)
        # Creates a drop down menu based on the list of personalities returned from BAI_commands
        personality_list = bc.personalityList(self.personalities)
        self.personality_block = QWidget(self)
        # Sets the layout for the personality block to QV
        self.personality_block.setLayout(QHBoxLayout(self))
        # Adds a label to the personality block
        self.personality_label = QLabel(self)
        self.personality_label.setText("Personality Type:")
        # Sets Sizes for the label
        self.personality_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Adds Items to List
        self.personality_dropdown = QComboBox(self)
        self.personality_dropdown.addItems(personality_list)
        # Adds Items to Personality Block
        self.personality_block.layout().addWidget(self.personality_label)
        self.personality_block.layout().addWidget(self.personality_dropdown)
        
        # Adds Personality Block to Main Layout
        self.layout.addWidget(self.personality_block)
        
        #################################################
        ##                Message Length               ##
        #################################################
        with open(f"{self.config['folders']['schemas']}{self.config['subfolders']['messagelength']}") as f:
            self.messagelengths = load(f)
        # Creates a drop down menu based on the list of message lengths returned from BAI_commands
        message_length_list = bc.getMessageLengthList(self.messagelengths)
        self.message_length_block = QWidget(self)
        # Sets the layout for the length block to QV
        self.message_length_block.setLayout(QHBoxLayout(self))
        # Adds a label to the length block
        self.message_length_label = QLabel(self)
        self.message_length_label.setText("Response Length:")
        # Sets Sizes for the label
        self.message_length_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Adds Items to List
        self.message_length_dropdown = QComboBox(self)
        self.message_length_dropdown.addItems(message_length_list)
        # Adds Items to Block
        self.message_length_block.layout().addWidget(self.message_length_label)
        self.message_length_block.layout().addWidget(self.message_length_dropdown)
        # Adds Block to Main Layout
        self.layout.addWidget(self.message_length_block)        
        
        #################################################
        ##                CheckBox Block               ##
        #################################################
        # Sets up a checkbox for emoji use
        self.checkbox_block = QWidget(self)
        # Sets the layout for the checkbox block to QV
        self.checkbox_block.setLayout(QHBoxLayout(self))
        # Creates Checkbox for TTS
        self.emoji_checkbox = QCheckBox(self)
        # Adds Label to Checkbox
        self.emoji_checkbox.setText("Use Emojis")
        # Adds Items to Length Block
        self.checkbox_block.layout().addWidget(self.emoji_checkbox)
        
        #################################################
        ##                Text to Speech               ##
        #################################################
        # Sets up the Checkbox for the TTS
        self.tts_block = QWidget(self)
        # Sets the layout for the checkbox block to QV
        self.tts_block.setLayout(QHBoxLayout(self))
        # Creates Checkbox for TTS
        self.tts_block = QCheckBox(self)
        # Adds Label to Checkbox
        self.tts_block.setText("Use TTS")
        # Adds Items to to checkbox_block
        self.checkbox_block.layout().addWidget(self.tts_block)
        
        #################################################
        ##               Save TTS Message              ##
        #################################################
        # Sets up the Checkbox for the Save TTS Message
        self.savetts_block = QWidget(self)
        # Sets the layout for the checkbox block to QV
        self.savetts_block.setLayout(QHBoxLayout(self))
        # Cretes Checkbox for Save TTS Message
        self.savetts_block = QCheckBox(self)
        # Adds Label to Checkbox
        self.savetts_block.setText("Save TTS Message")
        # Adds Items to checkbox_block
        self.checkbox_block.layout().addWidget(self.savetts_block)
        
        self.layout.addWidget(self.checkbox_block)
        
        #################################################
        ##               Question Field                ##
        #################################################
        # Adds a field for the user to enter their question
        self.question_field = QTextEdit(self)
        self.question_field.setPlaceholderText("Enter your question here...")
        self.question_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.question_field)
        
        #################################################
        ##                Submit Query                 ##
        #################################################
        # Adds a button to submit the question
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.fetch_response)
        self.submit_button.setFixedHeight(30)
        # Centers the button
        self.submit_button.setStyleSheet("QPushButton { margin-left: 50%; margin-right: 50%; }")
        self.layout.addWidget(self.submit_button)
        
    def fetch_response(self):
        # Fetches the API Token from the token field
        apitoken = self.apitoken_textbox.text()
        
        # Fetches the model from the model field
        model = self.model_dropdown.currentText()
        model_name = bc.getModelName(model, self.models)
        
        # Fetches the personality from the personality field
        personality = self.personality_dropdown.currentText()
        personality_description = bc.getPersonality(personality, self.personalities)
        
        # Fetches the message length from the message length field
        message_length = self.message_length_dropdown.currentText()
        message_length_description, token_limit = bc.getMessageLength(message_length, self.messagelengths)
        
        # Fetches the question from the question field
        question = self.question_field.toPlainText()
        
        # Fetches the emoji use from the checkbox
        emoji = self.emoji_checkbox.isChecked()
        emoji = bc.emojiUse(emoji)
        
        # Fetches the TTS use from the checkbox
        tts = self.tts_block.isChecked()
        
        # Fetches the Save TTS Message use from the checkbox
        savetts = self.savetts_block.isChecked()
        
        # Creates a Worker for API Signals
        query = QueryObject(apitoken, model_name, personality_description, message_length_description, token_limit, question, emoji, tts, savetts)
        self.APIWorker = SendAPI(query, self.baibot, self.messageCount)
        
        # Connect Messages to Console
        self.APIWorker.signals.inquiry.connect(self.console.add_inquiry)
        self.APIWorker.signals.response.connect(self.console.add_response)
        self.APIWorker.signals.finished.connect(self.console.add_message)
        
        # Add Worker to Threadpool
        self.APIThreadpool = QThreadPool()
        self.APIThreadpool.start(self.APIWorker)

############################################################################
##                       Worker Classes and Signals                       ##
############################################################################
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

class QueryObject:
    def __init__(self, apitoken, model, personality, messagelength, tokenlimit, question, emoji, tts, savetts):
        self.apitoken = apitoken
        self.model = model
        self.personality = personality
        self.messagelength = messagelength
        self.tokenlimit = tokenlimit
        self.question = question
        self.emoji = emoji
        self.tts = tts
        self.savetts = savetts

#########################################################
##                -- Worker Signals --                 ##
##            Transmitting API Information             ##
#########################################################
class SendAPISignals(QObject):
    finished = Signal(str)
    inquiry = Signal(str)
    response = Signal(str)
    
class SendAPI(QRunnable):
    def __init__(self, query, baibot, messageCount):
        super().__init__()
        self.messageCount = messageCount
        self.query = query
        self.baibot = baibot
        self.signals = SendAPISignals()
        
    @Slot()
    def run(self):
        # Sends Inquiry to Console
        self.signals.inquiry.emit(self.query.question)
        
        # Sends Inquiry to API and returns/parses response
        response = bc.askQuestion(self.query, self.baibot)
        response = bc.parseData(response.text)[0]
        
        # Saves Message to History
        self.baibot.saveHistory(self.query.question, response)
        
        # Sends Response to Console
        self.signals.response.emit(response)
        
        if self.query.tts:
            # Saves TTS Message
            bc.ttsMessage(response, self.messageCount, self.query.savetts)
        
        # Sends Finished Signal to Console
        #self.signals.finished.emit(f'Finished Querying API')
        
        
if __name__ == "__main__":
    import sys
    from main_app import main
    app = main()
    sys.exit(app.exit())