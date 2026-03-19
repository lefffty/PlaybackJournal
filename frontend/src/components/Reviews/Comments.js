import React from "react";
import Container from "react-bootstrap/Container";
import { Card, Col, Row } from "react-bootstrap";
import { FaRegUser } from "react-icons/fa";
import moment from "moment";

const Comments = ({ comments }) => {
  return (
    <div>
      {comments.map((comment) => (
        <Card key={comment.id} className="mb-3 border-0">
          <Card.Body>
            <div
                className="d-flex"
                style={{
                    backgroundColor: '#eadedeab'
                }}
            >
              <div style={{ flexShrink: 0, marginRight: '15px' }}>
                <img
                  src={`http://localhost:8000/${comment.author.avatar}`}
                  alt="аватар"
                  style={{
                      width: '75px',
                      height: '75px',
                      objectFit: 'cover',
                    }}
                    />
              </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '8px' }}>
                <FaRegUser />
            <div>
                <Card.Text className="mb-0">{comment.author.username}</Card.Text>
                <div>
                    {moment(comment.created_at).format('D MMMM YYYY [г.] HH:mm')}
                </div>
            </div>
            </div>
            </div>
            <div
                style={{
                    marginLeft: '90px',
                    marginTop: '10px'
                }}
            >
                {comment.text}
            </div>
          </Card.Body>
        </Card>
      ))}
    </div>
  );
};

export default Comments;