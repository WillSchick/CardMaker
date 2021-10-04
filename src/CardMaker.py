import PIL.Image, PIL.ImageTk, PIL.ImageFont, PIL.ImageDraw
import textwrap
from tkinter import *
from tkinter import filedialog
import os

def getProjDir():
    cwd = os.path.dirname(os.path.realpath(__file__))
    projDir = os.path.abspath(os.path.join(cwd, os.pardir))
    return projDir;

def getItemArt():
    TargetDir = projDir + "\\resources\\cardArt\\"
    root.filename = filedialog.askopenfilename(initialdir=TargetDir, title="Select art for your card", filetypes=(("png files", "*.png"),("all files", "*")))

def getFont():
    global fontPath

    TargetDir = projDir + "\\resources\\fonts\\"
    fontPath = filedialog.askopenfilename(initialdir=TargetDir, title="Select art for your card", filetypes=(("True Type Font", "*.ttf"), ("Open Type Format", "*.otf"), ("all files", "*")))

def getDrawPoint(targetCenter, textSize):
    return (#getDrawPoint()
        targetCenter[0] - textSize[0]//2,
        targetCenter[1] - textSize[1]//2
    )

class CardBuilder:
    def __init__(self, cardTemplatePath):
        self.name = ""
        self.price = ""
        self.itemSize = ""
        self.itemInfo = ""
        self.bonusTitle1 = ""
        self.bonusValue1 = ""
        self.bonusTitle2 = ""
        self.bonusValue2 = ""

        self.artPath = ""

        # fontPath is a global variable
        global fontPath
        try:
            if fontPath == "":
                fontDir = getProjDir() + "\\resources\\Fonts\\"
                DEFAULT_FONT = "Roboto-Regular.ttf"
                fontPath = fontDir + DEFAULT_FONT
        except NameError:
            fontDir = getProjDir() + "\\resources\\Fonts\\"
            DEFAULT_FONT = "Roboto-Regular.ttf"
            fontPath = fontDir + DEFAULT_FONT
        headerFontSize = 50 
        bodyFontSize = 36
        self.fontColor = (0, 0, 0) #rgb
        self.headerFont = PIL.ImageFont.truetype(fontPath, headerFontSize)
        self.bodyFont = PIL.ImageFont.truetype(fontPath, bodyFontSize)

        # OPTIONAL
        self.isPixelArt = False

        # Card Template
        self.card = PIL.Image.open(cardTemplatePath)
        self.draw = PIL.ImageDraw.Draw(self.card)

        # Centers for elements on a medium card
        # CHANGE-ME IF YOU'RE USING A DIFFERENT CARD LAYOUT!!! :) :) :)
        # For this project I use a subclass to overwrite these values for sideways cards
        self.__bonusBoxPath__ = getProjDir() + "\\resources\\bonusBox.png"
        self.itemNameCenter = (373, 105)
        self.priceCenter = (208, 248)
        self.sizeCenter = (544, 246)
        self.artCenter = (377, 464)
        self.infoCenterWithoutBonus = (375, 786)
        self.infoCenterWithBonus = (315, 784)
        self.infoWidthWithoutBonus = 29
        self.infoWidthWithBonus = 23
        self.bonusCenter1 = (640, 892)
        self.bonusCenter2 = (640, 740)
        self.MAX_ART_WIDTH = 570
        self.MAX_ART_HEIGHT = 324

    def setName(self, newName):
        self.name = newName
    
    def setPrice(self, newPrice):
        self.price = newPrice

    def setItemSize(self, newSize):
        self.itemSize = newSize

    def setItemInfo(self, newItemInfo):
        self.itemInfo = newItemInfo

    def setBonusTitle1(self, newBonusTitle1):
        self.bonusTitle1 = newBonusTitle1

    def setBonusValue1(self, newBonusValue1):
        self.bonusValue1 = newBonusValue1
    
    def setBonusTitle2(self, newBonusTitle2):
        self.bonusTitle2 = newBonusTitle2

    def setBonusValue2(self, newBonusValue2):
        self.bonusValue2 = newBonusValue2

    def setArt(self, newArtPath):
        self.artPath = newArtPath

    def setIsPixelArt(self, newIsPixelArt):
        self.isPixelArt = newIsPixelArt;
    
    # takes new header font's filename and size
    def setHeaderFont(self, newFontFileName, newFontSize):
        fontPath = getProjDir() + "\\resources\\Fonts\\"
        self.headerFont = PIL.ImageFont.truetype(fontPath + newFontFileName, newFontSize)
    
    # takes new body font's filename and size
    def setBodyFont(self, newFontFileName, newFontSize):
        fontPath = getProjDir() + "\\resources\\Fonts\\"
        self.bodyFont = PIL.ImageFont.truetype(fontPath + newFontFileName, newFontSize)

    # draws text to card. Used in build method
    def __writeText__(self, text, font, center, textWidth=999):
        text = "\n".join(textwrap.wrap(text, width=textWidth))
        textSize = self.draw.textsize(text, font)
        drawPoint = (center[0] - textSize[0]//2,
                    center[1] - textSize[1]//2)
        self.draw.text(drawPoint, text, self.fontColor, font=font)

    def __pasteImage__(self, imageToPaste, center):
        pastePoint = (center[0] - imageToPaste.size[0]//2,
                    center[1] - imageToPaste.size[1]//2)
        
        # try to paste image with alpha- but don't worry if there's no alpha channel
        try:
            self.card.paste(imageToPaste, pastePoint, imageToPaste)
        except ValueError:
            self.card.paste(imageToPaste, pastePoint)
        
    # returns true if card has a bonus currently
    def hasBonus(self):
        if (self.bonusTitle1 != "" or self.bonusTitle2 != ""):
            return True
        else:
            return False

    def __resizeArtToFit__(self, art):
        maxWidth = self.MAX_ART_WIDTH
        maxHeight = self.MAX_ART_HEIGHT

        artWidth = art.size[0]
        artHeight = art.size[1]

        ratio = min(maxWidth / artWidth, maxHeight / artHeight);

        art = art.resize((int(artWidth*ratio), int(artHeight*ratio)))

        return art

    # This function only scales art UPWARDS and is meant to give pixel art a higher resolution without blurryness or distortion
    def __resizePixelArtToFit__(self, art):
        maxWidth = self.MAX_ART_WIDTH
        maxHeight = self.MAX_ART_HEIGHT

        artWidth = art.size[0]
        artHeight = art.size[1]

        # Scale UP (this is for pixel art, so we need to be careful)
        if (artHeight > artWidth):
            factor = 1;
            while artHeight * 2 <= self.MAX_ART_HEIGHT:
                artHeight *= 2;
                factor *= 2
            artWidth *= factor
            art = art.resize((artWidth, artHeight), PIL.Image.NEAREST)
        else:
            factor = 1;
            while artWidth * 2 <= self.MAX_ART_WIDTH:
                artWidth *= 2;
                factor *= 2
            artHeight *= factor
            art = art.resize((artWidth, artHeight), PIL.Image.NEAREST)

        return art
        
    # Builds and returns image of user's card
    def buildCard(self):
        # Item Headers
        self.__writeText__(self.name, self.headerFont, self.itemNameCenter)
        self.__writeText__(self.price, self.headerFont, self.priceCenter)
        self.__writeText__(self.itemSize, self.headerFont, self.sizeCenter)
        
        # Item Description
        if (self.hasBonus()):
            self.__writeText__(self.itemInfo, self.bodyFont, self.infoCenterWithBonus, textWidth=self.infoWidthWithBonus)
        else:
            self.__writeText__(self.itemInfo, self.bodyFont, self.infoCenterWithoutBonus, textWidth=self.infoWidthWithoutBonus)
        
        # Bonus boxes
        bonusBox = PIL.Image.open(self.__bonusBoxPath__)
        
        if (self.bonusTitle1 != ""):
            self.__pasteImage__(bonusBox, self.bonusCenter1)
            self.__writeText__(self.bonusTitle1, self.bodyFont, (self.bonusCenter1[0], self.bonusCenter1[1] - int(bonusBox.size[1]*0.666)))
            self.__writeText__(self.bonusValue1, self.headerFont, self.bonusCenter1)
        
        if (self.bonusTitle2 != ""):
            self.__pasteImage__(bonusBox, self.bonusCenter2)
            self.__writeText__(self.bonusTitle2, self.bodyFont, (self.bonusCenter2[0], self.bonusCenter2[1] - int(bonusBox.size[1]*0.666)))
            self.__writeText__(self.bonusValue2, self.headerFont, self.bonusCenter2)

        # Item Art
        try:
            art = PIL.Image.open(self.artPath)
        except AttributeError:
            art = PIL.Image.new('RGB', (1, 1), (255, 255, 255))

        # Resize art depending on type
        if (self.isPixelArt):
            art = self.__resizePixelArtToFit__(art)
        else:
            art = self.__resizeArtToFit__(art)

        self.__pasteImage__(art, self.artCenter)

        # return fully built card
        return self.card

class HorizontalCardBuilder(CardBuilder):
    def __init__(self, cardTemplatePath):
        super().__init__(cardTemplatePath)
        # Centers for elements on a small or large card
        # CHANGE-ME IF YOU'RE USING A DIFFERENT CARD LAYOUT!!! :) :) :)
        self.itemNameCenter = (496, 92)
        self.priceCenter = (268, 217)
        self.sizeCenter = (731, 216)
        self.artCenter = (310, 487)
        self.infoCenterWithoutBonus = (762, 483)
        self.infoCenterWithBonus = (720, 483)
        self.infoWidthWithoutBonus = 18
        self.infoWidthWithBonus = 12
        self.bonusCenter1 = (900, 647)
        self.bonusCenter2 = (900, 509)
        self.MAX_ART_WIDTH = 475
        self.MAX_ART_HEIGHT = 375

def createCard():
    global tkCard
    global cardPreviewLabel

    try:
        cardPreviewLabel.pack_forget()
    except NameError:
        pass

    sz = size.get()
    cardBuilder = None
    if sz == "Small" or sz == "Large":
        cardTemplatePath = getProjDir() + "\\resources\\itemTemplate(Small-Large).png"
        cardBuilder = HorizontalCardBuilder(cardTemplatePath)
    else:
        cardTemplatePath = getProjDir() + "\\resources\\itemTemplate(Medium).png"
        cardBuilder = CardBuilder(cardTemplatePath)
    
    #cardBuilder.setHeaderFont(fontName, 66)
    #cardBuilder.setBodyFont(fontName, 38)
    cardBuilder.setName(nameEntry.get())
    cardBuilder.setPrice(priceEntry.get())
    cardBuilder.setItemSize(sz)
    cardBuilder.setItemInfo(infoEntry.get())
    cardBuilder.setBonusTitle1(bonusTitleEntry.get())
    cardBuilder.setBonusValue1(bonusValueEntry.get())
    cardBuilder.setBonusTitle2(bonusTitleEntry2.get())
    cardBuilder.setBonusValue2(bonusValueEntry2.get())
    cardBuilder.setIsPixelArt(False)

    # add art
    try:
        cardBuilder.setArt(root.filename)
    except:
        pass # No worries if the user hasn't selected a file to use as art
    
    cardImage = cardBuilder.buildCard()

    # Orient horizontal cards for saving upright
    if sz == "Small" or sz == "Large":
        cardImage = cardImage.transpose(PIL.Image.ROTATE_270)

    # Save the card
    saveDir = projDir + "\\Output\\"
    fileName = nameEntry.get() + "-card.png"
    cardImage.save(saveDir + fileName)

    # reorient small and large cards for suitable previewing
    if sz == "Small" or sz == "Large":
        cardImage = cardImage.transpose(PIL.Image.ROTATE_90)

    # Resize the card and display a preview
    PREVIEW_SIZE_PERCENT = 0.2
    cardImage = cardImage.resize((int(cardImage.size[0]*PREVIEW_SIZE_PERCENT), int(cardImage.size[1]*PREVIEW_SIZE_PERCENT)))
    tkCard = PIL.ImageTk.PhotoImage(cardImage)
    cardPreviewLabel = Label(image=tkCard)
    cardPreviewLabel.pack(side = BOTTOM, pady=5)

# Tkinter
root = Tk()
root.title("Card Designer")
root.iconbitmap()

# tkinter stuff
root.geometry("700x800")

# Name
nameLabel = Label(root, text = "Item Name:")
nameEntry = Entry(root, width=25)
nameLabel.pack(ipadx=0, ipady=0)
nameEntry.pack(ipadx=0, ipady=0)

# Price
priceLabel = Label(root, text="Item Price:")
priceEntry = Entry(root, width=15)
priceLabel.pack()
priceEntry.pack()

# Size 
sizeLabel = Label(root, text="Item Size:")
size = StringVar()
size.set("Medium")
sizeOptionMenu = OptionMenu(root, size, "Small", "Medium", "Large")
sizeLabel.pack()
sizeOptionMenu.pack()

# Item Info
infoLabel = Label(root, text="Item Description:")
infoEntry = Entry(root, width=50)
infoLabel.pack()
infoEntry.pack(ipady=20)

# Item Bonuses
bonusTitleLabel = Label(root, text="Item modifier #1 title:")
bonusTitleEntry = Entry(root, width= 15)
bonusTitleLabel.pack()
bonusTitleEntry.pack()

bonusValueLabel = Label(root, text="Item modifier #1 value:").pack()
bonusValueEntry = Entry(root, width=5)
bonusValueEntry.pack()

# Bonus x2
bonusTitleLabel2 = Label(root, text="Item modifier #2 title:").pack()
bonusTitleEntry2 = Entry(root, width= 15)
bonusTitleEntry2.pack()

bonusValueLabel2 = Label(root, text="Item modifier #2 value:").pack()
bonusValueEntry2 = Entry(root, width=5)
bonusValueEntry2.pack()

# Art
artButton = Button(root, text="Pick Item Art", padx=10, pady=5, command=getItemArt)
artButton.pack(pady=10)

# Font
fontButton = Button(root, text="Pick Font", padx=10, pady=5, command=getFont)
fontButton.pack(pady=10)

# Create card button
createCardButton = Button(root, text="Create Card", padx=30, pady=10, command=createCard)
createCardButton.pack(side=BOTTOM, pady= 20)

cwd = os.path.dirname(os.path.realpath(__file__))
projDir = os.path.abspath(os.path.join(cwd, os.pardir))

root.mainloop()




