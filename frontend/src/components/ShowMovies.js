import { useEffect, useState } from "react";
import "../styles/showmovies.css";
import { Card, Modal, Button } from 'react-bootstrap';

import DisplayMovieInfoModal from './MovieCardModal';

const PageControl = ({pageNum, setPageNum, minPage, maxPage}) => {
    const MIN_PAGE = minPage;
    const MAX_PAGE = maxPage;
    
    return (
        <div className="pt-5 pb-3">
            <nav aria-label="Page navigation example">
                <ul className="pagination justify-content-center">
                    <li className="page-item disabled" onClick={() => setPageNum(prevPageNum => Math.max(prevPageNum - 1, MIN_PAGE))}>
                        <a className="page-link" tabIndex="-1" aria-disabled="true">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>

                    <li className="page-item"><a className="page-link">PAGE: {pageNum}</a></li>

                    <li className="page-item" onClick={() => setPageNum(prevPageNum => Math.min(prevPageNum + 1, MAX_PAGE))}>
                        <a className="page-link">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    )
}

const fetchTopMovies = async (page, movie_per_page) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/movies/top-movies-paginated/?page=${page}&movie_per_page=${movie_per_page}`);

        if (!response.ok) {
            throw new Error("Failed to fetch movies.");
        }

        return await response.json();
    } catch (error) {
        console.error(error);
        return null; // Handle errors gracefully
    }
};


const DisplayMovies = ({current_page}) => {

    const [movies, setMovies] = useState([]);
    const movie_per_page = 12

    useEffect(() => {
        const getMovies = async () => {
            const data = await fetchTopMovies(current_page, movie_per_page);
            if (data && data.top_movies) {
                setMovies(data.top_movies);
            }
        };

        getMovies();
    }, [current_page]);

    const [cardSize, setCardSize] = useState('18rem');

    useEffect(() => {
        const cardResize = () => {
            const windowWidth = window.innerWidth;
            
            // Smooth resizing using a scaling factor
            const newCardSize = Math.max(10, Math.min(windowWidth / 70, 18)); // Adjust scaling factor (70) for smoother resizing
            setCardSize(`${newCardSize}rem`);
        };

        // Initial resize
        cardResize();

        // Add event listener for resizing
        window.addEventListener('resize', cardResize);

        // Cleanup on component unmount
        return () => {
            window.removeEventListener('resize', cardResize);
        };
    }, []);

    const [showModal, setShowModal] = useState(false);
    const [selectedMovie, setSelectedMovie] = useState(null);

    const handleCardClick = (movie) => {
        setSelectedMovie(movie); // Set the movie for the modal
        setShowModal(true); // Show the modal
    };

    const handleCloseModal = () => {
        setShowModal(false); // Hide the modal
    };

    return (
        <div className="container">
            <div className="row justify-content-center">
                {movies.length > 0 ? (
                    movies.map((movie) => (
                        <div key={movie.movie_id} className="col-auto movie-box pt-1 pb-1" onClick={() => handleCardClick(movie)}>
                            <div className="movie-card">
                                <Card.Img 
                                    style={{ width: `${cardSize}`, border: '2px solid white'}} 
                                    className="rounded-2"
                                    src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                                />
                            </div>
                        </div>
                    ))
                ) : (
                    <p>Loading...</p>
                )}
            </div>

            <DisplayMovieInfoModal showModal={showModal} handleCloseModal={handleCloseModal} selectedMovie={selectedMovie} />
          
        </div>
    );
}

const ShowMovies = () => {
    const MIN_PAGE = 1;
    const MAX_PAGE = 10;
    const [pageNum, setPageNum] = useState(() => {return MIN_PAGE})

    useEffect(() => {
        console.log("current page: ", pageNum)
    }, [pageNum])

    return (
        <div className="showmovies-container pt-5">
            <DisplayMovies current_page={pageNum} />
            <PageControl pageNum={pageNum} setPageNum={setPageNum} minPage={MIN_PAGE} maxPage={MAX_PAGE} />
        </div>
    );
};

export default ShowMovies;