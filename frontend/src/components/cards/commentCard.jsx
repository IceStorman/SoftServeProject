import axios from "axios";
import React, { useState } from "react";
import { SlArrowDown, SlArrowUp } from "react-icons/sl";
import apiEndpoints from "../../apiEndpoints";
import CommentsArea from "../containers/commentsArea";
import { useParams } from "react-router-dom";

export default function CommentCard({ comment_id, username, timestamp, content, isReplied }) {

    const [showReplies, setShowReplies] = useState(false);
    const [replies, setReplies] = useState([]);

    const [showReplyInput, setShowReplyInput] = useState(false);
    const [replyContent, setReplyContent] = useState("");
    const { articleId } = useParams();

    const fetchReplies = async () => {
        try {
            const response = await axios.get(
                `${apiEndpoints.url}${apiEndpoints.comment.getComments}`, {
                params:
                    { parent_comment_id: comment_id,
                    article_blob_id: articleId
                     },
            }
            );
            setReplies(response.data);
        } catch (error) {
            console.error("Error fetching replies:", error);
        }
    };

    const handleToggleReplies = () => {
        if (!showReplies) {
            fetchReplies();
        }
        setShowReplies(!showReplies);
    };

    const handleToggleReplyInput = () => {
        setShowReplyInput(!showReplyInput);
    };

    const saveReply = async () => {
        if (!replyContent.trim()) return;

        try {
            await axios.post(`${apiEndpoints.url}${apiEndpoints.comment.saveComment}`, {
                user_id: 1,
                article_blob_id: articleId,
                parent_comment_id: comment_id,
                content: replyContent,
            });

            setReplyContent("");
            setShowReplyInput(false);
            fetchReplies();
        } catch (error) {
            console.error("Error saving reply:", error);
        }
    };

    const [isEditing, setIsEditing] = useState(false);
    const [editedContent, setEditedContent] = useState(content);

    const handleToggleEditInput = () => {
        setIsEditing(!isEditing);
        setEditedContent(content);
    };

    const saveEditedComment = async () => {
        if (!editedContent.trim()) return;

        try {
            await axios.post(`${apiEndpoints.url}${apiEndpoints.comment.editComment}`, {
                comment_id: comment_id,
                content: editedContent,
            });

            setIsEditing(false);
        } catch (error) {
            console.error("Error updating comment:", error);
        }
    };

        const [isDeleted, setIsDeleted] = useState(false);

    const deleteComment = async () => {
        const confirmDelete = window.confirm("Are you sure you want to delete this comment?");
        if (!confirmDelete) return;

        try {
            await axios.delete(`${apiEndpoints.url}${apiEndpoints.comment.deleteComment}`, {
                data: { comment_id: comment_id }
            });

            setIsDeleted(true);
        } catch (error) {
            console.error("Error deleting comment:", error);
        }
    };

    if (isDeleted) return null;


    return (
        <div className="comment-card">
            <div className="comment-info">
                <h1>{username}</h1>
                <h3>{timestamp}</h3>
            </div>

            {isEditing ? (
                <div className="edit-input">
                    <input
                        type="text"
                        value={editedContent}
                        onChange={(e) => setEditedContent(e.target.value)}
                        maxLength={200}
                    />
                    <button onClick={saveEditedComment}>Save</button>
                    <button onClick={handleToggleEditInput}>Cancel</button>
                </div>
            ) : (
                <p>{content}</p>
            )}


            <div className="comment-actions">

                <button onClick={handleToggleReplies}>
                    replies {showReplies ? <SlArrowUp /> : <SlArrowDown />}
                </button>

                <button onClick={handleToggleReplyInput}>Reply</button>
                <button onClick={handleToggleEditInput}>Edit</button>
                <button onClick={deleteComment}>Delete</button>
            </div>

            {showReplyInput && (
                <div className="reply-input">
                    <input
                        type="text"
                        value={replyContent}
                        onChange={(e) => setReplyContent(e.target.value)}
                        placeholder="Write a reply..."
                        maxLength={80}
                    />
                    <button onClick={saveReply}>Send</button>
                </div>
            )}

            {showReplies && (
                <CommentsArea>
                    {replies.length > 0 ? (
                        replies.map(reply => (
                            <CommentCard
                                key={reply.id}
                                comment_id={reply.comment_id}
                                username={reply.username}
                                timestamp={reply.timestamp}
                                content={reply.content}
                                isReplied={reply.isReplied}
                            />
                        ))
                    ) : (
                        <p>No replies yet.</p>
                    )}
                </CommentsArea>
            )}
        </div>
    );
}