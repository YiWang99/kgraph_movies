import numpy as np
from movies import create_filter_dict, generate_query_in_brackets, generate_query_in_filter, MovieFilter, load_kg, execute_query
from movies import generate_query_movie_info, transfer_results_to_front_end


def test_create_filter_dict():
    # create actors, genres, runtime, initial_release_date, directors, producers, language, writers, editors, music_contributors, countries numpy arrays
    actor = np.array(["actor", "Dustin Hoffman"])
    genre = np.array(["genre", "Thriller"])
    runtime = np.array(["runtime", "< 300"])
    initial_release_date = np.array(["initial_release_date", ""])
    director = np.array(["director", ""])
    producer = np.array(["producer", ""])
    language = np.array(["language", ""])
    writer = np.array(["writer", ""])
    editor = np.array(["editor", ""])
    music_contributor = np.array(["music_contributor", ""])
    country = np.array(["country", ""])
    # create a dictionary from the numpy arrays
    filter_dict = create_filter_dict([actor, genre, runtime, initial_release_date, director, producer, 
                                      language, writer, editor, music_contributor, country])
    print(filter_dict)
    return filter_dict


def test_generate_query_in_brackets(filter_dict):
    q = generate_query_in_brackets(filter_dict)
    print(q)
    return q

def test_generate_query_in_filter(filter_dict):
    q = generate_query_in_filter(filter_dict)
    print(q)
    return q


def test_generate_query():
    fliter_dict = test_create_filter_dict()
    filter = MovieFilter(fliter_dict)
    q = filter.generate_query()
    return q

def test_generate_query_movie_info():
    # q = generate_query_movie_info("Buffy the Vampire Slayer")
    # q = generate_query_movie_info("Sphere")
    q = """
        SELECT DISTINCT ?movie_name ?actor_name ?genre_name ?runtime ?initial_release_date 
    ?director_name ?producer_name ?language ?writer_name ?editor_name ?music_contributor_name ?country_name
    WHERE{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{
            ?movie lmdb:actor ?actor .
            ?actor lmdb:actor_name ?actor_name .
        }
        OPTIONAL{
            ?movie lmdb:genre ?genre .
            ?genre lmdb:film_genre_name ?genre_name .
        }
        ?movie lmdb:runtime ?runtime .
        ?movie lmdb:initial_release_date ?initial_release_date .
        OPTIONAL{
            ?movie lmdb:director ?director .
            ?director lmdb:director_name ?director_name .
        }
        OPTIONAL{
            ?movie lmdb:producer ?producer .
            ?producer lmdb:producer_name ?producer_name .
        }
        ?movie lmdb:language ?language .
        OPTIONAL{
            ?movie lmdb:writer ?writer .
            ?writer lmdb:writer_name ?writer_name .
        }
        OPTIONAL{
            ?movie lmdb:editor ?editor .
            ?editor lmdb:editor_name ?editor_name .
        }
        OPTIONAL{
            ?movie lmdb:music_contributor ?music_contributor .
            ?music_contributor lmdb:music_contributor_name ?music_contributor_name .
        }
        OPTIONAL{
            ?movie lmdb:country ?country .
            ?country lmdb:country_name ?country_name .
        }
        FILTER(?movie_name = "Sphere")
    }
    GROUP BY ?movie_name ?actor_name ?genre_name ?runtime ?initial_release_date 
    ?director_name ?producer_name ?language ?writer_name ?editor_name ?music_contributor_name ?country_name
ORDER BY RAND()
LIMIT 1
    """
    print(q)
    return q


def test_filter():
    q  = test_generate_query()
    results = execute_query(load_kg("linkedmdb.nt"), q)
    transfer_results_to_front_end(results)

def test_info():
    # q = test_generate_query_movie_info()
    q = """
    SELECT DISTINCT ?movie_name ?actor_name ?genre_name ?runtime ?initial_release_date 
    ?director_name ?producer_name ?language ?writer_name ?editor_name ?music_contributor_name ?country_name
    WHERE{
        ?movie a lmdb:film ;
            dc:title ?movie_name .
        OPTIONAL{
            ?movie lmdb:actor ?actor .
            ?actor lmdb:actor_name ?actor_name .
        }
        OPTIONAL{
            ?movie lmdb:genre ?genre .
            ?genre lmdb:film_genre_name ?genre_name .
        }
        ?movie lmdb:runtime ?runtime .
        ?movie lmdb:initial_release_date ?initial_release_date .
        OPTIONAL{
            ?movie lmdb:director ?director .
            ?director lmdb:director_name ?director_name .
        }
        OPTIONAL{
            ?movie lmdb:producer ?producer .
            ?producer lmdb:producer_name ?producer_name .
        }
        ?movie lmdb:language ?language .
        OPTIONAL{
            ?movie lmdb:writer ?writer .
            ?writer lmdb:writer_name ?writer_name .
        }
        OPTIONAL{
            ?movie lmdb:editor ?editor .
            ?editor lmdb:editor_name ?editor_name .
        }
        OPTIONAL{
            ?movie lmdb:music_contributor ?music_contributor .
            ?music_contributor lmdb:music_contributor_name ?music_contributor_name .
        }
        OPTIONAL{
            ?movie lmdb:country ?country .
            ?country lmdb:country_name ?country_name .
        }
        FILTER(?movie_name = "Sphere")
    }
    GROUP BY ?movie_name ?actor_name ?genre_name ?runtime ?initial_release_date 
    ?director_name ?producer_name ?language ?writer_name ?editor_name ?music_contributor_name ?country_name
    """
    results = execute_query(load_kg("linkedmdb.nt"), q)
    print("results", results)
    print("results len", len(results))
    # transfer_results_to_front_end(results, result_types=["movie_name", "actor_name", "genre_name", "runtime",
    #                                                       "initial_release_date", "director_name", "producer_name", 
    #                                                       "language", "writer_name", "editor_name", 
    #                                                       "music_contributor_name", "country_name"])

if __name__ == "__main__":
    # fliter_dict = test_create_filter_dict()
    # print("Test_create_filter_dict passed.")
    # query_in_brackets = test_generate_query_in_brackets(fliter_dict)
    # print("Test_generate_query_in_brackets passed.")
    # query_in_where = test_generate_query_in_filter(fliter_dict)
    # print("Test_generate_query_in_filter passed.")
    # query_in_where = generate_query_in_where(fliter_dict)
    # print("Test_generate_query_in_where passed.")

    test_filter()
    
    test_info()

