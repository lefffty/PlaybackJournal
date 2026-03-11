import React from "react";
import {Card, Row} from 'react-bootstrap';

import ProfileListLink from "./ProfileListLink";

const ProfileLinksGroup = ({groupHeader, cardsTexts, links, mds}) => {
    return (
        <Row className="g-0">
            <Card.Header>
                {groupHeader}
            </Card.Header>
            {links.map(
                (link, index) => {
                    return <ProfileListLink cardText={cardsTexts[index]} link={link} md={mds[index]}/>
                }
            )}
        </Row>
    )
}

export default ProfileLinksGroup;