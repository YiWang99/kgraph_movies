import tkinter as tk
from tkinter import PhotoImage
import numpy as np
from tkinter import font,ttk
from PIL import Image, ImageTk

def filterSelection(e):
    selectedFilter = filterMenu.get()
    if selectedFilter == "Duration" or selectedFilter == "Release Year" or selectedFilter == "Content Rating":
        actorGenreInputText.grid_forget()
        comparisonSignMenu.grid(row=0, column=0, padx="10", pady="70", sticky="nw")
        durationRealeaseInputText.grid(row=0, column=0, padx="180", pady="70", sticky="nw")
    else:
        comparisonSignMenu.grid_forget()
        durationRealeaseInputText.grid_forget()
        actorGenreInputText.grid(row=0, column=0, padx="10", pady="70", sticky="nw")

def addFilter():
    selectedIndex = filterMenu.current()
    if selectedIndex == 2 or selectedIndex == 3 or selectedIndex == 11:
        input = durationRealeaseInputText.get(1.0, tk.END).strip()
        comperator = comparisonSignMenu.get().strip()
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
    index = 0
    for filter in filterTexts:
        rawString = filter.get(1.0,tk.END).strip()
        elements = rawString.split(";")
        label = filterLabels[index].cget("text")
        label = label[:-1]
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

def clearContentRatingsFilter():
    contentRatingFilters.configure(state="normal")
    contentRatingFilters.delete(1.0,tk.END)
    contentRatingFilters.configure(state="disabled")

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

#create labels
addFilterLabel = tk.Label(rootWindow, text="Add Filter", width=12, font=("Arial", 20, "bold"), background=color6)
appliedFiltersLabel = tk.Label(rootWindow, text="Applied Filters", width=12, font=("Arial", 20, "bold"), background=color6)
movieLabel = tk.Label(rootWindow, text="Movie", width=12, font=("Arial", 20, "bold"), background=color6)
abstractLabel = tk.Label(rootWindow, text="Abstract", width=12, font=("Arial", 20, "bold"), background=color6)

actorsLabel = tk.Label(rootWindow, text="Actors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
genresLabel = tk.Label(rootWindow, text="Genres:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
durationLabel = tk.Label(rootWindow, text="Duration:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
releaseYearLabel = tk.Label(rootWindow, text="Release:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
directorsLabel = tk.Label(rootWindow, text="Directors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
distributorsLabel = tk.Label(rootWindow, text="Distributors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
producersLabel = tk.Label(rootWindow, text="Producers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
languagesLabel = tk.Label(rootWindow, text="Languages:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
writersLabel = tk.Label(rootWindow, text="Writers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
editorsLabel = tk.Label(rootWindow, text="Editors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))
musicContributorsLabel = tk.Label(rootWindow, text="Music Contributors:", width=10, anchor="w", foreground="white", background=color4, font=("Arial", 19, "bold"))
contentRatingLabel = tk.Label(rootWindow, text="Content Rating:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 19, "bold"))

filterLabels = np.array([actorsLabel, genresLabel, durationLabel, releaseYearLabel, directorsLabel, distributorsLabel,
                producersLabel, languagesLabel, writersLabel, editorsLabel, musicContributorsLabel,
                contentRatingLabel])


#create buttons
searchButton = tk.Button(rootWindow, text="Search", command=searchMovies, background=color4, foreground="white",
                              activebackground=color5, border = 0, width=10, height=2, cursor = "hand2",
                              font=("Arial", 16, "bold"), activeforeground="white")
findMoreButton = tk.Button(rootWindow, text="Find More", background=color4, foreground="white",
                              activebackground=color5, border = 0, width=10, height=2, cursor = "hand2",
                              font=("Arial", 16, "bold"), activeforeground="white")
addFilterButton = tk.Button(rootWindow, text="Add", command=addFilter)

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
clearContentRatingButton = tk.Button(rootWindow, text="Clear", command=clearContentRatingsFilter, background=color1,
                              activebackground=color2, border = 0, width=5, height=0, cursor = "hand2",
                              font=("Arial", 14, "bold"))

clearButtons = np.array([clearActorsButton, clearGenresButton, clearDurationButton, clearReleaseButton,
                         clearDirectorButton ,clearDistributorButton, clearProducerButton, clearLanguageButton,
                         clearWriterButton, clearEditorButton, clearMusicContributorButton, clearContentRatingButton])


#create text fields
actorGenreInputText = tk.Text(rootWindow, height=1, width=100)
durationRealeaseInputText = tk.Text(rootWindow, height=1, width=100)

abstractText = tk.Text(rootWindow, height=100, width=100)

actorsFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
genresFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
durationFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
releaseYearFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
directorsFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
distributorsFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
producersFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
languagesFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
writersFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
editorsFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
musicContributorsFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")
contentRatingFilters = tk.Text(rootWindow, height=2, width=140, state="disabled")

filterTexts = np.array([actorsFilters, genresFilters, durationFilters, releaseYearFilters, directorsFilters, distributorsFilters,
           producersFilters, languagesFilters, writersFilters, editorsFilters, musicContributorsFilters,
           contentRatingFilters])

#create dropdown menus
movieOptions = ["Godfather", "Apocalypse Now", "Dune", "Forrest Gump"]
movieMenu = ttk.Combobox(rootWindow, values=movieOptions, state="readonly")
movieMenu.set("Movie List")
filterOptions = ["Actor", "Genre", "Duration", "Release Year", "Director", "Distributor", "Producer", "Language",
                 "Writer", "Editor", "Music Contributr", "Content Rating"]
filterMenu = ttk.Combobox(rootWindow, values=filterOptions, state="readonly")
filterMenu.set("Choose Filter")
filterMenu.bind("<<ComboboxSelected>>", filterSelection)
comparisonOptions = ["<", "<=", "=", "=>", ">"]
comparisonSignMenu = ttk.Combobox(rootWindow, values=comparisonOptions, state="readonly")
comparisonSignMenu.set("Select")

#add content to grid
yPos = 50
for i in range(filterLabels.size):
    filterLabels[i].grid(row=1, column=0, padx=10, pady=str(yPos), sticky="nw")
    filterTexts[i].grid(row=1, column=0, padx="180", pady=str(yPos), sticky="nw")
    clearButtons[i].grid(row=1, column=0, padx="10", pady=str(yPos), sticky="ne")
    yPos += 50

addFilterLabel.grid(row=0, column=0, padx="10", pady="10", sticky="n")
filterMenu.grid(row=0, column=0, padx="10", pady="40", sticky="nw")
addFilterButton.grid(row=0, column=0, padx="10", pady="40", sticky="ne")
appliedFiltersLabel.grid(row=1, column=0, padx="10", pady="10", sticky="n")
searchButton.grid(row=2, column=0, padx="10", pady="10", sticky="n")
movieLabel.grid(row=0, column=1, padx="10", pady="10", sticky="n")
movieMenu.grid(row=0, column=1, padx="10", pady="40", sticky="nw")
abstractLabel.grid(row=1, column=1, padx="10", pady="10", sticky="n")
abstractText.grid(row=1, column=1, padx="10", pady="50", sticky="nw")
findMoreButton.grid(row=2, column=1, padx="10", pady="10", sticky="n")

rootWindow.grid_rowconfigure(0, minsize=30)
rootWindow.grid_rowconfigure(1, minsize=630)
rootWindow.grid_rowconfigure(2, minsize=100)


for i in range(2):
    rootWindow.grid_rowconfigure(i, weight=1, uniform="row")
for i in range(2):
    rootWindow.grid_columnconfigure(i, weight=2, uniform="column")


rootWindow.mainloop()