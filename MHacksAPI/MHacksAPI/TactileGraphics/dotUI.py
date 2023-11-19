from GraphicsEngine import GraphicsEngine
import Features as f
import numpy as np
import TactileDisplay as td
import ChatGPT
import keyboard
import pdfParse
import wikiPageGetter
import vision


class Graphics(GraphicsEngine):

    def __init__(self, nRows, nColumns, Display):
        super().__init__((nRows, nColumns))
        # a connection to the tactile display
        self.m_Display = Display
        # this is the container for a desired state of the braille display
        self.desiredState = [[0 for iDot in range(0, nColumns)] for iRow in range(0, nRows)]

    def draw(self):
        # draw the objects to the display
        self.drawFeatures()
        # retrieve the drawing
        self.desiredState = self.retrieveList()

    def refreshDisplay(self):
        # draw the graphical objects
        self.draw()

        # go row by row and set the desired state
        for rowIndex in range(0, self.m_Display.nRows):
            self.m_Display.setRow(rowIndex, self.desiredState[rowIndex])

    def clearDisplay(self):
        # clear the graphical objects
        self.clearFeatures()
        self.draw()

        # go row by row and set the desired state
        for rowIndex in range(0, self.m_Display.nRows):
            self.m_Display.setRow(rowIndex, self.desiredState[rowIndex])


if __name__ == "__main__":

    parseFile = "docs/michigan_maryland.pdf"

    # create a connection to the tactile display
    Display = td.TactileDisplay("COM5", 115200, 3)

    for i in range(Display.nRows):
        Display.setRow(i, [0 for iDot in range(Display.nColumns)])
    # create a graphics engine the correct size of the display

    Engine = Graphics(Display.nColumns, Display.nRows, Display)

    # this is the container for a desired state of the braille display
    Engine.desiredState = [[0 for iDot in range(0, Display.nColumns)] for iRow in range(0, Display.nRows)]


    def break_text(text, max_length=72):
        """
        Breaks a text string into chunks at punctuation, with each chunk having a maximum length.

        Args:
        text (str): The text to be broken into chunks.
        max_length (int): Maximum length of each chunk.

        Returns:
        list: A list of text chunks.
        """
        import string

        if len(text) <= max_length:
            return [text]

        chunks = []
        while text:
            if len(text) <= max_length:
                chunks.append(text)
                break

            # Find the nearest punctuation mark before the max_length
            break_index = max([text.rfind(punc, 0, max_length + 1) for punc in string.punctuation + ' '])

            if break_index <= 0:  # No suitable break point found
                break_index = max_length  # Break at the max_length if no punctuation found

            chunks.append(text[:break_index].strip())
            text = text[break_index:].strip()

        return chunks


    def openDOT():
        Engine.clearDisplay()
        textToOutput = "Welcome to dotUI, press enter for menu options."
        Engine.addBraille((0, 0), textToOutput)
        Engine.refreshDisplay()
        input(textToOutput)


    def pageTurner(chunksToRead):
        index = 0
        while True:
            # Print the current item
            print(chunksToRead[index])
            Engine.clearDisplay()
            Engine.addBraille((0, 0), chunksToRead[index])
            Engine.refreshDisplay()
            # Wait for a key press
            key = keyboard.read_key()

            if key == 'right':
                # Increment index but don't go past the end of the list
                index = min(index + 1, len(chunksToRead) - 1)
            elif key == 'left':
                # Decrement index but don't go below 0
                index = max(index - 1, 0)
            elif key == 'esc':
                # Exit the loop if escape key is pressed
                break
        print(chunksToRead)
        pass


    def chatWithGPT():
        index = 0
        Engine.clearDisplay()
        Engine.addBraille((0, 0), "Input: ")
        Engine.refreshDisplay()
        response = ChatGPT.talkWithGPT()
        chunksToRead = break_text(response)
        while True:
            # Print the current item
            print(chunksToRead[index])
            Engine.clearDisplay()
            Engine.addBraille((0, 0), chunksToRead[index])
            Engine.refreshDisplay()
            # Wait for a key press
            key = keyboard.read_key()

            if key == 'right':
                # Increment index but don't go past the end of the list
                index = min(index + 1, len(chunksToRead) - 1)
            elif key == 'left':
                # Decrement index but don't go below 0
                index = max(index - 1, 0)
            elif key == 'esc':
                # Exit the loop if escape key is pressed
                break
        print(chunksToRead)
        pass


    def ParsePDF(filename):
        imageList = pdfParse.parseImages(filename)
        for i in range(len(imageList)):
            chunksToRead = break_text(imageList[i])
            pageTurner(chunksToRead)
        text = pdfParse.parseText(filename)
        chunkedText = break_text(text)
        pageTurner(chunkedText)
        pass


    def wikipediaSearch():
        Engine.clearDisplay()
        Engine.addBraille((0, 0), "Enter the Search Term: ")
        imageList, pageText = wikiPageGetter.search()
        pageText = pageText.text
        print(pageText)
        chunked_page = break_text(pageText)
        pageTurner(chunked_page)
        for i in range(4):
            describedImage = vision.describe_image(imageList.images[i])
            describedImage = break_text(describedImage)
            pageTurner(describedImage)
        pass


    def speechToText():
        pass


    def textToSpeech():
        pass


    def closeDOT():
        pass


    # applicationState = 0

    # applicationTasks = [
    #    wikipediaSearch,
    #    chatWithGPT,
    #    ParsePDF,
    #    closeDOT
    # ]
    def menu():
        # Automatically initialize openDOT when the state machine starts
        openDOT()

        while True:
            Engine.clearDisplay()
            Engine.addBraille((0,0),"1. Wiki    2. PDF    3. ChatGPT    4. Exit   Enter your choice:")
            Engine.refreshDisplay()
            print("1. Wiki Search")
            print("2. PDF Parser")
            print("3. ChatGPT")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                wikipediaSearch()
            elif choice == "2":
                ParsePDF(parseFile)
            elif choice == "3":
                chatWithGPT()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")


    if __name__ == "__main__":
        menu()



    # while 1:
    #    applicationTasks[appplicationState]()
    #    print(applicationTasks[appplicationState])
    #   appplicationState = int(input("next state: "))

    def closeScreen():
        Engine.clearDisplay()
        textToOutput = "This is the close screen"
        Engine.addBraille((0, 0), textToOutput)
        Engine.refreshDisplay()


    ## above is the intializing code for the various objects necessary ##
    ## below is the scene scripting paradigm ##
    """
    input("Scene 1: Intro to the Graphics Engine")
    Engine.clearDisplay()

    # Scene 1
    Engine.addBraille((0,0), "This is an intro to adding features using the graphics engine")

    Engine.refreshDisplay()

    input("Scene 2: Adding a Point to the display")
    Engine.clearDisplay()

    # Scene 2
    Engine.addPoint((0,0))

    Engine.refreshDisplay()

    input("Scene 3: Adding a Line to the display")
    Engine.clearDisplay()

    # Scene 3
    Engine.addLine((0,0), (34,18), 3)

    Engine.refreshDisplay()

    input("Scene 4: Adding a Triangle to the display")
    Engine.clearDisplay()

    # create the triangle vertices list
    triangleVertices = [(0,0), (28,18), (34,0)]

    # Scene 3
    Engine.addTriangle(triangleVertices, 4)

    Engine.refreshDisplay()

    input("Scene 5: Adding a Circle to the display")
    Engine.clearDisplay()

    # create the center point
    centerPoint = (20,10)

    # create the radius
    radius = 5

    # Scene 5
    Engine.addCircle(centerPoint, radius, 2)

    Engine.refreshDisplay()

    input("Scene 6: Adding a Rectangle to the display")
    Engine.clearDisplay()

    # Scene 3
    Engine.addRectangle((0,0), (20,13), 3)

    Engine.refreshDisplay()
    """
