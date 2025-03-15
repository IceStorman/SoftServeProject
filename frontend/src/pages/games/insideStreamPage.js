import {useLocation, useNavigate, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";
import VideoPlayer from "../../components/stream/videoPlayer";

function InsideStreamPage() {
    const {sportName, id} = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const streamId = location.state || id;
    const [game, setGame] = useState([]);

    const [stream, setStream] = useState([]);

    const [loading, setLoading] = useState(false);


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
    // // useEffect(() => {
    // //     axios.get(`${apiEndpoints.url}${apiEndpoints.games.getThisGame}`)
    // //         .then(res => {
    // //             const returnedGames = res.data;
    // //             setGame(returnedGames);
    // //         })
    // //         .catch(error => {
    // //             toast.error(`:( Troubles With Games Loading: ${error}`);
    // //         });
    // // }, []);

    const extractYouTubeId = (url) => {
        const match = url.match(/[?&]v=([^&]+)/) || url.match(/youtu\.be\/([^?]+)/);
        return match ? match[1] : null;
    };


    useEffect(() => {
        (stream?.url) ? setLoading(false)
            : setTimeout(() => {
                setLoading(false);
            }, 2000)
    }, [stream]);

    return(
        <>

            {/* TEST EXAMPLE WHAT INFO WILL BE HERE, WHILE I HAVEN'T API LOGIC */}

            <VideoPlayer
                game={{
                    name1: "Nuggets",
                    name2: "Lakers",
                    score1: 93,
                    score2: 15,
                    logo1: "https://upload.wikimedia.org/wikipedia/ru/2/21/Denver_Nuggets.png",
                    logo2: "https://cdn.nba.com/teams/legacy/www.nba.com/lakers/sites/lakers/files/ts_180804logo.jpg"
                }}
                youtubeLinks={["3ExpJPpC6r4", "LvjKYG8J50k", "dQw4w9WgXcQ", "dQw4w9WgXcQ", "dQw4w9WgXcQ", "dQw4w9WgXcQ", "dQw4w9WgXcQ", "GWuF23poTf4"]}
                otherLinks={[
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                ]}
            />


            {/*<VideoPlayer*/}
            {/*    game={game}*/}
            {/*    youtubeLinks={stream.youtubeVideoIds}*/}
            {/*    otherLinks={stream.otherLinks}*/}
            {/*/>*/}

    </>
    )



}
export default InsideStreamPage;