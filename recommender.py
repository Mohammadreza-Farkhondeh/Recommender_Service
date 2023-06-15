# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

target_user = 1


# Function to find similar users based on trading history
def find_similar_users(user_trading_history):
    # Compute similarity between users using cosine similarity
    user_similarity = cosine_similarity(user_trading_history)
    # Find users with highest similarities to target user
    similar_users = np.argsort(user_similarity[target_user])[:-11:-1]
    return similar_users


# Function to recommend cryptocurrencies based on similar users' trading history
def recommend_from_similar_users(similar_users, user_trading_history):
    # Calculate distances between the target user and similar users
    distances = []
    for user in similar_users:
        distance = np.linalg.norm(user_trading_history.iloc[target_user] - user_trading_history.iloc[user])
        distances.append(distance)
    # Find most similar user and recommend their highest-valued trades
    most_similar_user = similar_users[np.argmin(distances)]
    recommendations = []
    for crypto in user_trading_history.columns[1:]:
        if user_trading_history.loc[most_similar_user, crypto] > user_trading_history.loc[-1, crypto]:
            recommendations.append(crypto)
    return recommendations


# Function to find similar cryptocurrencies based on features
def find_similar_cryptos(crypto_features):
    # Compute similarity between cryptocurrencies using cosine similarity
    crypto_similarity = cosine_similarity(crypto_features.drop('crypto_id', axis=1))
    # Find cryptocurrencies with the highest similarities to target user's trading history
    similar_cryptos = np.argsort(crypto_similarity[target_user])[:-11:-1]
    return similar_cryptos


# Function to recommend cryptocurrencies based on similar cryptocurrencies
def recommend_similar_cryptos(similar_cryptos, user_trading_history):
    # Find similar cryptocurrencies that the target user hasn't traded recently
    recommendations = []
    for crypto in similar_cryptos:
        if user_trading_history.loc[target_user, crypto] == 0:
            recommendations.append(crypto)
    return recommendations


# Function to combine recommendations from collaborative and content-based filtering
def combine_recommendations(collaborative_recommendations, content_recommendations, alpha):
    # Combine recommendations using weighted average
    hybrid_recommendations = {}
    for crypto in collaborative_recommendations:
        hybrid_recommendations[crypto] = alpha * collaborative_recommendations[crypto]
    for crypto in content_recommendations:
        if crypto in hybrid_recommendations:
            hybrid_recommendations[crypto] += (1 - alpha) * content_recommendations[crypto]
        else:
            hybrid_recommendations[crypto] = (1 - alpha) * content_recommendations[crypto]
    return hybrid_recommendations


# Function to evaluate and refine recommendations
def evaluate_recommendations(recommendations):
    # Evaluate accuracy and usefulness of recommendations using metrics such as precision, recall, and diversity
    # Refine the system based on feedback and performance data
    # For example, we might use the following code to compute the precision and recall of the recommendations:
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for crypto in recommendations:
        if user_trading_history.loc[target_user, crypto] > 0:
            true_positives += 1
        else:
            false_positives += 1
    for crypto in user_trading_history.columns[1:]:
        if user_trading_history.loc[target_user, crypto] > 0 and crypto not in recommendations:
            false_negatives += 1
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    print('Precision:', precision)
    print('Recall:', recall)
    # We can use these metrics to evaluate the performance of the system and identify areas for improvement.
    # For example, if the precision is low, we might need to improve the similarity metric or add more features to the content-based filtering step.
    # If the recall is low, we might need to adjust the weighting parameter alpha in the hybrid filtering step or use a different combination approach.

#
#
#
#
#
# # Import necessary libraries
# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
#
#
# # Function to find similar users based on trading history
# def find_similar_users(user_trading_history):
#     # Compute similarity between users using cosine similarity
#     user_similarity = cosine_similarity(user_trading_history)
#     # Find users with highest similarities to target user
#     similar_users = np.argsort(user_similarity)[-10:]
#     return similar_users
#
# # Function to recommend cryptocurrencies based on similar users' trading history
# def recommend_from_similar_users(similar_users, user_trading_history):
#     # Find cryptocurrencies that similar users have traded but target user hasn't
#     recommendations = []
#     for user in similar_users:
#         user_history = user_trading_history.iloc[user]
#         for crypto in user_history.index:
#             if user_history[crypto] == 1 and user_trading_history.loc[target_user, crypto] == 0:
#                 recommendations.append(crypto)
#     return recommendations
#
# # Function to find similar cryptocurrencies based on features
# def find_similar_cryptos(crypto_features):
#     # Compute similarity between cryptocurrencies using cosine similarity
#     crypto_similarity = cosine_similarity(crypto_features.drop('crypto_id', axis=1))
#     # Find cryptocurrencies with highest similarities to target user's trading history
#     similar_cryptos = np.argsort(crypto_similarity[target_user])[-10:]
#     return similar_cryptos
#
# # Function to recommend cryptocurrencies based on similar cryptocurrencies
# def recommend_similar_cryptos(similar_cryptos, user_trading_history):
#     # Find similar cryptocurrencies that the target user hasn't traded recently
#     recommendations = []
#     for crypto in similar_cryptos:
#         if user_trading_history.loc[target_user, crypto] == 0:
#             recommendations.append(crypto)
#     return recommendations
#
# # Function to combine recommendations from collaborative and content-based filtering
# def combine_recommendations(collaborative_recommendations, content_recommendations, alpha):
#     # Combine recommendations using weighted average
#     hybrid_recommendations = {}
#     for crypto in collaborative_recommendations:
#         hybrid_recommendations[crypto] = alpha * collaborative_recommendations[crypto]
#     for crypto in content_recommendations:
#         if crypto in hybrid_recommendations:
#             hybrid_recommendations[crypto] += (1 - alpha) * content_recommendations[crypto]
#         else:
#             hybrid_recommendations[crypto] = (1 - alpha) * content_recommendations[crypto]
#     return hybrid_recommendations
#
#
# # Function to evaluate and refine recommendations
# def evaluate_recommendations(recommendations):
#     # Evaluate accuracy and usefulness of recommendations using metrics such as precision, recall, and diversity
#     # Refine the system based on feedback and performance data
#     # For example, we might use the following code to compute the precision and recall of the recommendations:
#     true_positives = 0
#     false_positives = 0
#     false_negatives = 0
#     for crypto in recommendations:
#         if user_trading_history.loc[target_user, crypto] > 0:
#             true_positives += 1
#         else:
#             false_positives += 1
#     for crypto in user_trading_history.columns[1:]:
#         if user_trading_history.loc[target_user, crypto] > 0 and crypto not in recommendations:
#             false_negatives += 1
#     precision = true_positives / (true_positives + false_positives)
#     recall = true_positives / (true_positives + false_negatives)
#     print('Precision:', precision)
#     print('Recall:', recall)
#     # We can use these metrics to evaluate the performance of the system and identify areas for improvement.
#     # For example, if the precision is low, we might need to improve the similarity metric or add more features to the content-based filtering step.
#     # If the recall is low, we might need to adjust the weighting parameter alpha in the hybrid filtering step or use a different combination approach.
#
#
# # Load data
# user_trading_history = pd.read_csv('user_trading_history.csv')
# crypto_features = pd.read_csv('crypto_features.csv')
#
# # Collaborative Filtering
# similar_users = find_similar_users(user_trading_history)
# collaborative_recommendations = recommend_from_similar_users(similar_users, user_trading_history)
#
# # Content-Based Filtering
# similar_cryptos = find_similar_cryptos(crypto_features)
# content_recommendations = recommend_similar_cryptos(similar_cryptos, user_trading_history)
#
# # Hybrid Filtering
# hybrid_recommendations = combine_recommendations(collaborative_recommendations, content_recommendations, alpha=0.5)
#
# # Evaluation and Refinement
# evaluate_recommendations(hybrid_recommendations)
