import axios from "axios";
import React, { useState, useContext } from "react";
import { SlArrowDown, SlArrowUp } from "react-icons/sl";
import apiEndpoints from "../../apiEndpoints";
import CommentsArea from "../containers/commentsArea";
import { useParams } from "react-router-dom";
import { AuthContext } from "../../pages/registration/AuthContext";

export default function CommentCard({ comment_id, user_id, username, timestamp, content }) {

    const [showReplies, setShowReplies] = useState(false);
    const [replies, setReplies] = useState([]);

    const [showReplyInput, setShowReplyInput] = useState(false);
    const [replyContent, setReplyContent] = useState("");
    const { articleId } = useParams();
    const { user } = useContext(AuthContext)

    const loadMore = () => {
        if (hasMore) {
            fetchReplies(currentPage + 1);
        }
    };

    const [currentPage, setCurrentPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);

    const fetchReplies = async (page = 1, perPage = 10) => {
        try {
            const response = await axios.get(
                `${apiEndpoints.url}${apiEndpoints.comment.getComments}`, {
                params:
                {
                    parent_comment_id: comment_id,
                    article_blob_id: articleId,
                    page: page,
                    per_page: perPage,
                },
            }
            );
            const { comments, has_more } = response.data;

            setReplies(prev => [...prev, ...comments]);
            setCurrentPage(page);
            setHasMore(has_more);
        } catch (error) {
            console.error("Error fetching replies:", error);
        }
    };

    const handleToggleReplies = () => {
        if (!showReplies) {
            setReplies([]);        
            fetchReplies(1);          
            setCurrentPage(1);       
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
                user_id: user.user_id,
                article_blob_id: articleId,
                parent_comment_id: comment_id,
                content: replyContent,
            });

            setReplyContent("");
            setShowReplyInput(false);
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

    const date = new Date(timestamp);

    const time = date.toLocaleString('uk', { hour: '2-digit', minute: '2-digit', hour12: false });
    const formattedDate = date.toLocaleString('uk', { day: '2-digit', month: '2-digit', year: '2-digit' });
  
    const formattedTimestamp = `${time}, ${formattedDate}`;

    return (
        <div className="comment-card">
            <div className="comment-info">
                <h1>{username}</h1>
                <h3>{formattedTimestamp}</h3>
            </div>

            {isEditing ? (
                <div className="reply-input">
                    <input
                        type="text"
                        value={editedContent}
                        onChange={(e) => setEditedContent(e.target.value)}
                        maxLength={80}
                    />
                    <p>{editedContent.length}/80</p>
                    <button className="filled" onClick={saveEditedComment}>Save</button>
                    <button className="filled" onClick={handleToggleEditInput}>Cancel</button>
                </div>
            ) : (
                <p>{content}</p>
            )}


            <div className="comment-actions">

                <button className="filled" onClick={handleToggleReplies}>
                    Replies {showReplies ? <SlArrowUp /> : <SlArrowDown />}
                </button>

                <button className="filled" onClick={handleToggleReplyInput}>Reply</button>

                { user && user.user_id === user_id && (
                    <>
                        <button className="filled" onClick={handleToggleEditInput}>Edit</button>
                        <button className="filled" onClick={deleteComment}>Delete</button>
                    </>
                )}

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
                    <p>{replyContent.length}/80</p>
                    <button className="filled" onClick={saveReply}>Send</button>
                </div>
            )}

            {showReplies && (
                <CommentsArea>
                    {replies.length > 0 ? (
                        replies.map(reply => (
                            <CommentCard
                                key={reply.id}
                                comment_id={reply.comment_id}
                                user_id={reply.user_id}
                                username={reply.username}
                                timestamp={reply.timestamp}
                                content={reply.content}
                                isReplied={reply.isReplied}
                            />
                        ))
                    ) : (
                        <p>No replies yet.</p>
                    )}
                    {hasMore && <button className="boxed" onClick={loadMore}>More</button>}
                </CommentsArea>
                
            )}
        </div>
    );
}