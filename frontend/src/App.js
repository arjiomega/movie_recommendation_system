// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from './components/NavBar';
import "./App.css"
import HomePage from './pages/HomePage';
import Profile from './pages/Profile';
function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Router>
    // <div className="App">
    //   <NavBar />  
    //   <MoviesCarousel />
    //   <ShowMovies />
    // </div>
  );
}

export default App;
