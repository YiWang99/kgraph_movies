import tkinter as tk
from tkinter import PhotoImage
import numpy as np
from tkinter import font,ttk
from PIL import Image, ImageTk

import movies

queryResults = {}

def filterSelection(e):
    selectedFilter = filterMenu.get()
    if selectedFilter == "Duration" or selectedFilter == "Release":
        actorGenreInputText.place_forget()
        languageMenu.place_forget()
        genreMenu.place_forget()
        comparisonSignMenu.place(x=10, y=90)
        durationRealeaseInputText.place(x=150, y=90)
    elif selectedFilter == "Genre":
        comparisonSignMenu.place_forget()
        durationRealeaseInputText.place_forget()
        actorGenreInputText.place_forget()
        languageMenu.place_forget()
        genreMenu.place(x=10, y=90)
    elif selectedFilter == "Language":
        comparisonSignMenu.place_forget()
        durationRealeaseInputText.place_forget()
        actorGenreInputText.place_forget()
        genreMenu.place_forget()
        languageMenu.place(x=10, y=90)
    else:
        comparisonSignMenu.place_forget()
        durationRealeaseInputText.place_forget()
        languageMenu.place_forget()
        genreMenu.place_forget()
        actorGenreInputText.place(x=10, y=90)

def addFilter():
    selectedIndex = filterMenu.current()
    if selectedIndex == 1:
        input = genreMenu.get()
        filterTexts[selectedIndex].configure(state="normal")
        if len(filterTexts[selectedIndex].get(1.0, tk.END)) == 1:
            filterTexts[selectedIndex].insert("insert", input)
        else:
            filterTexts[selectedIndex].insert("insert", ";" + input)
        filterTexts[selectedIndex].configure(state="disabled")
    elif selectedIndex == 6:
        input = languageMenu.get()
        filterTexts[selectedIndex].configure(state="normal")
        if len(filterTexts[selectedIndex].get(1.0, tk.END)) == 1:
            filterTexts[selectedIndex].insert("insert", input)
        else:
            filterTexts[selectedIndex].insert("insert", ";" + input)
        filterTexts[selectedIndex].configure(state="disabled")
    elif selectedIndex == 2 or selectedIndex == 3 or selectedIndex == 11:
        input = durationRealeaseInputText.get(1.0, tk.END).strip()
        comperator = comparisonSignMenu.get().strip()
        if input != "" and comperator != "Comparator":
            filterTexts[selectedIndex].configure(state="normal")
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
    movieMenu.set("Movie List")
    for info in infoTexts:
        info.configure(state="normal")
        info.delete(1.0, tk.END)
        info.configure(state="disabled")

    filterArray = []
    filterNames = np.array(["actor", "genre", "runtime", "initial_release_date", "director", "producer",
                            "language", "writer", "editor", "music_contributor", "country"])
    index = 0
    for filter in filterTexts:
        rawString = filter.get(1.0, tk.END).strip()
        elements = rawString.split(";")
        label = filterNames[index]
        elements.insert(0, label)
        if index == 6:
            for i in range(len(elements)):
                if elements[i] == "English":
                    elements[i] = "en"
                elif elements[i] == "Hindu":
                    elements[i] = "hi"
                elif elements[i] == "French":
                    elements[i] = "fr"
                elif elements[i] == "Spanish":
                    elements[i] = "es"
                elif elements[i] == "Japanese":
                    elements[i] = "ja"
                elif elements[i] == "Tamil":
                    elements[i] = "ta"
                elif elements[i] == "Italian":
                    elements[i] = "it"
                elif elements[i] == "German":
                    elements[i] = "de"
                elif elements[i] == "Korean":
                    elements[i] = "ko"
                elif elements[i] == "Russian":
                    elements[i] = "ru"
        rowArray = np.array(elements, dtype="str")
        filterArray.append(rowArray)
        index += 1
    for row in filterArray:
        print(row)
    dummy = np.array(["country", ""])
    filterArray.append(dummy)
    queryResults = backend.activate_filter(filterArray, graph, 200, exactSearch.get())
    movieNames = queryResults["movie_name"]
    print(movieNames)
    movieMenu['values'] = movieNames
    if movieNames:
        errorLabel.place_forget()
    else:
        errorLabel.place(x=400, y=187)

def movieSelection(e):
    for info in infoTexts:
        info.configure(state="normal")
        info.delete(1.0, tk.END)
        info.configure(state="disabled")

    selectedMovie = movieMenu.get()
    print(selectedMovie)
    movieInfo = backend.activate_info(selectedMovie, graph)

    infoNames = ["actor_name", "genre_name", "runtime", "initial_release_date", "director_name", "producer_name",
                 "languageCode", "writer_name", "editor_name", "music_contributor_name"]

    index = 0
    for info in infoNames:
        infoTexts[index].configure(state="normal")
        first = True
        for content in movieInfo[info]:
            if first:
                infoTexts[index].insert("insert", content)
            else:
                infoTexts[index].insert("insert", ", " + content)
            first = False
        actorsInfo.configure(state="disabled")
        infoTexts[index].configure(state="disabled")
        index += 1



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

def selectExactSearch():
    fuzzySearchSelector.deselect()
    exactSearchSelector.configure(state="disabled")
    fuzzySearchSelector.configure(state="normal")


def selectFuzzySearch():
    exactSearchSelector.deselect()
    fuzzySearchSelector.configure(state="disabled")
    exactSearchSelector.configure(state="normal")




#Load Backend
backend = movies
graph = movies.load_kg("linkedmdb.nt")

#Create and set up rootWindow
rootWindow = tk.Tk()
rootWindow.title("MovieFinder")
rootWindow.geometry("1400x900")
#rootWindow.wm_attributes("-transparentcolor", 'grey')

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
canvas.create_text(812, 30, text="Movies", font="arial 25 bold", fill="white")
canvas.create_text(840, 200, text="Movie Info", font="arial 25 bold", fill="white")
canvas.create_rectangle(760,230, 1390, 780,fill=color4, outline="")


#create labels
errorLabel = tk.Label(rootWindow, text="No results, please check for typos", width=26, anchor="w", background="red",
                      foreground="white", font=("Arial", 12, "bold"))


actorsLabel = tk.Label(rootWindow, text="Actors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
genresLabel = tk.Label(rootWindow, text="Genres:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
durationLabel = tk.Label(rootWindow, text="Duration:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
releaseYearLabel = tk.Label(rootWindow, text="Release:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
directorsLabel = tk.Label(rootWindow, text="Directors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
producersLabel = tk.Label(rootWindow, text="Producers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
languagesLabel = tk.Label(rootWindow, text="Languages:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
writersLabel = tk.Label(rootWindow, text="Writers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
editorsLabel = tk.Label(rootWindow, text="Editors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
musicContributorsLabel = tk.Label(rootWindow, text="Composer:", width=10, anchor="w", foreground="white", background=color4, font=("Arial", 15, "bold"))

filterLabels = np.array([actorsLabel, genresLabel, durationLabel, releaseYearLabel, directorsLabel,producersLabel,
                         languagesLabel, writersLabel, editorsLabel, musicContributorsLabel])

actorsLabelInfo = tk.Label(rootWindow, text="Actors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
genresLabelInfo = tk.Label(rootWindow, text="Genres:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
durationLabelInfo = tk.Label(rootWindow, text="Duration:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
releaseYearLabelInfo = tk.Label(rootWindow, text="Release:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
directorsLabelInfo = tk.Label(rootWindow, text="Directors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
producersLabelInfo = tk.Label(rootWindow, text="Producers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
languagesLabelInfo = tk.Label(rootWindow, text="Languages:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
writersLabelInfo = tk.Label(rootWindow, text="Writers:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
editorsLabelInfo = tk.Label(rootWindow, text="Editors:", width=10, anchor="w", background=color4, foreground="white", font=("Arial", 15, "bold"))
musicContributorsLabelInfo = tk.Label(rootWindow, text="Composer:", width=10, anchor="w", foreground="white", background=color4, font=("Arial", 15, "bold"))

InfoLabels = np.array([actorsLabelInfo, genresLabelInfo, durationLabelInfo, releaseYearLabelInfo, directorsLabelInfo,
                       producersLabelInfo,languagesLabelInfo, writersLabelInfo, editorsLabelInfo,
                       musicContributorsLabelInfo])

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
                         clearDirectorButton , clearProducerButton, clearLanguageButton,clearWriterButton,
                         clearEditorButton, clearMusicContributorButton])


#create text fields
actorGenreInputText = tk.Text(rootWindow, height=1, width=72)
durationRealeaseInputText = tk.Text(rootWindow, height=1, width=54)

movieInfoText = tk.Text(rootWindow, height=33, width=78)

actorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
genresFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
durationFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
releaseYearFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
directorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
producersFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
languagesFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
writersFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
editorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")
musicContributorsFilters = tk.Text(rootWindow, height=2, width=54, state="disabled")

filterTexts = np.array([actorsFilters, genresFilters, durationFilters, releaseYearFilters, directorsFilters,
           producersFilters, languagesFilters, writersFilters, editorsFilters, musicContributorsFilters])

actorsInfo = tk.Text(rootWindow, height=5, width=54, state="disabled")
genresInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
durationInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
releaseYearInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
directorsInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
producersInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
languagesInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
writersInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
editorsInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")
musicContributorsInfo = tk.Text(rootWindow, height=1, width=54, state="disabled")

infoTexts = np.array([actorsInfo, genresInfo, durationInfo, releaseYearInfo, directorsInfo,producersInfo, languagesInfo,
                      writersInfo, editorsInfo, musicContributorsInfo])

for info in infoTexts:
    info.configure(background = color5, foreground = "white")

#create dropdown menus
movieOptions = []
movieMenu = ttk.Combobox(rootWindow, values=movieOptions, state="readonly", width=102)
movieMenu.set("Movie List")
movieMenu.bind("<<ComboboxSelected>>", movieSelection)
filterOptions = ["Actor", "Genre", "Duration", "Release", "Director", "Producer", "Language",
                 "Writer", "Editor", "Composer"]
filterMenu = ttk.Combobox(rootWindow, values=filterOptions, state="readonly", width=17)
filterMenu.set("Choose Filter")
filterMenu.bind("<<ComboboxSelected>>", filterSelection)
comparisonOptions = ["<", "<=", "=", "=>", ">"]
comparisonSignMenu = ttk.Combobox(rootWindow, values=comparisonOptions, state="readonly", width=17)
comparisonSignMenu.set("Comparator")
languageOptions = ["English", "Hindu", "French", "Spanish", "Japanese", "Tamil", "Italian", "German", "Korean",
                   "Russian"]
languageMenu = ttk.Combobox(rootWindow, values=languageOptions, state="readonly", width = 50)
languageMenu.set("Language")
genreOptions = ["Drama", "Black-and-white", "Indie", "Short film", "Silent film",  "Horror Film", "Thriller",
"Documentary", "Comedy", "Adventure", "Crime", "Science fiction", "Musical", "Action", "Western", "Romance Film",
"Family", "Biographical", "Romantic comedy", "Mystery", "Martial arts", "Film noir", "Fantasy", "Coming of age",
"Slasher", "Teen", "Children's", "Black comedy", "Anime", "Parody"]
genreMenu = ttk.Combobox(rootWindow, values=genreOptions, state="readonly", width = 50)
genreMenu.set("Genre")

#Selector for FuzzySearch
exactSearch = tk.BooleanVar()
fuzzySearch = tk.BooleanVar()
exactSearchSelector = tk.Checkbutton(rootWindow, text='Exact Search',variable=exactSearch, onvalue=True, offvalue=False,
                                     command=selectExactSearch, bg=color4, foreground="white",
                                     disabledforeground="white")
fuzzySearchSelector = tk.Checkbutton(rootWindow, text='Fuzzy Search',variable=fuzzySearch, onvalue=True, offvalue=False,
                                     command=selectFuzzySearch, background=color4, foreground="white",
                                     disabledforeground="white")
exactSearchSelector.select()
exactSearchSelector.configure(state="disabled")

#add content to grid
yPos = 240
for i in range(filterLabels.size):
    if i == 0:
        infoTexts[i].place(x=910, y=str(yPos))
        InfoLabels[i].place(x=770, y=str(yPos))
    else:
        infoTexts[i].place(x=910, y=str(yPos + 59))
        InfoLabels[i].place(x=770, y=str(yPos + 53))
    rectangle = canvas.create_rectangle(10,yPos, 136,yPos+36,fill=color4, outline="")
    filterLabels[i].place(x=10, y=str(yPos+3))
    filterTexts[i].place(x=150, y=str(yPos))
    clearButtons[i].place(x=600, y=str(yPos))
    yPos += 50

filterMenu.place(x=10, y=60)
addFilterButton.place(x=600, y=75)
searchButton.place(x=300, y=800)
movieMenu.place(x=760, y=60)
exactSearchSelector.place(x=485, y=800)
fuzzySearchSelector.place(x=485, y=836)
#movieInfoText.place(x=760, y=240)
#findMoreButton.place(x=1000, y=800)


#execute_query()


rootWindow.mainloop()