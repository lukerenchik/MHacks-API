
import ChatGPT
import keyboard
import pdfParse
import wikiPageGetter
import vision
import string
import os
import sys
directory_path = r"C:\Users\Luke\Desktop\MHacksAPI\MHacksAPI\TactileGraphics"

if directory_path not in sys.path:
    sys.path.append(directory_path)
import GraphicsEngine
import TactileDisplay



class dotUI(GraphicsEngine.GraphicsEngine):

    def __init__(self, nRows, nColumns, Display):
        super().__init__((nRows, nColumns))
        # a connection to the tactile display
        self.m_Display = Display
        # this is the container for a desired state of the braille display
        self.desiredState = [[0 for iDot in range(0, nColumns)] for iRow in range(0, nRows)]
        self.pdfPath = "pdfLibrary"


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



    def break_text(self, text, max_length=72):
        """
        Breaks a text string into chunks at punctuation, with each chunk having a maximum length.

        Args:
        text (str): The text to be broken into chunks.
        max_length (int): Maximum length of each chunk.

        Returns:
        list: A list of text chunks.
        """

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

    def create_pages(self, list, char_limit=72):
        pages = []
        current_page = ""

        for string in list:
            # Check if adding the next string exceeds the character limit
            if len(current_page + string + 1) <= char_limit:
                current_page = current_page + " " + string
            else:
                # Add the current page to pages and start a new one
                pages.append(current_page)
                current_page = string

        # Don't forget to add the last page if it's not empty
        if current_page:
            pages.append(current_page)

        return pages

    def openDOT(self):
        self.clearDisplay()
        textToOutput = "Welcome to dotUI, press enter for menu options."
        self.addBraille((0, 0), textToOutput)
        self.refreshDisplay()
        input(textToOutput)

    def pageTurner(self, pages):
        index = 0
        while True:
            # Print the current item
            print(pages[index])
            self.clearDisplay()
            self.addBraille((0, 0), pages[index])
            self.refreshDisplay()
            # Wait for a key press
            key = keyboard.read_key()

            if key == 'right':
                # Increment index but don't go past the end of the list
                index = min(index + 1, len(pages) - 1)
            elif key == 'left':
                # Decrement index but don't go below 0
                index = max(index - 1, 0)
            elif key == 'esc':
                # Exit the loop if escape key is pressed
                break
        print(pages)
        pass

    def chatWithGPT(self):
        self.clearDisplay()
        self.addBraille((0, 0), "Input: ")
        self.refreshDisplay()
        response = ChatGPT.talkWithGPT()
        chunksToRead = self.break_text(response)
        self.pageTurner(chunksToRead)
        pass

    def wikipediaSearch(self):
        self.clearDisplay()
        self.addBraille((0, 0), "Enter the Search Term: ")
        self.refreshDisplay()
        imageList, pageText = wikiPageGetter.search()
        pageText = pageText.text
        print(pageText)
        chunked_page = self.break_text(pageText)
        self.pageTurner(chunked_page)
        for i in range(4):
            describedImage = vision.describe_image(imageList.images[i])
            describedImage = self.break_text(describedImage)
            self.pageTurner(describedImage)
        pass

    def ParsePDF(self, filename):
        imageList = pdfParse.parseImages(filename)
        for i in range(len(imageList)):
            chunksToRead = self.break_text(imageList[i])
            self.pageTurner(chunksToRead)
        text = pdfParse.parseText(filename)
        chunkedText = self.break_text(text)
        self.pageTurner(chunkedText)
        pass

    def loadPDF(self):
        files = os.listdir(self.pdfPath)
        filenames = []
        for i, filename in enumerate(files, start=1):
            filenames.append(f"{i}, {filename}")
        intro_message = "You will be shown a list of PDF's that are loaded in your pdf folder, remember the number of the file you wish to select. Press Enter to Continue."
        input(intro_message)
        chunked_intro = dotUI.break_text(intro_message)
        dotUI.pageTurner(chunked_intro)
        pdf_list = dotUI.create_pages(filenames)
        dotUI.pageTurner(pdf_list)
        pdfSelection = input("Please input selection number:")
        pdfLink = enumerate(files, pdfSelection)
        return pdfLink

    def speechToText(self):
        pass

    def textToSpeech(self):
        pass

    def closeDOT(self):
        pass

    def menu(self):
        # Automatically initialize openDOT when the state machine starts
        self.openDOT()

        while True:
            self.clearDisplay()
            self.addBraille((0, 0), "1. Wiki 2. PDF 3. ChatGPT 4. Exit Enter your choice:")
            self.refreshDisplay()
            print("1. Wiki Search")
            print("2. PDF Parser")
            print("3. ChatGPT")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.wikipediaSearch()
            elif choice == "2":
                self.parseFile = self.loadPDF()
                self.ParsePDF(self.parseFile)
            elif choice == "3":
                self.chatWithGPT()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # create a connection to the tactile display
    Display = TactileDisplay.TactileDisplay("COM5", 115200, 3)

    for i in range(Display.nRows):
        Display.setRow(i, [0 for iDot in range(Display.nColumns)])
    # create a graphics engine the correct size of the display

    Engine = dotUI(Display.nColumns, Display.nRows, Display)

    # this is the container for a desired state of the braille display
    Engine.desiredState = [[0 for iDot in range(0, Display.nColumns)] for iRow in range(0, Display.nRows)]

    Engine.menu()