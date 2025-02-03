import { useEffect, useState } from "react";
import "../styles/showmovies.css";
import { Card, Modal, Button } from 'react-bootstrap';
import axios from 'axios';

const API = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
});

API.interceptors.response.use(
    response => response,
    async error => {
        if (error.response?.status === 401) { 
            const refreshToken = localStorage.getItem("refresh_token");

            console.log("refresh token: ", refreshToken)

            if (refreshToken) {
                try {
                    const { data } = await axios.post("http://127.0.0.1:8000/api/users/token/refresh/", {
                        refresh: refreshToken
                    });

                    console.log("new access token: ", data)

                    localStorage.setItem("access_token", data.access);
                    
                    error.config.headers["Authorization"] = `Bearer ${data.access}`;
                    return axios(error.config);
                } catch (refreshError) {
                    console.error("Refresh Token Failed:", refreshError);
                    localStorage.removeItem("access_token");
                    localStorage.removeItem("refresh_token");
                    // window.location.href = "/login";  // Redirect to login page
                }
            }
        }
        return Promise.reject(error);
    }
);

API.interceptors.request.use(config => {
    const token = localStorage.getItem("access_token");
    if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
});


export const AddUserRating = async (selectedMovie, rating) => {
    try {
        const response = await API.post(
            'users/user-movies/',
            {
                movie_id: selectedMovie.movie_id,
                rating: rating,
                review: '',  // Optional for future implementation
            }
        );

        if (response.status === 201) {
            alert("Rating/Review submitted successfully!");
        } else {
            alert("Failed to submit rating/review.");
        }
    } catch (error) {
        console.error("Add User Rating Error:", error.response || error.message);
        alert(error.response?.data?.message || "An error occurred.");
    }
};

const RateModal = ({ selectedMovie, show, handleClose }) => {
    const [rating, setRating] = useState(0);
    const [hover, setHover] = useState(0);

    const handleSubmit = () => {
        AddUserRating(selectedMovie, rating)
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Rate This Movie</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="d-flex justify-content-center mt-3">
                    <div className="text-center">
        
                        <div className="rating">
                            {[5, 4, 3, 2, 1].map((num) => (
                                <span
                                    key={num}
                                    onClick={() => setRating(num)}
                                    onMouseEnter={() => setHover(num)}
                                    onMouseLeave={() => setHover(0)}
                                    style={{
                                        fontSize: "2rem",
                                        cursor: "pointer",
                                        color: (num <= (hover || rating)) ? "#ffc107" : "#e4e5e9"
                                    }}
                                >
                                    ★
                                </span>
                            ))}
                        </div>

                        <p className="mt-3">
                            {rating > 0 ? `You rated: ${rating} stars` : "Click a star to rate"}
                        </p>

                        <button 
                            className="btn btn-info px-4 py-1 mt-2"
                            onClick={handleSubmit}
                            disabled={rating === 0}
                        >
                            Submit
                        </button>
                    </div>
                </div>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
};

const DisplayMovieInfoModal = ({ showModal, handleCloseModal, selectedMovie }) => {
    const [showRatingModal, setShowRatingModal] = useState(false);

    return (
        <Modal show={showModal} onHide={handleCloseModal}>
            {selectedMovie && (
                <>
                <Modal.Header closeButton>
                    <Modal.Title>{selectedMovie.title}</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <p>{selectedMovie.overview}</p>
                    <img 
                        src={`https://image.tmdb.org/t/p/w500${selectedMovie.backdrop_path}`} 
                        alt={selectedMovie.title} 
                        className="img-fluid"
                    />
                </Modal.Body>

                <Modal.Footer>
                    <Button 
                        variant="dark"
                        onClick={() => setShowRatingModal(true)}
                    >
                        Rate Movie
                    </Button>
                </Modal.Footer>
                </>
            )}

            <RateModal selectedMovie={selectedMovie} show={showRatingModal} handleClose={() => setShowRatingModal(false)} />
        </Modal>
    );
};

export default DisplayMovieInfoModal