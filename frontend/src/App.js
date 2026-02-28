import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import {Routes, Route, Link, useNavigate} from 'react-router-dom'

import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Navbar';

import SignUp from './components/SignUp';
import Login from './components/Login';
import Password from './components/Password';
import Avatar from './components/Avatar';
import Profile from './components/Profile';
import UserService from './services/UserService';

import Albums from './components/Albums';
import Album from './components/Album';

import Genres from './components/Genres';
import Genre from './components/Genre';

import Artists from './components/Artists';
import Artist from './components/Artist';
import ArtistList from './components/ArtistList';


function App() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);

  useEffect(
    () => {
      const savedToken = localStorage.getItem('auth_token');
      const savedUser = localStorage.getItem('user');
      if (savedUser && savedToken){
        setToken(token);
        setUser(savedUser);
      } else{
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
      }
    }, []);

  async function login(user = null) {
    UserService.login(user)
    .then(
      (response) => {
        const token = response.data.auth_token;
        localStorage.setItem('auth_token', token);
        setToken(token);
        setUser(user);
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
    UserService.logout(token)
    .then(
      (_) => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        navigate('/login');
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
          <Navbar.Brand>
            <Link className='nav-link' to={"/albums/"}>
              PlaybackJournal
            </Link>
          </Navbar.Brand>
          <Nav className='me-auto'>
            <Container>
              <Link class='nav-link' to={"/albums/"}>Albums</Link>
              <Link class='nav-link' to={"/artists/"}>Artists</Link>
              <Link class='nav-link' to={"/genres/"}>Genres</Link>
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
                  <Link class='nav-link' to={'/signup/'}>Sign Up</Link>
                </>
              )}
            </Container>
          </Nav>
        </div>
      </Navbar>
      <div className='container mt-4'>
        <Routes>
          <Route
            path='/artists/:id/discography/'
            element={<ArtistList dataType="discography"/>}
          >
          </Route>
          <Route
            path='/artists/:id/similar/'
            element={<ArtistList dataType="similar"/>}
          >
          </Route>
          <Route
            path='/'
            element={<Albums/>}
          >
          </Route>
          <Route
            path='/albums/'
            element={<Albums/>}
          >
          </Route>
          <Route
            path='/profile/'
            element={<Profile token={token}/>}
          >
          </Route>
          <Route
            path='/genres/'
            element={<Genres/>}
          >
          </Route>
          <Route
            path='/artists'
            element={<Artists />}
          >
          </Route>
          <Route
            path='/artists/:id/'
            element={<Artist />}
          >
          </Route>
          <Route
            path='/login/'
            element={<Login login={login}/>}
          >
          </Route>
          <Route
            path='/signup/'
            element={<SignUp signup={signup}/>}
          >
          </Route>
          <Route
            path='/albums/:id/'
            element={<Album />}
          >
          </Route>
          <Route
            path='/genres/:id/'
            element={<Genre />}
          >
          </Route>
          <Route
            path='/profile/password/'
            element={<Password/>}
          >
          </Route>
          <Route
            path='/profile/avatar/'
            element={<Avatar/>}
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
