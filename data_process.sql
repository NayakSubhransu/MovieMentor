-- Movie Recommendation System Analysis using SQL

-- ============================================
-- 1. DATA SETUP AND SCHEMA DEFINITION
-- ============================================

-- Create tables based on the dataset schemas
CREATE TABLE tmdb_credits (
    movie_id INT,
    title VARCHAR(255),
    cast TEXT,
    crew TEXT
);

CREATE TABLE tmdb_movies (
    budget BIGINT,
    genres TEXT,
    homepage VARCHAR(500),
    id INT,
    keywords TEXT,
    original_language VARCHAR(10),
    original_title VARCHAR(255),
    overview TEXT,
    popularity DECIMAL(10,6),
    production_companies TEXT,
    production_countries TEXT,
    release_date DATE,
    revenue BIGINT,
    runtime DECIMAL(5,1),
    spoken_languages TEXT,
    status VARCHAR(50),
    tagline TEXT,
    title VARCHAR(255),
    vote_average DECIMAL(3,1),
    vote_count INT
);

-- ============================================
-- 2. DATA EXPLORATION AND BASIC STATISTICS
-- ============================================

-- Check dataset dimensions and basic info
SELECT COUNT(*) as total_movies FROM tmdb_movies;
SELECT COUNT(*) as total_credits FROM tmdb_credits;

-- Check for null values in key columns
SELECT 
    COUNT(*) as total_records,
    COUNT(overview) as overview_count,
    COUNT(*) - COUNT(overview) as overview_nulls,
    COUNT(genres) as genres_count,
    COUNT(*) - COUNT(genres) as genres_nulls,
    COUNT(keywords) as keywords_count,
    COUNT(*) - COUNT(keywords) as keywords_nulls
FROM tmdb_movies;

-- Check for duplicates
SELECT title, COUNT(*) as duplicate_count
FROM tmdb_movies
GROUP BY title
HAVING COUNT(*) > 1;

-- ============================================
-- 3. DATA MERGING (equivalent to pandas merge)
-- ============================================

-- Create merged dataset similar to movies.merge(credits, on='title')
CREATE VIEW merged_movies AS
SELECT 
    m.id,
    m.title,
    m.overview,
    m.genres,
    m.keywords,
    m.budget,
    m.revenue,
    m.vote_average,
    m.vote_count,
    m.release_date,
    c.cast,
    c.crew
FROM tmdb_movies m
LEFT JOIN tmdb_credits c ON m.title = c.title
WHERE m.overview IS NOT NULL;  -- Remove null overviews

-- ============================================
-- 4. DATA PREPROCESSING FOR CONTENT-BASED FILTERING
-- ============================================

-- Since SQL doesn't have built-in JSON parsing like Python's ast.literal_eval,
-- we'll create functions to extract key information from JSON-like strings

-- Function to extract genre names (simplified - would need actual JSON parsing in practice)
CREATE VIEW movie_features AS
SELECT 
    id as movie_id,
    title,
    overview,
    -- In practice, you'd need proper JSON parsing functions
    -- This is a simplified version showing the concept
    LOWER(REPLACE(REPLACE(REPLACE(genres, '"', ''), '[', ''), ']', '')) as genres_clean,
    LOWER(REPLACE(REPLACE(REPLACE(keywords, '"', ''), '[', ''), ']', '')) as keywords_clean,
    LOWER(REPLACE(REPLACE(REPLACE(cast, '"', ''), '[', ''), ']', '')) as cast_clean,
    LOWER(REPLACE(REPLACE(REPLACE(crew, '"', ''), '[', ''), ']', '')) as crew_clean
FROM merged_movies;

-- Create content tags (equivalent to Python's tags column)
CREATE VIEW movie_tags AS
SELECT 
    movie_id,
    title,
    LOWER(CONCAT(
        COALESCE(overview, ''), ' ',
        COALESCE(genres_clean, ''), ' ',
        COALESCE(keywords_clean, ''), ' ',
        COALESCE(cast_clean, ''), ' ',
        COALESCE(crew_clean, '')
    )) as content_tags
FROM movie_features;

-- ============================================
-- 5. CONTENT-BASED SIMILARITY CALCULATION
-- ============================================

-- Since SQL doesn't have built-in TF-IDF or cosine similarity,
-- we'll create a simplified word-based similarity approach

-- Create word frequency table for each movie
CREATE VIEW movie_words AS
SELECT 
    movie_id,
    title,
    TRIM(value) as word,
    COUNT(*) as word_count
FROM movie_tags
CROSS APPLY STRING_SPLIT(content_tags, ' ') 
WHERE TRIM(value) != '' 
    AND LENGTH(TRIM(value)) > 2  -- Filter short words
    AND TRIM(value) NOT IN ('the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by')  -- Basic stop words
GROUP BY movie_id, title, TRIM(value);

-- Calculate movie similarity based on shared words (simplified Jaccard similarity)
CREATE VIEW movie_similarity AS
SELECT 
    m1.movie_id as movie1_id,
    m1.title as movie1_title,
    m2.movie_id as movie2_id,
    m2.title as movie2_title,
    COUNT(DISTINCT m1.word) as common_words,
    (COUNT(DISTINCT m1.word) * 1.0) / 
    (SELECT COUNT(DISTINCT word) FROM movie_words WHERE movie_id IN (m1.movie_id, m2.movie_id)) as similarity_score
FROM movie_words m1
JOIN movie_words m2 ON m1.word = m2.word AND m1.movie_id != m2.movie_id
GROUP BY m1.movie_id, m1.title, m2.movie_id, m2.title
HAVING COUNT(DISTINCT m1.word) >= 3;  -- At least 3 common words

-- ============================================
-- 6. RECOMMENDATION FUNCTION (SQL Procedure)
-- ============================================

-- Create a stored procedure for movie recommendations
CREATE PROCEDURE GetMovieRecommendations
    @MovieTitle VARCHAR(255),
    @TopN INT = 5
AS
BEGIN
    DECLARE @MovieId INT;
    
    -- Get the movie ID for the input title
    SELECT @MovieId = movie_id 
    FROM movie_tags 
    WHERE title = @MovieTitle;
    
    -- Return top recommendations
    SELECT TOP (@TopN)
        movie2_title as recommended_movie,
        similarity_score,
        common_words
    FROM movie_similarity
    WHERE movie1_id = @MovieId
    ORDER BY similarity_score DESC, common_words DESC;
END;

-- ============================================
-- 7. ANALYSIS QUERIES
-- ============================================

-- Top movies by vote average
SELECT TOP 10
    title,
    vote_average,
    vote_count,
    release_date
FROM merged_movies
WHERE vote_count >= 100  -- Filter for movies with sufficient votes
ORDER BY vote_average DESC;

-- Genre popularity analysis
WITH genre_stats AS (
    SELECT 
        TRIM(genre_item) as genre,
        COUNT(*) as movie_count,
        AVG(vote_average) as avg_rating,
        AVG(CAST(revenue as DECIMAL(15,2))) as avg_revenue
    FROM merged_movies
    CROSS APPLY STRING_SPLIT(REPLACE(REPLACE(genres, '"', ''), 'name:', ''), ',')
    WHERE TRIM(genre_item) LIKE '%Action%' 
       OR TRIM(genre_item) LIKE '%Drama%'
       OR TRIM(genre_item) LIKE '%Comedy%'
       OR TRIM(genre_item) LIKE '%Thriller%'
       OR TRIM(genre_item) LIKE '%Romance%'
    GROUP BY TRIM(genre_item)
)
SELECT * FROM genre_stats ORDER BY movie_count DESC;

-- Revenue vs Budget analysis
SELECT 
    title,
    budget,
    revenue,
    CASE 
        WHEN budget > 0 THEN CAST(revenue as DECIMAL(10,2)) / CAST(budget as DECIMAL(10,2))
        ELSE 0 
    END as roi_ratio,
    vote_average
FROM merged_movies
WHERE budget > 1000000 AND revenue > 0  -- Filter for meaningful budget/revenue
ORDER BY roi_ratio DESC;

-- Release year trends
SELECT 
    YEAR(release_date) as release_year,
    COUNT(*) as movies_released,
    AVG(vote_average) as avg_rating,
    AVG(CAST(budget as DECIMAL(15,2))) as avg_budget,
    AVG(CAST(revenue as DECIMAL(15,2))) as avg_revenue
FROM merged_movies
WHERE release_date IS NOT NULL
GROUP BY YEAR(release_date)
ORDER BY release_year DESC;

-- ============================================
-- 8. SAMPLE RECOMMENDATION QUERIES
-- ============================================

-- Get recommendations for "Avatar"
EXEC GetMovieRecommendations @MovieTitle = 'Avatar', @TopN = 5;

-- Alternative direct query for recommendations
SELECT TOP 5
    ms.movie2_title as recommended_movie,
    ms.similarity_score,
    m.vote_average,
    m.release_date
FROM movie_similarity ms
JOIN merged_movies m ON ms.movie2_id = m.id
WHERE ms.movie1_title = 'Avatar'
ORDER BY ms.similarity_score DESC;

-- Find similar movies to multiple titles
WITH target_movies AS (
    SELECT movie_id FROM movie_tags 
    WHERE title IN ('Avatar', 'Spectre', 'John Carter')
)
SELECT 
    ms.movie2_title as recommended_movie,
    AVG(ms.similarity_score) as avg_similarity,
    COUNT(*) as matching_movies
FROM movie_similarity ms
WHERE ms.movie1_id IN (SELECT movie_id FROM target_movies)
GROUP BY ms.movie2_title, ms.movie2_id
HAVING COUNT(*) >= 2  -- Similar to at least 2 input movies
ORDER BY avg_similarity DESC, matching_movies DESC;

-- ============================================
-- 9. PERFORMANCE OPTIMIZATION
-- ============================================

-- Create indexes for better performance
CREATE INDEX idx_movie_title ON merged_movies(title);
CREATE INDEX idx_movie_id ON movie_tags(movie_id);
CREATE INDEX idx_similarity_movie1 ON movie_similarity(movie1_id, similarity_score);
CREATE INDEX idx_vote_average ON merged_movies(vote_average, vote_count);

-- ============================================
-- 10. DATA VALIDATION AND QUALITY CHECKS
-- ============================================

-- Check data quality
SELECT 
    'Total Movies' as metric,
    COUNT(*) as count
FROM merged_movies
UNION ALL
SELECT 
    'Movies with Overview' as metric,
    COUNT(*) as count
FROM merged_movies
WHERE overview IS NOT NULL
UNION ALL
SELECT 
    'Movies with Genres' as metric,
    COUNT(*) as count
FROM merged_movies
WHERE genres IS NOT NULL AND genres != '[]'
UNION ALL
SELECT 
    'Movies with Cast Info' as metric,
    COUNT(*) as count
FROM merged_movies
WHERE cast IS NOT NULL AND cast != '[]';

-- Summary statistics
SELECT 
    MIN(vote_average) as min_rating,
    MAX(vote_average) as max_rating,
    AVG(vote_average) as avg_rating,
    STDEV(vote_average) as rating_stdev,
    COUNT(*) as total_movies
FROM merged_movies
WHERE vote_count >= 10;