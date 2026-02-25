import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";

import UserService from "../services/UserService";
import { useNavigate } from "react-router-dom";


function Avatar(){
    const [file, setFile] = useState(null);
    const navigate = useNavigate();

    function uploadBase64Image(base64String){
        const data = {
            avatar: base64String
        }
        UserService.setAvatar(data)
        .then(
            (_) => {
                navigate('/profile');
            }
        )
        .catch(
            (e) => {
                console.log(e.toString());
            }
        )
    }

    function onButtonClick(){
        const reader = new FileReader();
        reader.onload = () => uploadBase64Image(reader.result);
        if (file) reader.readAsDataURL(file);
    }


    return (
        <Form>
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Choose image</Form.Label>
                <Form.Control
                    type="file"
                    accept=".png, .jpg"
                    onChange={(e) => {setFile(e.target.files[0])}}
                />
            </Form.Group>
            <Button onClick={onButtonClick}>
                Submit
            </Button>
        </Form>
    )
}

export default Avatar;