import pickle
import requests
import argparse
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress
from pyfiglet import Figlet
import sys
import time

console = Console()

def fetch_poster(movie_id, progress):
    """
    Fetches movie poster and overview from API.

    Args:
        movie_id (int): The ID of the movie.
        progress (Progress): The progress bar to track the fetching progress.

    Returns:
        tuple: A tuple containing the full path of the movie poster and the movie overview.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    task = progress.add_task(f"Fetching movie poster for {movie_id}", total=1)
    while not progress.finished:
        try:
            data = requests.get(url).json()
            poster_path = data['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            progress.update(task, advance=1)
            return full_path, data['overview']
        except requests.exceptions.RequestException as e:
            progress.log(f"Error: {e}")
            time.sleep(1)

def list_all_movies(page_size=800, page_number=1):
    """
    Lists all movies.

    Args:
        page_size (int, optional): The number of movies to display per page. Defaults to 800.
        page_number (int, optional): The page number to display. Defaults to 1.
    """
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size

    table = Table(show_header=True, header_style="bold magenta", title=f"List of Movies (Page {page_number})", box=box.DOUBLE)
    table.add_column("Index", style="dim", justify="right")
    table.add_column("Title", style="bold yellow")

    for i, title in enumerate(movies['title'][start_index:end_index], start=start_index + 1):
        table.add_row(str(i), title)

    console.print(table)

def recommend(movie, num_recommendations=5):
    """
    Recommends movies based on similarity.

    Args:
        movie (str): The title of the movie.
        num_recommendations (int, optional): The number of recommendations to show. Defaults to 5.

    Returns:
        list: A list of dictionaries containing the recommended movie details.
    """
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        raise ValueError(f"[red]Error:[/red] Movie '{movie}' not found in the database.")

    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movie_data = []
    with Progress(console=console, transient=True) as progress:
        for i in distances[1:num_recommendations + 1]:
            movie_id = movies.iloc[i[0]].movie_id
            movie_title = movies.iloc[i[0]].title
            poster_path, overview = fetch_poster(movie_id, progress)
            recommended_movie_data.append({
                'title': movie_title,
                'poster': poster_path,
                'overview': overview
            })

    return recommended_movie_data

def display_recommendations(recommended_movie_data):
    """
    Displays recommended movies.

    Args:
        recommended_movie_data (list): A list of dictionaries containing the recommended movie details.
    """
    console.print(f"\n[bold green]Top {len(recommended_movie_data)} Recommended Movies:[/bold green]\n")

    for movie in recommended_movie_data:
        panel = Panel(
            Text.from_markup(f"[bold bright_cyan]Title:[/bold bright_cyan] [underline yellow]{movie['title']}[/underline yellow]\n[bright_magenta]Overview:[/bright_magenta] [italic white]{movie['overview']}[/italic white]"),
            title="[bold green]Movie Details[/bold green]",
            style="white",
            border_style="red",
            padding=(2, 4),
            width=console.width - 4  # Adjust the width based on the console width
        )
        console.print(panel)

def main():
    """
    The main function of the Movie Recommender System CLI.
    """
    parser = argparse.ArgumentParser(description='Movie Recommender System CLI')
    parser.add_argument('--movie', required=True, help='Input movie title for recommendations')
    parser.add_argument('--num_recommendations', type=int, default=5, help='Number of recommendations to show (default: 5)')
    parser.add_argument('--page_number', type=int, default=1, help='Page number for listing movies (default: 1)')

    args = parser.parse_args()

    if args.movie.lower() == 'list':
        list_all_movies(page_number=args.page_number)
        return

    try:
        recommended_movie_data = recommend(args.movie, args.num_recommendations)
        display_recommendations(recommended_movie_data)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

def print_large_text(text, font='standard'):
    """
    Prints large text using ASCII art.

    Args:
        text (str): The text to be printed.
        font (str, optional): The font style to use. Defaults to 'standard'.
    """
    f = Figlet(font=font)
    ascii_art = f.renderText(text)
    console.print(ascii_art)

def display_loading_animation():
    """
    Displays a loading animation.
    """
    animation = "|/-\\"
    for i in range(100):
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

if __name__ == "__main__":
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))

    print_large_text("Welcome to the Movie Recommender Command Line Interface!", font='rounded')
    console.print("\n[bright_yellow]Loading...[/bright_yellow]", end="")
    display_loading_animation()

    main()

    print_large_text("Thank you for using the Movie Recommender CLI!", font='tinker-toy')
    console.print("\n[bold yellow]Please provide your valuable feedback![/bold yellow]\n")
