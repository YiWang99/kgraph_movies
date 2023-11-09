import tkinter as tk
from tkinter import PhotoImage
import numpy as np
from tkinter import font,ttk
from PIL import Image, ImageTk

def filterSelection(e):
    selectedFilter = filterMenu.get()
    if selectedFilter == "Duration" or selectedFilter == "Release Year" or selectedFilter == "Content Rating":
        actorGenreInputText.place_forget()
        comparisonSignMenu.place(x=10, y=90)
        durationRealeaseInputText.place(x=150, y=90)
    else:
        comparisonSignMenu.place_forget()
        durationRealeaseInputText.place_forget()
        actorGenreInputText.place(x=10, y=90)

def addFilter():
    selectedIndex = filterMenu.current()
    if selectedIndex == 2 or selectedIndex == 3 or selectedIndex == 11:
        input = durationRealeaseInputText.get(1.0, tk.END).strip()
        comperator = comparisonSignMenu.get().strip()
        if input != "" and comperator != "Comparator":
            filterTexts[selectedIndex].configure(state="normal")
            print(len(filterTexts[selectedIndex].get(1.0, tk.END)))
            if len(filterTexts[selectedIndex].get(1.0, tk.END)) == 1:
                filterTexts[selectedIndex].insert("insert", comperator + " " + input)
            else:
                filterTexts[selectedIndex].insert("insert", ";" + comperator + " " + input)
            filterTexts[selectedIndex].configure(state="disabled")
            durationRealeaseInputText.delete(1.0,tk.END)
    else:
        input = actorGenreInputText.get(1.0, tk.END).strip()
        filterTexts[selectedIndex].configure(state="normal")
        if len(filterTexts[selectedIndex].get(1.0, tk.END)) == 1:
            filterTexts[selectedIndex].insert("insert", input)
        else:
            filterTexts[selectedIndex].insert("insert", ";" + input)
        filterTexts[selectedIndex].configure(state="disabled")
        actorGenreInputText.delete(1.0,tk.END)

def searchMovies():
    filterArray = []
    filterNames = np.array(["actor", "genre", "runtime", "initial_release_date", "director", "producer", "language",
                            "writer", "editor", "music_contributor", "country"])
    index = 0
    for filter in filterTexts:
        rawString = filter.get(1.0,tk.END).strip()
        elements = rawString.split(";")
        label = filterNames[index]
        elements.insert(0, label)
        rowArray = np.array(elements, dtype="str")
        filterArray.append(rowArray)
        index += 1
    for row in filterArray:
        print(row)

def clearActorsFilter():
    actorsFilters.configure(state="normal")
    actorsFilters.delete(1.0,tk.END)
    actorsFilters.configure(state="disabled")

def clearGenresFilter():
    genresFilters.configure(state="normal")
    genresFilters.delete(1.0,tk.END)
    genresFilters.configure(state="disabled")

def clearDurationFilter():
    durationFilters.configure(state="normal")
    durationFilters.delete(1.0,tk.END)
    durationFilters.configure(state="disabled")

def clearReleaseYearFilter():
    releaseYearFilters.configure(state="normal")
    releaseYearFilters.delete(1.0,tk.END)
    releaseYearFilters.configure(state="disabled")

def clearDirectorFilter():
    directorsFilters.configure(state="normal")
    directorsFilters.delete(1.0,tk.END)
    directorsFilters.configure(state="disabled")

def clearDistributorFilter():
    distributorsFilters.configure(state="normal")
    distributorsFilters.delete(1.0,tk.END)
    distributorsFilters.configure(state="disabled")

def clearProducersFilter():
    producersFilters.configure(state="normal")
    producersFilters.delete(1.0,tk.END)
    producersFilters.configure(state="disabled")

def clearLanguagesFilter():
    languagesFilters.configure(state="normal")
    languagesFilters.delete(1.0,tk.END)
    languagesFilters.configure(state="disabled")

def clearWritersFilter():
    writersFilters.configure(state="normal")
    writersFilters.delete(1.0,tk.END)
    writersFilters.configure(state="disabled")

def clearEditorsFilter():
    editorsFilters.configure(state="normal")
    editorsFilters.delete(1.0,tk.END)
    editorsFilters.configure(state="disabled")

def clearMusicContributorsFilter():
    musicContributorsFilters.configure(state="normal")
    musicContributorsFilters.delete(1.0,tk.END)
    musicContributorsFilters.configure(state="disabled")



#Create and set up rootWindow
rootWindow = tk.Tk()
rootWindow.title("MovieFinder")
rootWindow.geometry("1400x900")
rootWindow.wm_attributes("-transparentcolor", 'grey')

#Colors
color1 = "#ff476d"
color2 = "#ff7894"
color3 = "#7bb2d6"
color4 = "#2F4858"
color5 = "#4a718a"
color6 = "#7BD6A1"

backgroundImage = Image.open("ressources/background.jpg")
background = ImageTk.PhotoImage(backgroundImage)
background_label = tk.Label(rootWindow, image=background)
background_label.place(relwidth=1, relheight=1)

bold_font = font.nametofont("TkDefaultFont")
bold_font.configure(weight="bold")

#create canva with headlines
canvas = tk.Canvas(rootWindow, width=1400, height=900, bg=rootWindow.cget('bg'), highlightthickness=0)
canvas.place(x=0, y=0)
backgroundImage = Image.open("ressources/background.jpg")
background = ImageTk.PhotoImage(backgroundImage)
canvas.create_image(700, 450, anchor=tk.CENTER, image=background)
canvas.create_text(95, 30, text="Add Filters", font="arial 25 bold", fill="white")
canvas.create_text(125, 200, text="Applied Filters", font="arial 25 bold", fill="white")
canvas.create_text(814, 30, text="Movies", font="arial 25 bold", fill="white")
canvas.create_text(826, 200, text="Abstract", font="arial 25 bold", fill="white")

#create labels
actorsLabel = tk.Label(rootWindow, text="Actors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
genresLabel = tk.Label(rootWindow, text="Genres:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
durationLabel = tk.Label(rootWindow, text="Duration:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
releaseYearLabel = tk.Label(rootWindow, text="Release:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
directorsLabel = tk.Label(rootWindow, text="Directors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
distributorsLabel = tk.Label(rootWindow, text="Distributors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
producersLabel = tk.Label(rootWindow, text="Producers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
languagesLabel = tk.Label(rootWindow, text="Languages:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
writersLabel = tk.Label(rootWindow, text="Writers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
editorsLabel = tk.Label(rootWindow, text="Editors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
musicContributorsLabel = tk.Label(rootWindow, text="Composer:", width=10, anchor="w", foreground="white", background=color4, font=("Arial", 15, "bold"))

filterLabels = np.array([actorsLabel, genresLabel, durationLabel, releaseYearLabel, directorsLabel, distributorsLabel,
                producersLabel, languagesLabel, writersLabel, editorsLabel, musicContributorsLabel])


#create buttons
searchButton = tk.Button(rootWindow, text="Search", command=searchMovies, background=color4, foreground="white",
                              activebackground=color5, border = 0, width=10, height=2, cursor = "hand2",
                              font=("Arial", 16, "bold"), activeforeground="white")
findMoreButton = tk.Button(rootWindow, text="Find More", background=color4, foreground="white",
                              activebackground=color5, border = 0, width=10, height=2, cursor = "hand2",
                              font=("Arial", 16, "bold"), activeforeground="white")
addFilterButton = tk.Button(rootWindow, text="Add", command=addFilter, background=color4, foreground="white",
                              activebackground=color5, border=0, width=5, height=1, cursor = "hand2",
                              font=("Arial", 14, "bold"), activeforeground="white")

clearActorsButton = tk.Button(rootWindow, text="Clear", command=clearActorsFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearGenresButton = tk.Button(rootWindow, text="Clear", command=clearGenresFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearDurationButton = tk.Button(rootWindow, text="Clear", command=clearDurationFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearReleaseButton = tk.Button(rootWindow, text="Clear", command=clearReleaseYearFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearDirectorButton = tk.Button(rootWindow, text="Clear", command=clearDirectorFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearDistributorButton = tk.Button(rootWindow, text="Clear", command=clearDistributorFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearProducerButton = tk.Button(rootWindow, text="Clear", command=clearProducersFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearLanguageButton = tk.Button(rootWindow, text="Clear", command=clearLanguagesFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearWriterButton = tk.Button(rootWindow, text="Clear", command=clearWritersFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearEditorButton = tk.Button(rootWindow, text="Clear", command=clearEditorsFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))
clearMusicContributorButton = tk.Button(rootWindow, text="Clear", command=clearMusicContributorsFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))


clearButtons = np.array([clearActorsButton, clearGenresButton, clearDurationButton, clearReleaseButton,
                         clearDirectorButton ,clearDistributorButton, clearProducerButton, clearLanguageButton,
                         clearWriterButton, clearEditorButton, clearMusicContributorButton])


#create text fields
actorGenreInputText = tk.Text(rootWindow, height=1, width=72)
durationRealeaseInputText = tk.Text(rootWindow, height=1, width=54)

abstractText = tk.Text(rootWindow, height=33, width=78)

actorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
genresFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
durationFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
releaseYearFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
directorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
distributorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
producersFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
languagesFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
writersFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
editorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
musicContributorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")

filterTexts = np.array([actorsFilters, genresFilters, durationFilters, releaseYearFilters, directorsFilters, distributorsFilters,
           producersFilters, languagesFilters, writersFilters, editorsFilters, musicContributorsFilters])

#create dropdown menus
movieOptions = ["Godfather", "Apocalypse Now", "Dune", "Forrest Gump"]
movieMenu = ttk.Combobox(rootWindow, values=movieOptions, state="readonly")
movieMenu.set("Movie List")
filterOptions = ["Actor", "Genre", "Duration", "Release", "Director", "Distributor", "Producer", "Language",
                 "Writer", "Editor", "Composer"]
filterMenu = ttk.Combobox(rootWindow, values=filterOptions, state="readonly", width=17)
filterMenu.set("Choose Filter")
filterMenu.bind("<<ComboboxSelected>>", filterSelection)
comparisonOptions = ["<", "<=", "=", "=>", ">"]
comparisonSignMenu = ttk.Combobox(rootWindow, values=comparisonOptions, state="readonly", width=17)
comparisonSignMenu.set("Comparator")

#add content to grid
yPos = 240
for i in range(filterLabels.size):
    rectangle = canvas.create_rectangle(10,yPos, 136,yPos+36,fill=color4, outline="")
    filterLabels[i].place(x=10, y=str(yPos+3))
    filterTexts[i].place(x=150, y=str(yPos))
    clearButtons[i].place(x=600, y=str(yPos))
    yPos += 50

filterMenu.place(x=10, y=60)
addFilterButton.place(x=600, y=75)
searchButton.place(x=300, y=800)
movieMenu.place(x=760, y=60)
abstractText.place(x=760, y=240)
findMoreButton.place(x=1000, y=800)




rootWindow.mainloop()