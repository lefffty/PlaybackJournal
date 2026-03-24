import React from "react";
import { Card, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import { FaAngleRight } from "react-icons/fa";

const ItemGrid = ({urlPathName, itemsName, itemId, items, urlPath, kind}) => {
    const borderRadius = urlPath === 'artists' ? '50%' : '5%';
    const imageKey = urlPath === 'artists' ? 'avatar' : 'cover';
    const nameKey = urlPath === 'artists' ? 'username' : 'name';

    return (
        <Card className="mb-3 border-0">
            <Card.Body>
                <Card.Header className="fs-3 mb-3">
                    <div className="d-flex align-items-end" style={{height: '50px'}}>
                        <Link
                            to={`/${urlPathName}/${itemId}/${kind}/`}
                            className="text-decoration-none"
                            style={{
                                color: "black"
                            }}
                        >
                            <Card.Text className="mb-0 me-2">
                                <b>{itemsName}</b>
                            </Card.Text>
                        </Link>
                        <Link
                            to={`/${urlPathName}/${itemId}/${kind}/`}
                            style={{
                                color: "black"
                            }}
                        >
                            <FaAngleRight
                                className="hover-shift"
                            />
                        </Link>
                    </div>
                </Card.Header>
                <Row className="g-0">
                    {items.map(
                        (item) => {
                            return (
                                <Col style={{textAlign: "center"}}>
                                    <Link
                                        to={`/${urlPath}/${item.id}`}
                                    >
                                        <Card.Img
                                            src={item[imageKey]}
                                            style={{
                                                borderRadius: borderRadius,
                                                width: '240px',
                                                height: '240px',
                                                objectFit: 'cover'
                                            }}
                                            className="album-cover"
                                        />
                                    </Link>
                                    <Link
                                        to={`/${urlPath}/${item.id}`}
                                        className="text-decoration-none fs-5"
                                        style={{color: "black"}}
                                    >
                                        <Col>
                                            {item[nameKey]}
                                        </Col>
                                    </Link>
                                </Col>
                            )
                        }
                    )}
                </Row>
            </Card.Body>
        </Card>
    )
}

export default ItemGrid;