import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const LoginModal = ({ show, handleClose }) => {
  const [isRegistering, setIsRegistering] = useState(false); // State to toggle login/register

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>{isRegistering ? "Register" : "Login"}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {isRegistering ? (
          <>
            <p className="text-center h4 fw-bold mb-3">Sign up</p>
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Your Name</Form.Label>
                <Form.Control type="text" placeholder="Enter your name" />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Your Email</Form.Label>
                <Form.Control type="email" placeholder="Enter your email" />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Enter password" />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Repeat your password</Form.Label>
                <Form.Control type="password" placeholder="Repeat password" />
              </Form.Group>

              <Form.Check className="mb-3" type="checkbox" label="I agree to the Terms of Service" />

              <Button variant="primary" type="submit" className="w-100">
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
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" placeholder="Enter your email" />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Enter password" />
              </Form.Group>

              <Button variant="primary" type="submit" className="w-100">
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
