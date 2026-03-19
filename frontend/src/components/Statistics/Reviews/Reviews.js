import React from 'react';
import { Card, Row, Col } from 'react-bootstrap';
import './Reviews.css';

const Reviews = ({ stats }) => {
  const calculatePercent = (value) => ((value / stats.total) * 100).toFixed(2);

  return (
    <div className="statistics-sticky">
      <Card className="shadow-sm border-0">
        <Card.Body>
          <Card.Title className="text-center mb-4">Статистика отзывов</Card.Title>
          
          <div className="text-center mb-3">
            <span className="display-4 fw-bold">{stats.total}</span>
            <span className="text-muted ms-2">Всего</span>
          </div>

          <Row className="mb-2 align-items-center">
            <Col xs={6} className="text-success fw-bold">Положительные</Col>
            <Col xs={3} className="text-end fw-bold">{stats.positive}</Col>
            <Col xs={3} className="text-end text-muted">
              {calculatePercent(stats.positive)}%
            </Col>
          </Row>

          <Row className="mb-2 align-items-center">
            <Col xs={6} className="text-danger fw-bold">Отрицательные</Col>
            <Col xs={3} className="text-end fw-bold">{stats.negative}</Col>
            <Col xs={3} className="text-end text-muted">
              {calculatePercent(stats.negative)}%
            </Col>
          </Row>

          <Row className="mb-2 align-items-center">
            <Col xs={6} className="text-secondary fw-bold">Нейтральные</Col>
            <Col xs={3} className="text-end fw-bold">{stats.neutral}</Col>
            <Col xs={3} className="text-end text-muted">
              {calculatePercent(stats.neutral)}%
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Reviews;