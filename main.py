import math
import os
import random
import copy

from PIL import Image, ImageTk, ImageDraw

from tkinter import Label, Radiobutton, Tk, Canvas, NW, Entry, Button, IntVar
import webbrowser

def calculateRootQuadraticEquation(a: float, b: float, c: float) -> list[float]:
    discr = b ** 2 - 4 * a * c
    if discr > 0:
        x1 = (-b + math.sqrt(discr)) / (2 * a)
        x2 = (-b - math.sqrt(discr)) / (2 * a)
        return [x1, x2]
    elif discr == 0:
        x = -b / (2 * a)
        return [x]
    else:
        raise Exception(f"Нет корней для: {a}x^2 + {b}x + {c} = 0!")

def getPositive(decimals: list[float]):
    if   decimals[0] > 0: return decimals[0]
    elif decimals[1] > 0: return decimals[1]
    elif decimals[0] == 0: return 0
    else: raise Exception(f"Нет положительных в {decimals}")

class Dobble():
    def __init__(self, imgs: list, countOfCards: int, countOfItems: int):
        self.imgs = imgs
        self.numbersOfItems = len(self.imgs)
        self.countOfCards = countOfCards
        self.order = countOfItems

    def getNumberOfItemInOneCard(self) -> int:
        return int(getPositive(calculateRootQuadraticEquation(1, 1, 1-self.numbersOfItems)))

    def generateCards2(self):
        nbSymByCard = self.getNumberOfItemInOneCard() if self.getNumberOfItemInOneCard() <= self.order else self.order
        nbCards = (nbSymByCard**2) - nbSymByCard + 1
        cards = []
        n = nbSymByCard - 1
        t = []
        t.append([[(i+1)+(j*n) for i in range(n)] for j in range(n)])
        for ti in range(n-1):
            t.append([[t[0][((ti+1)*i) % n][(j+i) % n] for i in range(n)] for j in range(n)])
        t.append([[t[0][i][j] for i in range(n)] for j in range(n)])
        for i in range(n):
            t[0][i].append(nbCards - n)
            t[n][i].append(nbCards - n + 1)
            for ti in range(n-1):
                t[ti+1][i].append(nbCards - n + 1 + ti + 1)
        t.append([[(i+(nbCards-n)) for i in range(nbSymByCard)]])
        for ti in t:
            cards = cards + ti
        for i in cards:
            random.shuffle(i);
        return cards[:self.countOfCards+1]

    def generateCards(self):
        p = self.getNumberOfItemInOneCard() if self.getNumberOfItemInOneCard() <= self.order else self.order-1
        for min_factor in range(2, 1 + int(p ** 0.5)):
            if p % min_factor == 0:
                break
        else:
            min_factor = p
        cards = []
        for i in range(p):
            cards.append(set([i * p + j for j in range(p)] + [p * p]))
        for i in range(min_factor):
            for j in range(p):
                cards.append(set([k * p + (j + i * k) % p
                                for k in range(p)] + [p * p + 1 + i]))
        for i in cards:
            random.shuffle(list(i));
        return list(cards[:self.countOfCards+1])


class DobbleImageSettings():
    def __init__(self, shape):
        self.shape = shape

class DobbleImageGenerator():
    def __init__(self, dobble: Dobble, settings: DobbleImageSettings, scale):
        self.dobble = dobble
        self.settings = settings
        self.scale = scale    
        self.cardSize = int(210*scale/2*0.94)
        self.shapeImage = Image.new("RGB", (self.cardSize, self.cardSize), "#FFF")

        draw = ImageDraw.Draw(self.shapeImage)
        match settings.shape:
            case "circle":    draw.ellipse  ((0, 0, self.cardSize-1,  self.cardSize-1), fill=(255, 255, 255), outline=(0, 0, 0))
            case "square":    draw.rectangle((0, 0, self.cardSize-1,  self.cardSize-1), fill=(255, 255, 255), outline=(0, 0, 0))
            case "rectangle": draw.rectangle((0, 0, self.cardSize-36, self.cardSize-1), fill=(255, 255, 255), outline=(0, 0, 0))
            case _:           draw.ellipse  ((0, 0, self.cardSize-1,  self.cardSize-1), fill=(255, 255, 255), outline=(0, 0, 0))


    def getCards(self, count):
        cards = []
        cardsData = self.dobble.generateCards()[ :count]
        for i in cardsData:
            images = []
            for j in i:
                images.append(self.dobble.imgs[j])
            random.shuffle(images)
            cards.append(
                    createCard(self.shapeImage, images, self.cardSize)
                    )
        return cards

    def getSheets(self, count):
        cards = self.getCards(count)
        random.shuffle(cards)
        lists = []
        for i in range(5, len(cards), 6):
            lists.append(createSheet(cards[i-5:i+1], self.scale))
        lists.append(createSheet(cards[len(cards)-len(cards)%6: len(cards)], self.scale))
        return lists



class ItemPosition():
    def __init__(self, coordinates, size):
         self.coordinates = (int(coordinates[0]-size[0]/2), int(coordinates[1]-size[1]/2))
         self.size = (int(size[0]), int(size[1]))


def createCard(shape, imgs, size):
    positions = [
        [],#0
        [#1
            ItemPosition((size/2, size/2), (size*0.7, size*0.7))
        ],
        [#2
            ItemPosition((size/4*1.3,   size/2), (size/2, size/2)), 
            ItemPosition((size/4*3, size/2), (size/4, size/4))
        ],
        [#3
            ItemPosition((size/2,   size/4), (size/2.5, size/2.5)),
            ItemPosition((size/4*2.5, size/2*1.5), (size/2.5, size/2.5)), 
            ItemPosition((size/4, size/2*1.25), (size/3.2, size/3.2))
        ],
        [#4
            ItemPosition((size/3,   size/3*1.1), (size/2.5, size/2.5)),
            ItemPosition((size/3*2, size/3*0.8), (size/3.4, size/3.4)), 
            ItemPosition((size/3, size/3*2.3), (size/3.9, size/3.9)),
            ItemPosition((size/3*2, size/3*2), (size/3.6, size/3.6)),
        ],
        [#5
            ItemPosition((size/2,   size/3.5), (size/2.5, size/2.5)),
            ItemPosition((size/6, size/2), (size/7, size/7)), 
            ItemPosition((size/3, size/3*2.3), (size/3.9, size/3.9)),
            ItemPosition((size/3*2, size/3*2), (size/3, size/3)),
            ItemPosition((size/5*3.7, size/3), (size/6, size/6)),
        ],
        [#6
            ItemPosition((size/1.9,   size/3.5), (size/2.5, size/2.5)),
            ItemPosition((size/4.2, size/3.8), (size/5, size/5)), 
            ItemPosition((size/6, size/2), (size/4.5, size/4.5)),
            ItemPosition((size/3, size/3*2.3), (size/3.9, size/3.9)),
            ItemPosition((size/3*2, size/3*2), (size/3, size/3)),
            ItemPosition((size/5*4, size/3), (size/5, size/5)),
        ],
        [#7
            ItemPosition((size/2.2,   size/3.5), (size/2.5, size/2.5)),
            ItemPosition((size/1.5,   size/4), (size/8, size/8)),
            ItemPosition((size/1.3,   size/2), (size/5, size/5)),
            ItemPosition((size/1.3,   size/1.5), (size/8, size/8)),
            ItemPosition((size/5,   size/1.6), (size/4, size/4)),
            ItemPosition((size/8.5,   size/2.5), (size/6, size/6)),
            ItemPosition((size/2,   size/1.3), (size/3, size/3)),
        ],
        [#8
            ItemPosition((size/1.9,   size/3.5), (size/2.5, size/2.5)),
            ItemPosition((size/1.2,   size/4*1.2), (size/5, size/5)),
            ItemPosition((size/1.3,   size/2), (size/5, size/5)),
            ItemPosition((size/1.2,   size/1.4), (size/5, size/5)),
            ItemPosition((size/5,   size/1.6), (size/4, size/4)),
            ItemPosition((size/8.5,   size/2.5), (size/6, size/6)),
            ItemPosition((size/2,   size/1.3), (size/3, size/3)),
            ItemPosition((size/2,   size/1.86), (size/6, size/6)),
        ],
        [#9
            ItemPosition((size/2,   size/3), (size/4.5, size/4.5)),
            ItemPosition((size/3.2,   size/5), (size/5.5, size/5.5)),
            ItemPosition((size/1.5,   size/4), (size/8, size/8)),
            ItemPosition((size/1.3,   size/2), (size/5, size/5)),
            ItemPosition((size/1.3,   size/1.5), (size/8, size/8)),
            ItemPosition((size/5,   size/1.6), (size/4, size/4)),
            ItemPosition((size/7.5,   size/2.5), (size/6, size/6)),
            ItemPosition((size/2,   size/1.3), (size/3, size/3)),
            ItemPosition((size/2,   size/1.86), (size/8, size/8)),
        ],
        [#10
            ItemPosition((size/2,   size/3), (size/4.5, size/4.5)),
            ItemPosition((size/3.2,   size/5), (size/5.5, size/5.5)),
            ItemPosition((size/1.9,   size/6.6), (size/8, size/8)),
            ItemPosition((size/1.4,   size/4), (size/5.5, size/5.5)),
            ItemPosition((size/1.3,   size/2), (size/5, size/5)),
            ItemPosition((size/1.3,   size/1.5), (size/8, size/8)),
            ItemPosition((size/5,   size/1.6), (size/4, size/4)),
            ItemPosition((size/7.5,   size/2.5), (size/6, size/6)),
            ItemPosition((size/2,   size/1.3), (size/3, size/3)),
            ItemPosition((size/2,   size/1.86), (size/8, size/8)),
        ],
    ]
    def s(t):
        return (int(t[0]*0.85), int(t[1]*0.85))

    background = Image.new("RGB", (int(size), int(size)), "#FFF")
    background.paste(shape, (0, 0))
    imgsCopy = copy.deepcopy(imgs)
    for i in range(len(positions[len(imgsCopy)])):
        imgsCopy[i].thumbnail(s(positions[len(imgsCopy)][i].size))
        imgsCopy[i].resize(s(positions[len(imgsCopy)][i].size))
        imgsCopy[i].convert('RGBA')
        background.paste(imgsCopy[i], positions[len(imgsCopy)][i].coordinates)

    return background

def createSheet(cards, r):
    back = Image.new("RGB", (210*r, 297*r), "#FFF")
    if len(cards)>=1: back.paste(cards[0], (0,0))
    if len(cards)>=2: back.paste(cards[1], (cards[0].width,0))
    if len(cards)>=3: back.paste(cards[2], (0,cards[0].height))
    if len(cards)>=4: back.paste(cards[3], (cards[0].width,cards[0].height))
    if len(cards)>=5: back.paste(cards[4], (0,cards[0].height+cards[0].height))
    if len(cards)>=6: back.paste(cards[5], (cards[0].width,cards[0].height+cards[0].height))
    return back

def getImages() -> list:
    imagesDir = "images/"
    imgs = []
    for i in os.listdir(imagesDir):
        imgs.append(Image.open(f'{imagesDir}{i}'))
    random.shuffle(imgs)
    if len(imgs) <= 0:
        raise Exception("Нет изображений для карточек! (Изображения должны храниться в папке: images/)")
    return imgs

def show(img):
    frame = Tk()
    frame.title("Доббль")
    tatras = ImageTk.PhotoImage(img)
    canvas = Canvas(frame, width=img.size[0]+20, height=img.size[1]+20)
    canvas.create_image(10, 10, anchor=NW, image=tatras)
    canvas.pack()
    frame.mainloop()

class DobbleSettings():
    def getSettings(self):
        self.frame = Tk()
        self.frame.title("Доббль")

        Label(self.frame, text="Форма карточек:").pack()
        self.shape = "circle"
        self.shapeD = IntVar()
        self.shapeD.set(0)
        radioGroup:list[Radiobutton] = []
        radioGroup.append(Radiobutton(self.frame, width=30, text="Круг", value = 0, variable=self.shapeD))
        radioGroup.append(Radiobutton(self.frame, width=30, text="Квадрат", value = 1, variable=self.shapeD))
        radioGroup.append(Radiobutton(self.frame, width=30, text="Прямоугольник", value = 2, variable=self.shapeD))
        for i in radioGroup: i.pack()

        Label(self.frame, text="Максимальное количество карточек:").pack()
        self.entry1 = Entry(self.frame)
        self.entry1.insert(0, "100")
        self.entry1.pack()

        Label(self.frame, text="Максимальное количество изображений на карточке:").pack()
        self.entry2 = Entry(self.frame)
        self.entry2.insert(0, "10")
        self.entry2.pack()
    
        button = Button(self.frame, width=30, text="Далее", command=self.button_click)
        button.pack()
        
        self.frame.mainloop()
        
        return DobbleImageSettings(self.shape), int(self.entry1.get()), int(self.entry2.get())
    
    def button_click(self):
        match self.shapeD.get():
            case 0:
                self.shape = "circle"
            case 1:
                self.shape = "square"
            case 2:
                self.shape = "rectangle"
        try:
            1/int(self.entry1.get())
            1/int(self.entry2.get())
            if (int(self.entry2.get())>10): raise Exception("Количество изображений на карточке не должно быть больше 10!")
        except ValueError:
            log(Exception("Количество должно быть числом"));
        except ZeroDivisionError:
            log(Exception("Количество должно быть числом отличным от нуля!"));
        except Exception as ex:
            log(ex)
        finally:
            self.frame.quit()

    def quit(self):
        self.frame.destroy();

def savePdf(path, imgs):
    imgs[0].save(
        path, "PDF", resolution=100.0, save_all=True, append_images=imgs[1:]
    )

def openErrorMessage(text: str):
    frame = Tk()
    frame.title(text)
    Label(frame, text=text).pack()
    def button_click(): frame.destroy()
    Button(frame, text="ok", command=button_click).pack()
    frame.mainloop()

def log(ex: Exception):
    print(str(ex))
    openErrorMessage(str(ex))

def main():
    while True:
        try:
            settings = DobbleSettings()
            shape, countOfCards, countOfItems = settings.getSettings()
            settings.quit()
            dig = DobbleImageGenerator(
                    Dobble(getImages(), countOfCards, countOfItems), 
                    shape,
                    10
            )
            sheets = dig.getSheets(countOfCards)
            savePdf("cards/card.pdf", sheets)
            webbrowser.open("file:///"+(os.path.realpath(__name__)[: -9])+"\\cards\\card.pdf")
        except Exception as ex:
            if str(ex) != 'invalid command name ".!entry"':
                log(ex)
            else:
                break


if __name__ == "__main__":
    main()
