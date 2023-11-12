from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import time

lmdb = Namespace("http://data.linkedmdb.org/movie/")
initNs = {
            "foaf": "http://xmlns.com/foaf/0.1/", 
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", 
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#", 
            "lmdb": lmdb, 
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

def generate_query_in_filter(filter_dict):
    q = ""
    for key, values in filter_dict.items():
        if values[0] == "":
            print("No value for key:", key)
            continue
        if key in ["actor", "genre", "director", "producer", "writer", "editor", "music_contributor"]:
            for index, value in enumerate(values):
                q += f"FILTER (?{key}_name{index} = \"{value}\") ."
        else:
            if key in ["runtime", "initial_release_date"]:
                q += f"FILTER (?{key}_int {values[0]}) ."
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
    print(q)      
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


    def generate_query(self):
        query = """
        SELECT DISTINCT ?movie_name
            WHERE {{{}}}LIMIT 100
        """.format(generate_query_in_where(self.__dict__))
        print(query)
        return query
        

def generate_query_movie_info(movie_name):
    q =f"""
    SELECT DISTINCT ?movie_name ?actor_name ?genre_name ?runtime ?initial_release_date 
    ?director_name ?producer_name ?language ?writer_name ?editor_name ?music_contributor_name ?country_name
    WHERE{{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{{
            ?movie lmdb:actor ?actor .
            ?actor lmdb:actor_name ?actor_name .
        }}
        OPTIONAL{{
            ?movie lmdb:genre ?genre .
            ?genre lmdb:film_genre_name ?genre_name .
        }}
        ?movie lmdb:runtime ?runtime .
        ?movie lmdb:initial_release_date ?initial_release_date .
        OPTIONAL{{
            ?movie lmdb:director ?director .
            ?director lmdb:director_name ?director_name .
        }}
        OPTIONAL{{
            ?movie lmdb:producer ?producer .
            ?producer lmdb:producer_name ?producer_name .
        }}
        ?movie lmdb:language ?language .
        OPTIONAL{{
            ?movie lmdb:writer ?writer .
            ?writer lmdb:writer_name ?writer_name .
        }}
        OPTIONAL{{
            ?movie lmdb:editor ?editor .
            ?editor lmdb:editor_name ?editor_name .
        }}
        OPTIONAL{{
            ?movie lmdb:music_contributor ?music_contributor .
            ?music_contributor lmdb:music_contributor_name ?music_contributor_name .
        }}
        OPTIONAL{{
            ?movie lmdb:country ?country .
            ?country lmdb:country_name ?country_name .
        }}
        FILTER(?movie_name = "{movie_name}")
    }}
    GROUP BY ?movie_name ?actor_name ?genre_name ?runtime ?initial_release_date 
    ?director_name ?producer_name ?language ?writer_name ?editor_name ?music_contributor_name ?country_name
    """
    return q



def execute_query(g, query):
    # execute a query
    start_time = time.time()
    query = prepareQuery(query, initNs=initNs)
    results = g.query(query)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"query execution time: {execution_time}s")
    return results


def transfer_results_to_front_end(results, result_types=["movie_name"]):
    # transfer the results to a list that can be sent to the front end
    print("transfer the results to a list that can be sent to the front end")
    # first_result = next(results, None)
    # print(first_result)
    # for row in results:
    #     print(row)
    results_list = []
    # print(len(results))
    # print(results)
    try:
        for index, result in enumerate(results):
            for result_type in result_types:
                results_list.append({index: result[result_type].value})  
    except Exception as e:
        print("No results found.", e)
    print(results_list)
    return results_list
            



if __name__ == "__main__":
    # g = load_kg("linkedmdb.nt")
    pass