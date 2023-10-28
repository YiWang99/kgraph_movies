import tkinter as tk
from tkinter import font,ttk

def filterSelection(e):
    selectedFilter = filterMenu.get()
    if selectedFilter == "Actor" or selectedFilter == "Genre":
        comparisonSignMenu.grid_forget()
        durationRealeaseInputText.grid_forget()
        actorGenreInputText.grid(row=0, column=0, padx="10", pady="70", sticky="nw")
    else:
        actorGenreInputText.grid_forget()
        comparisonSignMenu.grid(row=0, column=0, padx="10", pady="70", sticky="nw")
        durationRealeaseInputText.grid(row=0, column=0, padx="180", pady="70", sticky="nw")

def addFilter():
    selectedFilter = filterMenu.get()
    if selectedFilter != "":
        if selectedFilter == "Actor":
            actor = actorGenreInputText.get(1.0, tk.END).strip()
            actorsFilters.configure(state="normal")
            actorsFilters.insert("insert", actor + ";")
            actorsFilters.configure(state="disabled")
        elif selectedFilter == "Genre":
            genre = actorGenreInputText.get(1.0, tk.END).strip()
            genresFilters.configure(state="normal")
            genresFilters.insert("insert", genre + ";")
            genresFilters.configure(state="disabled")
        elif selectedFilter == "Duration":
            duration = durationRealeaseInputText.get(1.0, tk.END).strip()
            comperator = comparisonSignMenu.get().strip()
            durationFilters.configure(state="normal")
            durationFilters.insert("insert", comperator + " " + duration)
            durationFilters.configure(state="disabled")
        elif selectedFilter == "Release Year":
            releaseYear = durationRealeaseInputText.get(1.0, tk.END).strip()
            comperator = comparisonSignMenu.get().strip()
            releaseYearFilters.configure(state="normal")
            releaseYearFilters.insert("insert", comperator + " " + releaseYear)
            releaseYearFilters.configure(state="disabled")

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

#Create and set up rootWindow
rootWindow = tk.Tk()
rootWindow.title("MovieFinder")
rootWindow.geometry("1000x600")

bold_font = font.nametofont("TkDefaultFont")
bold_font.configure(weight="bold")

#create labels
addFilterLabel = tk.Label(rootWindow, text="Add Filter", font=bold_font)
appliedFiltersLabel = tk.Label(rootWindow, text="Applied Filters", font=bold_font)
movieLabel = tk.Label(rootWindow, text="Movie", font=bold_font)
abstractLabel = tk.Label(rootWindow, text="Abstract", font=bold_font)

actorsLabel = tk.Label(rootWindow, text="Actors:")
genresLabel = tk.Label(rootWindow, text="Genres:")
durationLabel = tk.Label(rootWindow, text="Duration:")
releaseYearLabel = tk.Label(rootWindow, text="Release Year:")

#create buttons
searchButton = tk.Button(rootWindow, text="Search", width=10, height=1)
findMoreButton = tk.Button(rootWindow, text="Find more", width=10, height=1)
addFilterButton = tk.Button(rootWindow, text="Add", command=addFilter)
clearActorsButton = tk.Button(rootWindow, text="Clear", command=clearActorsFilter)
clearGenresButton = tk.Button(rootWindow, text="Clear", command=clearGenresFilter)
clearDurationButton = tk.Button(rootWindow, text="Clear", command=clearDurationFilter)
clearReleaseButton = tk.Button(rootWindow, text="Clear", command=clearReleaseYearFilter)

#create text fields
actorGenreInputText = tk.Text(rootWindow, height=1, width=100)
durationRealeaseInputText = tk.Text(rootWindow, height=1, width=100)

abstractText = tk.Text(rootWindow, height=100, width=100)

actorsFilters = tk.Text(rootWindow, height=1, width=100, state="disabled")
genresFilters = tk.Text(rootWindow, height=1, width=100, state="disabled")
durationFilters = tk.Text(rootWindow, height=1, width=100, state="disabled")
releaseYearFilters = tk.Text(rootWindow, height=1, width=100, state="disabled")

#create dropdown menus
movieOptions = ["Godfather", "Apocalypse Now", "Dune", "Forrest Gump"]
movieMenu = ttk.Combobox(rootWindow, values=movieOptions, state="readonly")
movieMenu.set("Movie List")
filterOptions = ["Actor", "Genre", "Duration", "Release Year"]
filterMenu = ttk.Combobox(rootWindow, values=filterOptions, state="readonly")
filterMenu.set("Choose Filter")
filterMenu.bind("<<ComboboxSelected>>", filterSelection)
comparisonOptions = ["<", "<=", "=", "=>", ">"]
comparisonSignMenu = ttk.Combobox(rootWindow, values=comparisonOptions, state="readonly")
comparisonSignMenu.set("Select")

#add content to grid
addFilterLabel.grid(row=0, column=0, padx="10", pady="10", sticky="nw")
filterMenu.grid(row=0, column=0, padx="10", pady="40", sticky="nw")
addFilterButton.grid(row=0, column=0, padx="10", pady="40", sticky="ne")
appliedFiltersLabel.grid(row=1, column=0, padx="10", pady="10", sticky="nw")
actorsLabel.grid(row=1, column=0, padx="10", pady="40", sticky="nw")
actorsFilters.grid(row=1, column=0, padx="80", pady="40", sticky="nw")
clearActorsButton.grid(row=1, column=0, padx="10", pady="40", sticky="ne")
genresLabel.grid(row=1, column=0, padx="10", pady="70", sticky="nw")
genresFilters.grid(row=1, column=0, padx="80", pady="70", sticky="nw")
clearGenresButton.grid(row=1, column=0, padx="10", pady="70", sticky="ne")
durationLabel.grid(row=1, column=0, padx="10", pady="100", sticky="nw")
durationFilters.grid(row=1, column=0, padx="80", pady="100", sticky="nw")
clearDurationButton.grid(row=1, column=0, padx="10", pady="100", sticky="ne")
releaseYearLabel.grid(row=1, column=0, padx="10", pady="130", sticky="nw")
releaseYearFilters.grid(row=1, column=0, padx="80", pady="130", sticky="nw")
clearReleaseButton.grid(row=1, column=0, padx="10", pady="130", sticky="ne")
searchButton.grid(row=2, column=0, padx="10", pady="10", sticky="n")
movieLabel.grid(row=0, column=1, padx="10", pady="10", sticky="nw")
movieMenu.grid(row=0, column=1, padx="10", pady="40", sticky="nw")
abstractLabel.grid(row=1, column=1, padx="10", pady="10", sticky="nw")
abstractText.grid(row=1, column=1, padx="10", pady="40", sticky="nw")
findMoreButton.grid(row=2, column=1, padx="10", pady="10", sticky="n")

rootWindow.grid_rowconfigure(2, minsize=100)


for i in range(2):
    rootWindow.grid_rowconfigure(i, weight=1, uniform="row")
for i in range(2):
    rootWindow.grid_columnconfigure(i, weight=1, uniform="column")

rootWindow.mainloop()