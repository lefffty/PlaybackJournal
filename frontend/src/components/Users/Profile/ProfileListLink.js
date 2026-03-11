import React from "react";
import {Card, Col} from 'react-bootstrap';
import { Link } from "react-router-dom";
import { FaAngleRight } from "react-icons/fa";

const ProfileListLink = ({link, cardText, md}) => {
    return (
        <Col md={md}>
            <Card.Header className="fs-4">
                <div className="d-flex align-items-end">
                    <Link to={link} className="text-decoration-none">
                        <Card.Text className="mb-0 me-2" style={{color: "black", textAlign:"center"}}>
                            <b>{cardText}</b>
                        </Card.Text>
                    </Link>
                    <Link to={link} style={{color: "black"}}>
                        <FaAngleRight className="hover-shift"/>
                    </Link>
                </div>
            </Card.Header>
        </Col>
    )
}

export default ProfileListLink;