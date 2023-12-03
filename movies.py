from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import time
import numpy as np

lmdb = Namespace("http://data.linkedmdb.org/movie/")
lingvo = Namespace("http://www.lingvoj.org/lingvo/")
initNs = {
            "foaf": "http://xmlns.com/foaf/0.1/", 
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", 
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#", 
            "lmdb": lmdb, 
            "lingvo": lingvo,
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "dc": "http://purl.org/dc/terms/"
          }

def load_kg(file, format='nt'):
    # load a knowledge graph from a file
    print("start loading")
    start_time = time.time()
    g=Graph().parse(file, format=format)
    print("graph loaded")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"loading execution time: {execution_time}s")
    if len(g) > 0:
        print("RDF loaded.")
    else:
        print("RDF load failed.")
    print(f"load {len(g)} triples.")
    return g

def create_filter_dict(front_end_list:list):
    # create a dictionary from the front end
    # front_end_dict: a dictionary from the front end
    # return: a dictionary that can be used for query
    filter_dict = {}
    for row in front_end_list:
        filter_dict.update({row[0]:row[1:]}) 
    return filter_dict

def generate_query_in_brackets(filter_dict):
    q = "[a lmdb:film; dc:title ?movie_name;"
    for key, values in filter_dict.items():
        if values[0] == "":
            continue
        if key in ["actor", "genre", "director", "producer", "writer", "editor", "music_contributor"]:
            for index, _ in enumerate(values):
                    q += f" lmdb:{key} ?{key}{index}; "
        else:
            q += f" lmdb:{key} ?{key} ;"
    q += "] ."
    return q

def generate_query_in_brackets_full_name(filter_dict):
    q = """
        ?film a lmdb:film ;
            dc:title ?movie_name ;
    """
    for key, values in filter_dict.items():
        if values[0] == "":
            continue
        if key in ["actor", "genre", "director", "producer", "writer", "editor", "music_contributor"]:
            for _, value in enumerate(values):
                q += f"lmdb:{key} [lmdb:{key}_name \"{value}\"] ;"
        else:
            q += f" lmdb:{key} ?{key} ;"
    return q

def generate_query_in_filter(filter_dict):
    q = ""
    for key, values in filter_dict.items():
        if values[0] == "":
            print("No value for key:", key)
            continue
        if key in ["actor", "genre", "director", "producer", "writer", "editor", "music_contributor"]:
            for index, value in enumerate(values):
                # q += f"FILTER (?{key}_name{index} = \"{value}\") ."
                q += f"FILTER (STRSTARTS(?{key}_name{index}, \"{value}\")) ."
        elif key == "runtime":
            # maybe multiple values of runtime
            for value in values:
                q += f"FILTER (?{key}_int {value}) ."
        elif key == "initial_release_date":
            q += f"FILTER (?{key}_int {values[0]}) ."
        elif key == "language":
            q += f"""
                    BIND(STRAFTER(str(?language), "http://www.lingvoj.org/lingvo/") AS ?languageCode)
                    FILTER(?languageCode = "{values[0]}")"""
        else:
            q += f"FILTER (?{key} = \"{values[0]}\") ."

    return q


def generate_query_in_filter_full_name(filter_dict):
    q = ""
    for key, values in filter_dict.items():
        if values[0] == "":
            print("No value for key:", key)
            continue
        if key in ["actor", "genre", "director", "producer", "writer", "editor", "music_contributor"]:
            continue
        if key == "runtime" or key == "initial_release_date":
            if key == "runtime":
                q += f"BIND(xsd:integer(?{key}) AS ?{key}_int) ."
            if key == "initial_release_date":
                q += f"BIND(STRDT(SUBSTR(?{key}, 1, 4), xsd:integer) AS ?{key}_int) ."
            # maybe multiple values of runtime
            q += f"FILTER ("
            for value in values:
                q += f"?{key}_int {value} && "
            q = q[:-3] + ") ."
        elif key == "language":
            q += f"FILTER(STRAFTER(str(?language), \"http://www.lingvoj.org/lingvo/\") = \"{values[0]}\")"
        else:
            q += f"FILTER (?{key} = \"{values[0]}\") ."
    return q


def generate_query_in_where(filter_dict):
    query_in_brackets = generate_query_in_brackets(filter_dict)
    query_in_filter = generate_query_in_filter(filter_dict)
    q = query_in_brackets
    for key, values in filter_dict.items():
        if values[0] == "":
            continue
        if key in ["actor", "genre", "director", "producer", "writer", "editor", "music_contributor"]:
            for index, value in enumerate(values):
                if key == "genre":
                    q += f"?{key}{index} lmdb:film_genre_name  ?{key}_name{index} ."
                else:
                    q += f"?{key}{index} lmdb:{key}_name  ?{key}_name{index} ."
    if filter_dict.get("runtime")[0] != "":
        q += "BIND(xsd:integer(?runtime) AS ?runtime_int) . "
    if filter_dict.get("initial_release_date")[0] != "":
        q += "BIND(STRDT(SUBSTR(?initial_release_date, 1, 4), xsd:integer) AS ?initial_release_date_int) ."         
    q += query_in_filter 
    return q

def generate_query_in_where_full_name(filter_dict):
    q = generate_query_in_brackets_full_name(filter_dict)      
    q += generate_query_in_filter_full_name(filter_dict)
    return q

class MovieFilter:
    """
    filter movies based on the given criteria: 
    actors, genres, runtime, initial_release_date, directors, producers, language, writers, editors, music_contributors, countries
    """
    def __init__(self, filter_dict):
        self.actor = filter_dict.get("actor")
        self.genre = filter_dict.get("genre")
        self.runtime = filter_dict.get("runtime")
        self.initial_release_date = filter_dict.get("initial_release_date")
        self.director = filter_dict.get("director")
        self.producer = filter_dict.get("producer")
        self.language = filter_dict.get("language")
        self.writer = filter_dict.get("writer")
        self.editor = filter_dict.get("editor")
        self.music_contributor = filter_dict.get("music_contributor")
        self.country = filter_dict.get("country")

    def display_filter(self):
        print("Movie filters:")
        print("actor:", self.actor)
        print("genre:", self.genre)
        print("runtime:", self.runtime)
        print("initial_release_date:", self.initial_release_date)
        print("director:", self.director)
        print("producer:", self.producer)
        print("language:", self.language)
        print("writer:", self.writer)
        print("editor:", self.editor)
        print("music_contributor:", self.music_contributor)
        print("country:", self.country)


    def generate_query(self, limit=100, full_name_only=True):
        if full_name_only:
            generate_query_in_where_clause = generate_query_in_where_full_name(self.__dict__)
        else:
            generate_query_in_where_clause = generate_query_in_where(self.__dict__)
        query = """
        SELECT DISTINCT ?movie_name
            WHERE {{{}}}LIMIT {}
        """.format(generate_query_in_where_clause, limit)
        print(query)
        return query
        

def generate_query_movie_info(movie_name):
    q0 = f"""
    SELECT DISTINCT ?actor_name 
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:actor ?actor .
            ?actor lmdb:actor_name ?actor_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """
    q1 = f"""
    SELECT DISTINCT ?genre_name 
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:genre ?genre .
            ?genre lmdb:film_genre_name ?genre_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """
    q2 = f"""
    SELECT DISTINCT ?runtime
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        ?movie lmdb:runtime ?runtime .
        FILTER(?movie_name = "{movie_name}")
    }}
    """
    
    q3 = f"""
    SELECT DISTINCT ?initial_release_date 
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        
        ?movie lmdb:initial_release_date ?initial_release_date .
        FILTER(?movie_name = "{movie_name}")
    }}
    """

    q4 = f"""
    SELECT DISTINCT ?director_name 
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:director ?director .
            ?director lmdb:director_name ?director_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """

    q5 = f"""
    SELECT DISTINCT ?producer_name
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:producer ?producer .
            ?producer lmdb:producer_name ?producer_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """
    q6 = f"""
    SELECT DISTINCT ?languageCode
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        ?movie lmdb:language ?language .
        BIND(STRAFTER(str(?language), "http://www.lingvoj.org/lingvo/") AS ?languageCode)
        FILTER(?movie_name = "{movie_name}")
    }}
    """
    q7 = f"""
    SELECT DISTINCT ?writer_name 
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:writer ?writer .
            ?writer lmdb:writer_name ?writer_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """

    q8 = f"""
    SELECT DISTINCT ?editor_name
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:editor ?editor .
            ?editor lmdb:editor_name ?editor_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """

    q9 = f"""
    SELECT DISTINCT ?music_contributor_name
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:music_contributor ?music_contributor .
            ?music_contributor lmdb:music_contributor_name ?music_contributor_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """

    q10 = f"""
    SELECT DISTINCT ?country_name
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:country ?country .
            ?country lmdb:country_name ?country_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    """
    return [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]



def execute_query(g, query):
    # execute a query
    start_time = time.time()
    query = prepareQuery(query, initNs=initNs)
    results = g.query(query)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"query execution time: {execution_time}s")
    print(f"query results: {results}")
    return results




def transfer_results_to_front_end(results, result_types):
    # transfer the results to a list that can be sent to the front end
    print("transfer results to front end ------")
    results_list = {}
    for result_type in result_types:
        results_list[result_type] = []
    try:
        for _, result in enumerate(results):
            for result_type in result_types:
                value = result[result_type].value
                if value not in results_list[result_type]:
                    results_list[result_type].append(value)
    except Exception as e:
        print("No results found.", e)
    return results_list




# There are three acitvate functions: 1) for loading graph 2) for filtering 3) for getting movie info
def activate_initial():         
    g = load_kg("linkedmdb.nt")
    return g


def activate_filter(front_end_filter_list, g, limit, full_name_only):
    filter_dict = create_filter_dict(front_end_filter_list)
    filter = MovieFilter(filter_dict)
    filter.display_filter()
    filter_query = filter.generate_query(limit=limit, full_name_only=full_name_only)
    print(len(g))
    results = execute_query(g, filter_query)
    filter_results = transfer_results_to_front_end(results, result_types=["movie_name"])
    print(filter_results)
    return filter_results

def activate_info(front_end_movie_name, g):
    info_query = generate_query_movie_info(front_end_movie_name)
    print(info_query)
    result_types=["actor_name", "genre_name", "runtime", "initial_release_date", 
                  "director_name", "producer_name", "languageCode", "writer_name", "editor_name", 
                  "music_contributor_name", "country_name"]
    info_result = {}
    start_time = time.time()
    for index, query in enumerate(info_query):
        results = execute_query(g, query)
        results_dict = transfer_results_to_front_end(results, result_types=[result_types[index]])
        info_result.update(results_dict)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"whole query execution time: {execution_time}s")
    print(info_result)
    return info_result


if __name__ == "__main__":
    g = activate_initial()
    # create actors, genres, runtime, initial_release_date, directors, producers, language, writers, editors, music_contributors, countries numpy arrays
    actor = np.array(["actor", "Daniel Radcliffe", "Emma Watson"])
    genre = np.array(["genre", ""])
    runtime = np.array(["runtime", "<= 150"])
    initial_release_date = np.array(["initial_release_date", "< 2015"])
    director = np.array(["director", ""])
    producer = np.array(["producer", ""])
    language = np.array(["language", "en"])
    writer = np.array(["writer", ""])
    editor = np.array(["editor", ""])
    music_contributor = np.array(["music_contributor", ""])
    country = np.array(["country", ""])
    front_end_list =[actor, genre, runtime, initial_release_date, director, producer, language, writer, editor, music_contributor, country]
    
    activate_filter(front_end_list, g, 100, True)

    # activate_info("Harry Potter and the Prisoner of Azkaban", g)

