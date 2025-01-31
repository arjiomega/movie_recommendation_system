import { Navbar, Container, Nav, Button } from 'react-bootstrap';
import React, { useState } from 'react';
import "../styles/navbar.css";

// Importing the Modal for login/register
import LoginModal from './LoginModal';

const NavBar = () => {
  const [showModal, setShowModal] = useState(false); // State to control modal visibility

  const handleShowModal = () => setShowModal(true);  // Function to open the modal
  const handleCloseModal = () => setShowModal(false); // Function to close the modal

  return (
    <>
      <Navbar expand="lg" className="navbar-custom navbar-dark bg-dark justify-content-between">
        <Container>
          <Navbar.Brand href="/" className="navbar-brand">
            Movie Recommendation
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="navbar-nav" />
          <Navbar.Collapse id="navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="/" className="nav-link">
                Home
              </Nav.Link>
              <Nav.Link href="/" className="nav-link">
                Recommendations
              </Nav.Link>
              <Nav.Link href="/" className="nav-link">
                About
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
          {/* Add Login/Register button aligned to the far right */}
          <Button 
            variant="primary" 
            onClick={handleShowModal} 
            className="login-btn btn-dark">
            Login/Register
          </Button>
        </Container>
      </Navbar>

      {/* Modal for Login/Register */}
      <LoginModal show={showModal} handleClose={handleCloseModal} />
    </>
  );
};

export default NavBar;
