import React from 'react';

import "../App.css"
import MoviesCarousel from './homepage_components/MoviesCarousel';
import ShowMovies from '../components/ShowMovies';
function HomePage() {
  return (
    <div className="HomePage">
      <MoviesCarousel />
      <ShowMovies />
    </div>
  );
}

export default HomePage;
