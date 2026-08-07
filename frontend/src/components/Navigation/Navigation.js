import { Navbar, Nav, Image } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import { FaCompactDisc, FaMicrophoneAlt, FaMusic, FaListAlt, FaUser, FaSignOutAlt, FaSignInAlt, FaUserPlus } from 'react-icons/fa';
import logo from '../../logo.png';
import './Navigation.css';

import SearchField from '../Common/SearchField';

function Navigation({ user, logout }) {
  return (
    <Navbar expand='lg' className='custom-navbar shadow-sm' variant='dark'>
      <div className='container-fluid'>
        <Navbar.Brand>
          <NavLink to='/albums/'>
            <Image src={logo} height={50} />
          </NavLink>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls='main-nav' />
        <Navbar.Collapse id='main-nav'>
          <Nav className='me-auto mb-2 mb-lg-0 fs-5'>
            <NavLink className='nav-link' to='/albums/'><FaCompactDisc className='me-2' />Albums</NavLink>
            <NavLink className='nav-link' to='/artists/'><FaMicrophoneAlt className='me-2' />Artists</NavLink>
            <NavLink className='nav-link' to='/genres/'><FaMusic className='me-2' />Genres</NavLink>
            <NavLink className='nav-link' to='/playlists/'><FaListAlt className='me-2' />Playlists</NavLink>
          </Nav>
          <div className='d-flex align-items-center gap-2'>
            <SearchField />
            {user ? (
              <>
                <NavLink className='nav-link' to='/profile'><FaUser /> Profile</NavLink>
                <button className='btn btn-outline-light' onClick={logout}><FaSignOutAlt /> Logout</button>
              </>
            ) : (
              <>
                <NavLink className='nav-link' to='/login'><FaSignInAlt /> Login</NavLink>
                <NavLink className='nav-link' to='/signup'><FaUserPlus /> Sign Up</NavLink>
              </>
            )}
          </div>
        </Navbar.Collapse>
      </div>
    </Navbar>
  );
}

export default Navigation;