import React from "react";
import { useState } from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import CommentsArea from "./commentsArea";
import CommentCard from "../cards/commentCard";
import { useParams } from "react-router-dom";

const CommentsBlock = ({ comments }) => {
    const [newComment, setNewComment] = useState("");
    const { articleId } = useParams();

    const handleChange = (e) => {
        if (e.target.value.length <= 80) {
            setNewComment(e.target.value);
        }
    };

    const saveComment = async (content) => {
        try {
            await axios.post(
                `${apiEndpoints.url}${apiEndpoints.comment.saveComment}`, {
                user_id: 1,
                article_blob_id: articleId,
                content: content
            }
            );
            setNewComment("");
        }
        catch (error) {

        }
    };

    return (
        <section className="comments-block">
            <section className="comments-header">
                <h1>Comments</h1>
                <h1>Sort by</h1>
            </section>
            <hr />
            <div className="comment-input">
                <input
                    type="text"
                    value={newComment}
                    onChange={handleChange}
                    placeholder="Add comment..."
                    maxLength={80}
                />
                <button onClick={() => saveComment(newComment)}>Add</button>
                <p>{newComment.length}/80</p>
            </div>
            <CommentsArea>
                {comments.length > 0 ? (
                    comments.map(comment => (
                        <CommentCard
                            comment_id={comment.comment_id}
                            username={comment.username}
                            timestamp={comment.timestamp}
                            content={comment.content}
                            isReplied={comment.isReplied}
                        />
                    ))
                ) : (
                    <p>No children yet.</p>
                )}
            </CommentsArea>
        </section>
    );
}

export default CommentsBlock;