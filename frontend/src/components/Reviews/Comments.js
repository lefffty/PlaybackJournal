import React from "react";
import Container from "react-bootstrap/Container";
import { Card, Col, Row } from "react-bootstrap";
import { FaRegUser } from "react-icons/fa";
import moment from "moment";

import CommentReaction from "../Common/Reactions/Comment/Reaction";

const Comments = ({ comments }) => {
  const token = localStorage.getItem('auth_token');
  const isAuthenticated = token && token !== '';

  return (
    <div>
      {comments.map((comment) => (
          <Card key={comment.id} className="mb-3 border-0">
            <Card.Body>
              <div className="d-flex">
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

                <div style={{ flex: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <FaRegUser className="me-2" />
                    <span><b>{comment.author.username}</b></span>
                    <div className="text-muted small">
                      {moment(comment.created_at).format('D MMMM YYYY [г.] HH:mm')}
                    </div>
                  </div>
                  {isAuthenticated && (
                    <CommentReaction
                      commentId={comment.id}
                      initialState={comment.reaction}
                      plusCount={comment.plus_count}
                      minusCount={comment.minus_count}
                    />
                  )}
                </div>
              </div>

              <div style={{ marginLeft: '90px', marginTop: '10px' }}>
                {comment.text}
              </div>
            </Card.Body>
          </Card>
      ))}
    </div>
  );
};

export default Comments;