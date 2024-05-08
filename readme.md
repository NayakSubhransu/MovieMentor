

<a name="readme-top"></a>
<div align="center">
  <h1>🎬 MovieMentor</h1>
  <h3>Movie Recommendation System</h3>
  <p>
    An intelligent system that harnesses the power of machine learning and natural language processing(NLP) to provide personalized movie recommendations tailored to individual preferences.
  </p>
  <img src="https://i0.wp.com/spotintelligence.com/wp-content/uploads/2023/11/content-based-recommendation-system.jpg?fit=1200%2C675&ssl=1" alt="Movie Recommendation System" width="800" height="400">
</div>

## 📽️ About:

This project aims to develop a cutting-edge movie recommendation system that leverages advanced techniques in data cleaning, exploratory data analysis (EDA), machine learning, and natural language processing (NLP). The system is designed to suggest movies to users based on their unique preferences, behavior, and the similarities between movies.
<br /><br />
The recommendation engine employs a content-based filtering approach, analyzing movie overviews, features, and user-item interactions to provide highly relevant and personalized recommendations. By combining machine learning algorithms with natural language processing techniques, the system can effectively understand and interpret user preferences, enabling it to suggest movies that align with their specific interests.
<br /><br />
See the implementation details with [IPython Notebook](https://github.com/NayakSubhransu/MovieMentor/blob/main/MovieMentor.ipynb).


## 🌟 Key Features

💡 Content-Based Filtering Algorithm: MovieMentor employs a cutting-edge content-based filtering algorithm that analyzes movie overviews, features, and metadata to identify similarities between movies and your preferences.<br />
🗜️ Cosine Similarity and Vectorization: The system implements advanced cosine similarity calculations and vectorization techniques to accurately measure the similarity between textual documents, such as movie overviews and user reviews.<br />
👥 Collaborative Filtering: In addition to content-based filtering, MovieMentor utilizes user-based and item-based collaborative filtering techniques to enhance recommendation accuracy by incorporating user-item interactions and preferences.<br />
🎯 Personalized Recommendations: You'll receive tailored movie suggestions based on your unique preferences, behavior, and the similarities between movies, ensuring a highly personalized and relevant recommendation experience.<br />

## 📁 Datasets
MovieMentor relies on a comprehensive movie dataset containing rich information about movie features, overviews, credits, and ratings. This dataset undergoes thorough preprocessing to extract relevant features, ensuring that the recommendation algorithms have access to high-quality data for training and evaluation.

## 🚀 Getting Started:

To set up the Movie Recommendation System on your local machine, follow these step-by-step instructions:

### 📋 Prerequisites:

Before proceeding, ensure that you have the following software installed:

- [Python](https://www.python.org/downloads/) (version 3.10 or higher)
- [Anaconda](https://www.anaconda.com/products/distribution) or [venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) (for creating a virtual environment)
- [Git](https://git-scm.com/downloads) (for cloning the repository)

### 🛠️ Installations:

1. **Clone the Repository**

   ```sh
   git clone https://github.com/NayakSubhransu/MovieMentor.git
   ```

2. **Change the Working Directory**

   ```sh
   cd MovieMentor
   ```

3. **Create and Activate a Virtual Environment**

   It's highly recommended to create a virtual environment to maintain a clean and isolated setup for the project dependencies.

   - For Anaconda:

     ```sh
     conda create -n env_name python=3.10
     conda activate env_name
     ```

   - For venv:
     - Windows:
       ```sh
       py -3 -m venv venv
       venv\Scripts\activate
       ```
     - macOS/Linux:
       ```sh
       python3 -m venv venv
       source venv/bin/activate
       ```

4. **Install Required Packages**

   ```sh
   python -m pip install -r requirements.txt
   ```

   This command will install all the necessary packages and dependencies specified in the `requirements.txt` file.

5. **Run the Web Application**

   ```sh
   streamlit run app.py
   ```

   This command will start the Streamlit web application, and you should see a URL in your terminal. Copy and paste this URL into your web browser to access the Movie Recommendation System.

### 💻 Running the Application on CLI

In addition to the web application, you can also run the Movie Recommendation System through the command-line interface (CLI). To do so, follow these steps:

1. **Install Required Packages**

2. **See the Movie List**

   ```sh
   python MovieMentor_cli.py --movie list --page_number 2  # Default page number is 2
   ```

   This command will display a list of movies from the dataset. You can specify the page number using the `--page_number` option (default is 2).

3. **Get Movie Recommendations**

   ```sh
   python MovieMentor_cli.py --movie "YourMovieTitle" --num_recommendations 5  # Default number of recommendations is 5
   ```

   Replace `"YourMovieTitle"` with the title of a movie you're interested in, and the system will provide the top 5 movie recommendations based on your selection. You can adjust the number of recommendations using the `--num_recommendations` option (default is 5).


## 📚 Requirement Packages:

The following packages and libraries are required to run the Movie Recommendation System:

- Jupyter Notebook
- Pandas
- pillow
- NLTK (Natural Language Toolkit)
- Scikit-learn
- Pickle
- Streamlit
- streamlit_lottie
- colorama
- requests
- rich
- pyfiglet

These dependencies are automatically installed when running the `python -m pip install -r requirements.txt` command during the installation process.

## 🖥️ Web Application
The MovieMentor web application provides a user-friendly interface for discovering and exploring movie recommendations. Users can input their preferences, and the application will generate personalized recommendations based on their choices.

<div align="center">
<img src="https://github.com/NayakSubhransu/MovieMentor/assets/139241744/9935bf2c-f134-4419-a22d-0609bd5c8f93" width="800" height="500">
</div>

<div align="center">
<img src="https://github.com/NayakSubhransu/MovieMentor/assets/139241744/7c396b5f-c7e4-4046-a215-236bbc6d1725" width="800" height="500">
</div>

<div align="center">
<img src="https://github.com/NayakSubhransu/MovieMentor/assets/139241744/5bcce2ce-dc29-4b7b-a7bb-a1cdcc65e1fa
" width="800" height="500">
</div>

<div align="center">
<img src="https://github.com/NayakSubhransu/MovieMentor/assets/139241744/3bfcb6e3-5c77-44a9-8080-7b80c71e7df9" width="800" height="500">
</div>

## 💻 CLI Application
For quick and convenient recommendations, the MovieMentor CLI application allows users to input movie titles directly from the terminal and receive personalized recommendations instantly.

<div align="center">
<img src="https://raw.githubusercontent.com/NayakSubhransu/MovieMentor/main/assets/cli-app-screenshot.png" width="800" height="500">
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/NayakSubhransu/MovieMentor/main/assets/web-app-screenshot.png" width="800" height="500">
</div>


## 🏆 Usage
MovieMentor can be utilized by both new and existing users to receive personalized movie recommendations:

🎯 User Preferences: Input your movie preferences, such as genres, actors, directors, or specific movie titles you enjoy.<br />
📊 Historical Data: MovieMentor leverages historical data, including user-item interactions and movie metadata, to identify patterns and similarities.<br />
🎥 Recommendation Generation: Based on your preferences and the analyzed data, the system generates a list of recommended movies tailored to your unique interests and tastes.<br />
🔍 Exploration and Feedback: Explore the recommended movies, provide feedback, and refine your preferences for even more accurate recommendations in the future.<br />

## 🌟 Future Improvements
MovieMentor has several potential areas for future improvements and enhancements:

🧠 **Deep Learning Models:** Incorporate advanced deep learning models, such as neural networks or transformers, to further improve recommendation accuracy and handle more complex data patterns.<br />
🎨 **User Interface Enhancements:** Develop a more intuitive and user-friendly interface to enhance the overall user experience, making it easier for users to input their preferences and explore recommendations.<br />
📂 **Additional Data Sources:** Integrate additional data sources, such as user reviews, ratings, and social media data, to enhance the system's understanding of user preferences and movie characteristics.<br />
🔀 **Hybrid Recommendation Approach:** Explore a hybrid recommendation approach that combines content-based filtering, collaborative filtering, and other advanced techniques to leverage the strengths of multiple algorithms and provide more robust recommendations.<br />
⏱️ **Real-Time Updates:** Implement mechanisms to continuously update the recommendation models with new data, ensuring that the system remains up-to-date and can adapt to changing user preferences and movie releases.<br />

## 🤝 Contributing
Contributions to MovieMentor are highly appreciated and welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please follow these steps:

 🍴 **Fork the Repository:** Start by forking the MovieMentor repository on GitHub.<br />
🌱 **Create a Branch:** Create a new branch for your feature or bug fix by running git checkout -b feature/your-feature-name or git checkout -b fix/your-fix-name. <br />
✨ **Make Changes:** Implement your changes, following best coding practices and ensuring that your code is well-documented and tested.<br />
🔖 **Commit and Push:** Commit your changes with descriptive commit messages and push them to your forked repository.<br />
🔍 **Submit a Pull Request:** Open a new Pull Request on the original repository, providing a detailed description of your changes.<br />

## 📚 Additional Resources:

The documentation also includes references to external resources, such as research papers, blog posts, and online tutorials, that provide further insights into the techniques and technologies used in the Movie Recommendation System.

## 🙏 Acknowledgements:

The Movie Recommendation System project would not have been possible without the contributions and support of the following individuals and organizations:

- Open-Source Community: I extend my gratitude to the open-source community for providing invaluable resources, libraries, and tools that facilitated the development of this project.
- Research Community: I acknowledge the researchers and academics whose work in the fields of machine learning, natural language processing, and recommender systems laid the foundation for the techniques employed in this project.
- Data Providers: I thank the organizations and individuals who curated and made available the movie datasets used in training and evaluating the recommendation system.



<p align="right">(<a href="#readme-top">back to top</a>)</p>
