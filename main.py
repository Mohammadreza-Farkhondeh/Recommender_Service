from .recommender import *







# Load data
user_trading_history = pd.read_csv('user_trading_history.csv')
crypto_features = pd.read_csv('crypto_features.csv')

# Collaborative Filtering
similar_users = find_similar_users(user_trading_history)
collaborative_recommendations = recommend_from_similar_users(similar_users, user_trading_history)

# Content-Based Filtering
similar_cryptos = find_similar_cryptos(crypto_features)
content_recommendations = recommend_similar_cryptos(similar_cryptos, user_trading_history)

# Hybrid Filtering
hybrid_recommendations = combine_recommendations(collaborative_recommendations, content_recommendations, alpha=0.5)

# Evaluation and Refinement
evaluate_recommendations(hybrid_recommendations)