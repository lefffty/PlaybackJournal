import React, { useState } from "react";
import {Form} from 'react-bootstrap'
import { useNavigate } from "react-router-dom";

const SearchField = (props) => {
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const onKeyDownPressed = (e) => {
        if (e.key === 'Enter'){
            e.preventDefault();
            navigate(`/search?q=${encodeURIComponent(query)}`)
        }
    }

    return (
        <Form>
            <input
                type="text"
                placeholder="Search..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={onKeyDownPressed}
                style={{
                    borderColor: 'white',
                    borderRadius: '40px',
                    marginLeft: '50px',
                    paddingInline: '20px',
                    outline: 'none',
                    width: '500px',
                    fontSize: '24px'
                }}
            />
        </Form>
    )
}

export default SearchField;