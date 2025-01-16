import { Navbar, Container, Nav } from 'react-bootstrap';
import "../styles/navbar.css";

const NavBar = () => {
    return (
      <Navbar expand="lg" className="navbar-custom">
        <Container>
          <Navbar.Brand href="/" className="navbar-brand">
            Movie Recommendation
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="navbar-nav" />
          <Navbar.Collapse id="navbar-nav">
            <Nav className="ml-auto">
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
        </Container>
      </Navbar>
    );
  };
  
  export default NavBar;