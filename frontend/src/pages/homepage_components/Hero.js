// src/components/Hero.js
import React, { useEffect, useState } from "react";
import "../../styles/hero.css"; // Import the styles

const Hero = ({ movie }) => {
  const [animate, setAnimate] = useState(false); // State to trigger the animation

  useEffect(() => {
    if (movie) {
      setAnimate(false); // Reset the animation when the movie changes
      setTimeout(() => setAnimate(true), 50); // Add a small delay before triggering the animation
    }
  }, [movie]); // Re-run when the movie changes

  if (!movie) return null;

  return (
    <div
      className="hero-container"
      style={{
        backgroundImage: `url(https://image.tmdb.org/t/p/original${movie.backdrop_path})`,
      }}
    >
      <div className={`hero-content ${animate ? "fadeUp" : ""}`}>
        <h1 className="hero-title">{movie.title}</h1>
        <div className="hero-info">
            <span className="rating-icon">⭐ {movie.vote_average}</span>
            <span className="year-icon">📅 {new Date(movie.release_date).getFullYear()}</span>
        </div>
        <p className="hero-overview">{movie.overview}</p>
      </div>
    </div>
  );
};

export default Hero;
