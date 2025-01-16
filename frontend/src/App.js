// src/App.js
import React from 'react';
import { Button, Container, Row, Col, Card, Carousel, Stack } from 'react-bootstrap';
import NavBar from './components/NavBar';
import MoviesCarousel from './components/MoviesCarousel';
import "./App.css"

function ContainerFluidBreakpointExample() {
  const reviews = [
    { _id: 1, text: "abc" },
    { _id: 2, text: "def" },
    { _id: 3, text: "ghi" },
    { _id: 4, text: "jkl" },
    { _id: 5, text: "mno" },
    { _id: 6, text: "pqr" },
    { _id: 7, text: "stu" },
    { _id: 8, text: "vwx" },
    { _id: 9, text: "yza" }
  ];

  return (
    <div>
      <h1 className="text-center fw-bold my-5">
        User Reviews ({reviews.length})
      </h1>
      <div className="bg-dark bg-opacity-25 container-fluid">
        <Carousel style={{ height: 500 }}>
          {reviews.map((review, index) => (
            <Carousel.Item style={{ height: 500 }}>
              <Stack
                direction="horizontal"
                className="h-100 justify-content-center align-items-center"
                gap={3}
              >
                <Card style={{ width: "18rem" }}>
                  <Card.Body>
                    <Card.Title>Card Title</Card.Title>
                    <Card.Text>
                      Some quick example text to build on the card title and
                      make up the bulk of the card's content.
                    </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
                  </Card.Body>
                </Card>

                <Card style={{ width: "18rem" }}>
                  <Card.Body>
                    <Card.Title>Card Title</Card.Title>
                    <Card.Text>
                      Some quick example text to build on the card title and
                      make up the bulk of the card's content.
                    </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
                  </Card.Body>
                </Card>

                <Card style={{ width: "18rem" }}>
                  <Card.Body>
                    <Card.Title>Card Title</Card.Title>
                    <Card.Text>
                      Some quick example text to build on the card title and
                      make up the bulk of the card's content.
                    </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
                  </Card.Body>
                </Card>
              </Stack>
            </Carousel.Item>
          ))}
        </Carousel>
      </div>
    </div>
  );
}


function App() {
  return (
    <div className="App">
      <NavBar />  
      <MoviesCarousel />
    </div>
  );
}

export default App;
