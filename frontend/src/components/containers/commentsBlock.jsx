import React from "react";
import { useState, useContext } from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import CommentsArea from "./commentsArea";
import CommentCard from "../cards/commentCard";
import { useParams, useNavigate } from "react-router-dom";
import { AuthContext } from "../../pages/registration/AuthContext";
import { toast } from "sonner";
import globalVariables from "../../globalVariables";

const CommentsBlock = ({ comments }) => {
    const [newComment, setNewComment] = useState("");
    const { articleId } = useParams();
    const { user } = useContext(AuthContext)
    const navigate = useNavigate();

    const handleChange = (e) => {
        if (e.target.value.length <= 80) {
            setNewComment(e.target.value);
        }
    };

    const saveComment = async (content) => {
        if (user) {
            try {
                await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.comment.save}`, {
                    user_id: user.user_id,
                    article_blob_id: articleId,
                    content: content
                }
                );
                setNewComment("");
            }
            catch (error) {
                toast.error(`Failed to save comment: ${error}`)
            }
        }
        else {
            const notify = () => toast('Sign in to add comment', {
                action: {
                    label: 'sign in',
                    onClick: () =>  navigate(globalVariables.routeLinks.signInRoute) ,
                },
            });
            notify()
        }
    };

    return (
        <section className="comments-block">
            <section className="comments-header">
                <h1>Comments</h1>
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
                <p>{newComment.length}/80</p>
                <button className="filled" onClick={() => saveComment(newComment)}>Add</button>
            </div>
            <CommentsArea>
                {comments.length > 0 ? (
                    comments.map(comment => (
                        <CommentCard
                            comment_id={comment.comment_id}
                            user_id={comment.user_id}
                            username={comment.username}
                            timestamp={comment.timestamp}
                            content={comment.content}
                            isReplied={comment.isReplied}
                        />
                    ))
                ) : (
                    <p>No comments yet.</p>
                )}
            </CommentsArea>
        </section>
    );
}

export default CommentsBlock;