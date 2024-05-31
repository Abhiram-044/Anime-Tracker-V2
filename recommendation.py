import pandas as pd
import numpy as np
import h5py
from tabulate import tabulate
import warnings
import pickle

warnings.simplefilter('ignore')

def extract_weights(file_path, layer_name):
    with h5py.File(file_path, 'r') as h5_file:
        if layer_name in h5_file:
            weight_layer = h5_file[layer_name]
            if isinstance(weight_layer, h5py.Dataset):
                weights = weight_layer[()]
                weights = weights / np.linalg.norm(weights, axis=1).reshape((-1, 1))
                return weights
            
    raise KeyError(f"Unable to find weights for layer '{layer_name} in the HDF5 file. ")

file_path = 'models/myanimeweights.h5'

def find_similar_animes(name, n=10):
    anime_weights = extract_weights(file_path, 'anime_embedding/anime_embedding/embeddings:0')

    with open('models/anime_encoder.pkl', 'rb') as file:
        anime_encoder = pickle.load(file)

    with open('models/anime-dataset-2023.pkl', 'rb') as file:
        df_anime = pickle.load(file)

    df_anime = df_anime.replace("UNKNOWN", "")

    anime_row = df_anime[df_anime['Name'] == name].iloc[0]
    index = anime_row['anime_id']

    encoded_index = anime_encoder.transform([index])[0]

    weights = anime_weights
    dists = np.dot(weights, weights[encoded_index])
    sorted_dists = np.argsort(dists)
    n = n + 1
    closest = sorted_dists[-n:]
    SimilarityArr = []
    id = 11

    for close in closest:
        id = id - 1
        decoded_id = anime_encoder.inverse_transform([close])[0]
        anime_frame = df_anime[df_anime['anime_id'] == decoded_id]
        anime_name = anime_frame['Name'].values[0]
        image_link = anime_frame['Image URL'].values[0]
        similarity = dists[close]
        similarity = "{:.2f}%".format(similarity * 100)
        score = float(anime_frame['Score'].values[0])
        
        if anime_name != name:
            SimilarityArr.append(
                {
                    "id": id,
                    "image": image_link,
                    "title": anime_name,
                    "similarity": similarity,
                    "rating": score,
                }
            )
    SimilarityArr = list(reversed(SimilarityArr))

    return SimilarityArr