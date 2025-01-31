// src/App.js
import React from 'react';
import { Button, Container, Row, Col, Card, Carousel, Stack } from 'react-bootstrap';
import NavBar from './components/NavBar';
import MoviesCarousel from './components/MoviesCarousel';
import "./App.css"

function App() {
  return (
    <div className="App">
      <NavBar />  
      <MoviesCarousel />
    </div>
  );
}

export default App;
