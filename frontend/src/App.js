import React, { useEffect, useState } from 'react';
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
import Album from './components/Album';

import UserService from './services/UserService';
import Profile from './components/Profile';
import Avatar from './components/Avatar';
import Password from './components/Password';

import axios from 'axios';

function App() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);

  async function login(user = null) {
    UserService.login(user)
    .then(
      (response) => {
        axios.defaults.headers['Authorization'] = 'Token ' + response.data.auth_token;
        setToken(response.data.auth_token);
        setUser(user);
        localStorage.setItem('auth_token', response.data.auth_token);
        localStorage.setItem('user', user);
        setError('');
      }
    )
    .catch(
      (e) => {
        setError(e.toString());
      }
    )
  }

  async function logout() {
    console.log('Token inside logout ', token);
    UserService.logout(token)
    .then(
      (response) => {
        delete axios.defaults.headers['Authorization'];
        setUser('');
        setToken('');
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        navigate('/albums');
      }
    )
    .catch(
      (e) => {
        setError(e.toString());
      }
    )
  }

  async function signup(user = null){
    UserService.signup(user)
    .catch(
      (e) => {
        setError(e.toString());
      }
    );
  };

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
            path='/profile'
            element={<Profile token={token}/>}
          >
          </Route>
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
          <Route
            path='/albums/:id/'
            element={<Album />}
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
