import {useLocation, useNavigate, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import VideoPlayer from "../../components/stream/videoPlayer";

function InsideStreamPage() {
    const { streamId } = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const stateStream = location.state || null;

    const [stream, setStream] = useState(stateStream);
    const [videoIds, setVideoIds] = useState([]);

    // useEffect(() => {
    //
    //     const fetchStreams = async () => {
    //         try {
    //             setLoading(true);
    //
    //             const response = await axios.post(
    //                 `${apiEndpoints.url}${apiEndpoints.stream.getInfo}`,
    //                 {
    //                     stream_id: streamId,
    //                 },
    //                 {
    //                     headers: {'Content-Type': 'application/json'},
    //                 }
    //             );
    //             const fetchedStream = response.data;
    //
    //             const youtubeVideoIds = fetchedStream.links
    //                 .map(link => extractYouTubeId(link))
    //                 .filter(id => id !== null);
    //
    //             const otherLinks = fetchedStream.links.filter(link => extractYouTubeId(link) === null);
    //
    //             setStream({
    //                 ...fetchedStream,
    //                 youtubeVideoIds,
    //                 otherLinks,
    //             });
    //         } catch (error) {
    //             if (stream.length === 0) {
    //                 navigate("/not-existing")
    //             }
    //             toast.error(`:( Troubles With This Stream Loading: ${error}`);
    //         }
    //     };
    //
    //     fetchStreams();
    // }, []);
    //

    useEffect(() => {
        if (!stream) {
            axios.post(
                `${apiEndpoints.url}${apiEndpoints.stream.getStreamsSearch}`,
                { filters: [{ filter_name: "stream_id", filter_value: streamId }] },
                { headers: { 'Content-Type': 'application/json' } }
            )
                .then(res => {
                    if (res.data.items.length !== 0) {
                        setStream(res.data.items[0]);
                    } else {
                        navigate("/not-existing")
                    }
                })
                .catch(error => {
                    if (!axios.isCancel(error)) {
                        toast.error(`:( Troubles With Stream Loading: ${error}`);
                    }
                });
        }
    }, [streamId]);

    useEffect(() => {
        if (stream && stream.stream_url) {
            const ids = stream.stream_url.map(link => {
                return extractYouTubeId(link);
            }).filter(Boolean);
            setVideoIds(ids);
        }
    }, [stream]);

    const extractYouTubeId = (url) => {
        const match = url.match(/[?&]v=([^&]+)/) || url.match(/youtu\.be\/([^?]+)/);
        return match ? match[1] : null;
    };

    return(
        <VideoPlayer
            youtubeLinks={videoIds}
            otherLinks={stream?.stream_url}
        />
    )



}
export default InsideStreamPage;