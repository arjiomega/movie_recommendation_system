import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import axios from 'axios';
import "../styles/login_modal.css";
const LoginModal = ({ show, handleClose, setIsLoggedIn, setUserEmail }) => {
  const [isRegistering, setIsRegistering] = useState(false); // State to toggle login/register
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (isRegistering) {
      try {
        const response = await axios.post('http://localhost:8000/api/users/register/', {
          email: formData.email,
          password: formData.password,
        });
        alert(response.data.message);
        setIsRegistering(false);
      } catch (error) {
        console.error(error.response);
        alert('Error during registration');
      }
    } else {
      try {
        const response = await axios.post('http://localhost:8000/api/users/login/', {
          email: formData.email,
          password: formData.password,
        });
  
        if (response.status === 200) {
          const data = response.data;
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
          localStorage.setItem("user_email", formData.email); // ✅ Store email
          
          setIsLoggedIn(true);
          setUserEmail(formData.email); // ✅ Update NavBar state
  
          handleClose(); // Close modal on success
        }
      } catch (error) {
        console.error("Login Error:", error.response || error.message);
        alert(error.response?.data?.message || "An error occurred.");
      }
    }
  };

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>{isRegistering ? "Register" : "Login"}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {isRegistering ? (
          <>
            <p className="text-center h4 fw-bold mb-3">Sign up</p>
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3">
                <Form.Label>Your Email</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Enter your email"
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Enter password"
                />
              </Form.Group>

              <Button variant="dark" type="submit" className="w-100">
                Register
              </Button>
            </Form>
            <p className="text-center mt-3">
              Already have an account?{" "}
              <span className="text-primary" style={{ cursor: "pointer" }} onClick={() => setIsRegistering(false)}>
                Login here
              </span>
            </p>
          </>
        ) : (
          <>
            <p className="text-center h4 fw-bold mb-3">Login</p>
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Enter your email"
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Enter password"
                />
              </Form.Group>

              <Button variant="dark" type="submit" className="w-100">
                Login
              </Button>
            </Form>
            <p className="text-center mt-3">
              Don't have an account?{" "}
              <span className="text-primary" style={{ cursor: "pointer" }} onClick={() => setIsRegistering(true)}>
                Register here
              </span>
            </p>
          </>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LoginModal;
