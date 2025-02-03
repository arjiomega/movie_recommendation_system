import React, { useState, useEffect } from 'react';
import { Modal, Button, Table } from 'react-bootstrap';
import axios from 'axios';

import "./profile_components/styles/Profile.css";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
});

API.interceptors.response.use(
    response => response,
    async error => {
        if (error.response?.status === 401) { 
            const refreshToken = localStorage.getItem("refresh_token");

            if (refreshToken) {
                try {
                    const { data } = await axios.post("http://127.0.0.1:8000/api/users/token/refresh/", {
                        refresh: refreshToken
                    });

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

const fetchUserMovies = async (setUserMovies, setError, setLoading) => {
    setLoading(true);
    try {        
        const response = await API.get('users/user-movies/');

        if (response.status === 200) {
            setUserMovies(response.data);
        } else {
            setError('Failed to fetch user movies.');
        }
    } catch (error) {
        setError(error.response?.data?.message || "An error occurred.");
    } finally {
        setLoading(false);
    }
};

const deleteUserMovie = async (movieId, setUserMovies, setError) => {
    try {
        const response = await API.delete('users/user-movies/', { data: { movie_id: movieId } });

        if (response.status === 204) {
            setUserMovies(prevMovies => prevMovies.filter(movie => movie.movie_id !== movieId));
        } else {
            setError('Failed to delete movie.');
        }
    } catch (error) {
        setError(error.response?.data?.message || "An error occurred.");
    }
};

function Profile() {
    const [userMovies, setUserMovies] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [movieToDelete, setMovieToDelete] = useState(null);
    const userEmail = localStorage.getItem("user_email");

    useEffect(() => {
        fetchUserMovies(setUserMovies, setError, setLoading);
    }, []);

    const handleDelete = (movieId) => {
        setMovieToDelete(movieId);
        setShowModal(true);
    };

    const confirmDelete = () => {
        deleteUserMovie(movieToDelete, setUserMovies, setError);
        setShowModal(false);
    };

    return (
        <div className="Profile">
            <div className="profile-header text-center py-4">
                <h1>Profile Page</h1>
                <p>Welcome, {userEmail || "Guest"}!</p>
                <p>This is your profile page.</p>
            </div>

            {error && <p className="text-danger">{error}</p>}

            {loading ? (
                <p>Loading...</p>
            ) : (
                <div className="table-responsive">
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Movie Title</th>
                                <th>Rating</th>
                                <th>Review</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {userMovies.map((movie, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td>{movie.movie_title}</td>
                                    <td>{movie.rating}</td>
                                    <td>{movie.review || "No review"}</td>
                                    <td>
                                        <Button 
                                            variant="danger" 
                                            onClick={() => handleDelete(movie.movie_id)}
                                        >
                                            Delete
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </div>
            )}

            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Confirm Deletion</Modal.Title>
                </Modal.Header>
                <Modal.Body>Are you sure you want to delete this movie?</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Cancel
                    </Button>
                    <Button variant="danger" onClick={confirmDelete}>
                        Delete
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}

export default Profile;