import {React, useEffect, useState } from 'react';
import { Card, Carousel, Stack } from 'react-bootstrap';
import axios from 'axios';
import "../styles/movies-carousel.css";

const MovieCard = ({ image }) => {
    return (
      <Card style={{ width: '18rem' }}>
        <Card.Img variant="top" src={image} alt="Movie poster" />
      </Card>
    );
  };
  
  const MoviesCarousel = () => {
    const [movies, setMovies] = useState([]);
    const [moviesPerSlide, setMoviesPerSlide] = useState(3); // Default to 3 movies per slide
  
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
  
    useEffect(() => {
      // Fetch popular movies from the API
      axios
        .get('http://localhost:8000/api/popular-movies/')
        .then((response) => {
          setMovies(response.data.results); // Assuming the API response has a "results" array
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
      <div className="pt-5">
        <h1 className="carousel-title fw-bold ps-5">Popular Movies</h1>
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
                      key={movie.id}
                      image={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
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