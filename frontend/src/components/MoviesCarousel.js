// src/components/MoviesCarousel.js

import React, { useEffect, useState } from 'react';
import { Card, Carousel, Stack } from 'react-bootstrap';
import axios from 'axios';
import "../styles/movies-carousel.css";
import Hero from './Hero';  // Make sure to import Hero

const MovieCard = ({ movie, onHover, onClick }) => {
  const { poster_path, title } = movie;

  return (
    <div
      onMouseEnter={() => onHover(movie)} // Trigger hover with movie data
      onClick={() => onClick(movie)} // Trigger click with movie data
    >
      <Card
        style={{ width: '18rem' }}
      >
        <Card.Img variant="top" src={poster_path ? `https://image.tmdb.org/t/p/w500${poster_path}` : "https://via.placeholder.com/500"} alt={title} />
      </Card>
    </div>
  );
};

const MoviesCarousel = () => {
  const [movies, setMovies] = useState([]);
  const [moviesPerSlide, setMoviesPerSlide] = useState(3);
  const [hoveredMovie, setHoveredMovie] = useState(null);
  const [activeMovie, setActiveMovie] = useState(null); // Store the active movie

  // Update moviesPerSlide based on window size
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 1200) {
        setMoviesPerSlide(6); // Show 6 movies for large screens
      } else {
        setMoviesPerSlide(3); // Show 3 movies for smaller screens
      }
    };

    handleResize(); // Initialize the movies per slide value
    window.addEventListener('resize', handleResize); // Add event listener for resize
    return () => {
      window.removeEventListener('resize', handleResize); // Clean up event listener
    };
  }, []);

  // Fetch top movies from the API
  useEffect(() => {
    axios
      .get('http://localhost:8000/api/movies/top-movies/')
      .then((response) => {
        if (response.data && response.data.top_movies) {
          setMovies(response.data.top_movies);
          // Set the first movie as the default active movie
          setActiveMovie(response.data.top_movies[0]);
        }
      })
      .catch((error) => {
        console.error("Error fetching movies:", error);
      });
  }, []);

  // Helper function to group movies into sets based on screen size
  const chunkMovies = (movies, chunkSize) => {
    const chunks = [];
    for (let i = 0; i < movies.length; i += chunkSize) {
      chunks.push(movies.slice(i, i + chunkSize));
    }
    return chunks;
  };

  const groupedMovies = chunkMovies(movies, moviesPerSlide); // Group movies based on the screen size

  return (
    <div className="">
      {/* Hero Section */}
      {activeMovie && (
        <Hero movie={activeMovie} /> // Show Hero with active movie
      )}

      <h1 className="carousel-title fw-bold ps-5 pt-5">Popular Movies</h1>

      <div className="container-fluid">
        <Carousel>
          {groupedMovies.map((group, index) => (
            <Carousel.Item key={index} style={{ height: 500 }}>
              <Stack
                direction="horizontal"
                className="h-100 justify-content-center align-items-center"
                gap={3}
              >
                {group.map((movie) => (
                  <MovieCard
                    key={movie.movie_id}
                    movie={movie}
                    onHover={setActiveMovie} // Set hovered movie
                    onClick={setActiveMovie}  // Set active movie on click
                  />
                ))}
              </Stack>
            </Carousel.Item>
          ))}
        </Carousel>
      </div>
    </div>
  );
};

export default MoviesCarousel;
