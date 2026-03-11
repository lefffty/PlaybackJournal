import React, { useEffect, useState } from "react";

import './UserList.css';
import UserListFunction from './Utils/UserListFunction';

const UserPlaylistsList = ({listType}) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const token = localStorage.getItem('auth_token');

    const fetchFunction = UserListFunction(listType);

    useEffect(
        () => {
            fetchFunction()
            .then(
                (response) => {
                    setData(response.data);
                }
            )
            .catch(
                (e) => {
                    setError(e.toString());
                }
            )
        },
        [token]
    )

    if (error){
        return (
            <div>
                Error: {error}
            </div>
        )
    }


};

export default UserPlaylistsList;