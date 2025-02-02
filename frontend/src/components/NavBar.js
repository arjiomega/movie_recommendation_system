import { Navbar, Container, Nav, Button, Dropdown } from 'react-bootstrap';
import React, { useState, useEffect } from 'react';
import "../styles/navbar.css";

// Importing the Modal for login/register
import LoginModal from './LoginModal';

const NavBar = () => {
  const [showModal, setShowModal] = useState(false); // State to control modal visibility
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const email = localStorage.getItem("user_email");
    
    if (token && email) {
      setIsLoggedIn(true);
      setUserEmail(email);
    }
  }, []);

  const handleShowModal = () => setShowModal(true);  // Function to open the modal
  const handleCloseModal = () => setShowModal(false); // Function to close the modal

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_email");
    setIsLoggedIn(false);
    setUserEmail("");
  };

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
              <Nav.Link href="/" className="nav-link">Home</Nav.Link>
              <Nav.Link href="/" className="nav-link">Recommendations</Nav.Link>
              <Nav.Link href="/" className="nav-link">About</Nav.Link>
            </Nav>
          </Navbar.Collapse>

          {/* Show Profile when logged in, otherwise show Login/Register button */}
          {isLoggedIn ? (
            <Dropdown>
              <Dropdown.Toggle variant="dark" id="dropdown-dark">
                {userEmail}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <Dropdown.Item href="/profile">Profile</Dropdown.Item>
                <Dropdown.Item onClick={handleLogout}>Logout</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          ) : (
            <Button 
              variant="dark" 
              onClick={handleShowModal} 
              className="login-btn btn-dark">
              Login/Register
            </Button>
          )}
        </Container>
      </Navbar>

      {/* Pass `setIsLoggedIn` and `setUserEmail` to LoginModal */}
      <LoginModal show={showModal} handleClose={handleCloseModal} setIsLoggedIn={setIsLoggedIn} setUserEmail={setUserEmail} />
    </>
  );
};

export default NavBar;
