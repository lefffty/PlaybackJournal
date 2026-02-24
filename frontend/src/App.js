import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Routes, Route, Link, useNavigate} from 'react-router-dom'

import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Navbar';

import SignUp from './components/SignUp';
import Login from './components/Login';
import Albums from './components/Albums';
import Genres from './components/Genres';
import Artists from './components/Artists';

import UserService from './services/UserService';

function App() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);

  async function login(user = null) {
    UserService.login(user)
    .then(
      response => {
        setToken(response.data.auth_token);
        setUser(user);
        setError('');
      }
    )
    .catch(
      e => {
        console.log(e.toString());
      }
    )
  }

  async function logout() {
    setUser('');
    setToken('');
    localStorage.setItem('auth_token', '');
    localStorage.setItem('user', '');
    console.log('locaStorage', localStorage);
    navigate('/');
  }

  async function signup(user = null){
    setUser(user);
  }

  return (
    <div className="App">
      <Navbar bg='primary' variant='dark'>
        <div className='container-fluid'>
          <Navbar.Brand> PlaybackJournal</Navbar.Brand>
          <Nav className='me-auto'>
            <Container>
              <Link class='nav-link' to={"/albums"}>Albums</Link>
              <Link class='nav-link' to={"/artists"}>Artists</Link>
              <Link class='nav-link' to={"/genres"}>Genres</Link>
              {user ? (
                <>
                  <Link class='nav-link' to={'/profile'}>Profile</Link>
                  <button className="nav-link btn btn-link" onClick={logout}>
                      Logout
                  </button>
                </>
              ) : (
                <>
                  <Link class='nav-link' to={'/login'}>Login</Link>
                  <Link class='nav-link' to={'/signup'}>Sign Up</Link>
                </>
              )}
            </Container>
          </Nav>
        </div>
      </Navbar>
      <div className='container mt-4'>
        <Routes>
          <Route
          path='/genres'
          element={<Genres/>}
          >
          </Route>
          <Route
          path='/albums'
          element={<Albums/>}
          >
          </Route>
          <Route
          path='/artists'
          element={<Artists/>}
          >
          </Route>
          <Route
          path='/login'
          element={<Login login={login}/>}
          >
          </Route>
          <Route
          path='/signup'
          element={<SignUp signup={signup}/>}
          >
          </Route>
        </Routes>
      </div>

      <footer className='text-center text-lg-start bg-light text-muted mt-4'>
        <div className='text-center p-4'>
          Author: <a
            target='_blank'
            href='https://github.com/lefffty'
            className='text-reset fw-bold text-decoration-none'
          >lefffty</a>
        </div>
      </footer>
    </div>
  );
}

export default App;
